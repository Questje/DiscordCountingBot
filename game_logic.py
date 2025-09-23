"""Game logic and state management for the counting bot."""

import json
import os
import threading
from datetime import datetime
from constants import STATS_FILE, GAME_STATE_FILE, ACHIEVEMENT_EMOJIS
import concurrent.futures

# State variables
next_number = 1
user_stats = {}
number_history = []
last_correct_user = None
last_streak_milestone = 0
total_correct = 0
testing_mode = False

# Thread safety
SHARED_DATA_LOCK = threading.Lock()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def _write_state_to_disk(game_state_copy, stats_copy):
    """Write state to disk (run in thread to avoid blocking)."""
    try:
        with open(GAME_STATE_FILE, 'w') as f:
            json.dump(game_state_copy, f, indent=4)
        
        with open(STATS_FILE, 'w') as f:
            json.dump(stats_copy, f, indent=4)
        
        print(f"💾 Game state saved at {datetime.now().isoformat()}")
    except (IOError, TypeError) as e:
        print(f"❌ Error saving state to disk: {e}")


def save_state():
    """Schedule game state to be saved without blocking."""
    with SHARED_DATA_LOCK:
        game_state_copy = {
            'next_number': next_number,
            'last_correct_user': last_correct_user,
            'total_correct': total_correct,
            'last_streak_milestone': last_streak_milestone,
            'testing_mode': testing_mode,
        }
        stats_copy = {
            uid: {**stats, 'achievements': list(stats.get('achievements', []))}
            for uid, stats in user_stats.items()
        }
    
    executor.submit(_write_state_to_disk, game_state_copy, stats_copy)


def load_state():
    """Load game state and user stats from JSON files."""
    global next_number, user_stats, last_correct_user, total_correct, last_streak_milestone, testing_mode
    
    with SHARED_DATA_LOCK:
        try:
            if os.path.exists(GAME_STATE_FILE):
                with open(GAME_STATE_FILE, 'r') as f:
                    game_state = json.load(f)
                    next_number = game_state.get('next_number', 1)
                    last_correct_user = game_state.get('last_correct_user', None)
                    total_correct = game_state.get('total_correct', 0)
                    last_streak_milestone = game_state.get('last_streak_milestone', 0)
                    testing_mode = game_state.get('testing_mode', False)
                    print(f"✅ Loaded game state from {GAME_STATE_FILE}.")
            
            if os.path.exists(STATS_FILE):
                with open(STATS_FILE, 'r') as f:
                    loaded_stats = json.load(f)
                    for uid, stats in loaded_stats.items():
                        user_id = int(uid)
                        user_stats[user_id] = stats
                        user_stats[user_id]['achievements'] = set(stats.get('achievements', []))
                        user_stats[user_id].setdefault('best_streak', stats.get('streak', 0))
                    print(f"✅ Loaded {len(user_stats)} user records from {STATS_FILE}.")
        except (IOError, json.JSONDecodeError) as e:
            print(f"⚠️ Could not load state, starting fresh. Reason: {e}")


def reset_game(preserve_stats=True):
    """Reset the game state."""
    global next_number, last_correct_user, last_streak_milestone, total_correct
    
    with SHARED_DATA_LOCK:
        next_number = 1
        last_correct_user = None
        last_streak_milestone = 0
        total_correct = 0
        
        if not preserve_stats:
            user_stats.clear()
            number_history.clear()
        
        save_state()


def update_user_stats(user_id, username, correct):
    """Update statistics for a user."""
    if user_id not in user_stats:
        user_stats[user_id] = {
            'correct': 0,
            'wrong': 0,
            'username': username,
            'streak': 0,
            'best_streak': 0,
            'achievements': set(),
            'consecutive_wrong': 0,
            'back_to_back_violations': 0,
            'timeout_until': 0
        }
    
    stats = user_stats[user_id]
    stats['username'] = username
    
    if correct:
        stats['correct'] += 1
        stats['streak'] += 1
        stats['consecutive_wrong'] = 0
        
        if stats['streak'] > stats.get('best_streak', 0):
            stats['best_streak'] = stats['streak']
    else:
        stats['wrong'] += 1
        stats['streak'] = 0
        stats['consecutive_wrong'] += 1


def add_to_history(number, username, input_text, types_used, parse_method):
    """Add an entry to the number history."""
    global number_history
    
    number_history.append({
        'number': number,
        'username': username,
        'input': input_text,
        'types': list(types_used) if types_used else ['integer'],
        'method': parse_method,
        'timestamp': datetime.now().isoformat()
    })
    
    if len(number_history) > 100:
        number_history = number_history[-100:]


def get_game_state():
    """Get current game state (thread-safe)."""
    with SHARED_DATA_LOCK:
        return {
            'next_number': next_number,
            'last_correct_user': last_correct_user,
            'total_correct': total_correct,
            'testing_mode': testing_mode,
            'user_stats': dict(user_stats),
            'history': list(number_history)
        }


def process_correct_answer(user_id, username, parsed_number, content, types_used, parse_method, languages):
    """Process a correct answer."""
    global next_number, last_correct_user, total_correct
    
    last_correct_user = user_id
    update_user_stats(user_id, username, True)
    
    # Unlock achievements
    user_achievements = user_stats[user_id].get('achievements', set())
    for type_used in types_used:
        user_achievements.add(type_used)
    for lang_used in languages:
        user_achievements.add(lang_used)
    
    # Check for polyglot achievement (4+ languages in one expression)
    if len(languages) >= 4:
        user_achievements.add('polyglot')
    
    user_stats[user_id]['achievements'] = user_achievements
    
    total_correct += 1
    add_to_history(parsed_number, username, content, types_used, parse_method)
    next_number += 1
    
    return True


def process_wrong_answer(user_id, username, should_reset):
    """Process a wrong answer."""
    global next_number, last_correct_user, total_correct
    
    last_correct_user = None
    update_user_stats(user_id, username, False)
    
    if should_reset:
        next_number = 1
        last_correct_user = None
        total_correct = 0
        return True
    
    return False