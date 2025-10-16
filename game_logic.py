#!/usr/bin/env python
# -*- coding: utf-8 -*- 
"""Game logic and state management for the counting bot."""

import os
import json
import threading
from datetime import datetime
from dotenv import load_dotenv
import pymysql
from pymysql.cursors import DictCursor
import concurrent.futures

# Load environment variables
load_dotenv('.env')

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'charset': 'utf8mb4',
    'cursorclass': DictCursor
}

# Check if we're in development mode (be defensive if ENVIRONMENT is not set)
_env_val = os.getenv('ENVIRONMENT', '')
IS_DEV_MODE = _env_val.lower() in ('dev', 'development', 'local')

if IS_DEV_MODE:
    print("⚠️  DEVELOPMENT MODE - Database writes are DISABLED")

# State variables (cache)
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


def get_db_connection():
    """Create and return a database connection."""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        raise


def _write_game_state_to_db(game_state_copy):
    """Write game state to database (run in thread to avoid blocking)."""
    if IS_DEV_MODE:
        print(f"🔧 DEV MODE: Skipping game state save to database")
        return
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE game_state 
                SET next_number = %s,
                    last_correct_user = %s,
                    total_correct = %s,
                    last_streak_milestone = %s,
                    testing_mode = %s
                WHERE id = 1
            """, (
                game_state_copy['next_number'],
                game_state_copy['last_correct_user'],
                game_state_copy['total_correct'],
                game_state_copy['last_streak_milestone'],
                game_state_copy['testing_mode']
            ))
            conn.commit()
        conn.close()
        print(f"💾 Game state saved to database at {datetime.now().isoformat()}")
    except Exception as e:
        print(f"❌ Error saving game state to database: {e}")


def _write_user_stats_to_db(user_id, stats):
    """Write user stats to database (run in thread to avoid blocking)."""
    if IS_DEV_MODE:
        print(f"🔧 DEV MODE: Skipping user stats save for user {user_id}")
        return
    
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            achievements_json = json.dumps(list(stats.get('achievements', set())))
            cursor.execute("""
                INSERT INTO user_stats 
                (user_id, username, correct, wrong, streak, best_streak, 
                 achievements, consecutive_wrong, back_to_back_violations, timeout_until)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    username = VALUES(username),
                    correct = VALUES(correct),
                    wrong = VALUES(wrong),
                    streak = VALUES(streak),
                    best_streak = VALUES(best_streak),
                    achievements = VALUES(achievements),
                    consecutive_wrong = VALUES(consecutive_wrong),
                    back_to_back_violations = VALUES(back_to_back_violations),
                    timeout_until = VALUES(timeout_until)
            """, (
                user_id,
                stats.get('username', ''),
                stats.get('correct', 0),
                stats.get('wrong', 0),
                stats.get('streak', 0),
                stats.get('best_streak', 0),
                achievements_json,
                stats.get('consecutive_wrong', 0),
                stats.get('back_to_back_violations', 0),
                stats.get('timeout_until', 0)
            ))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Error saving user stats to database: {e}")


def save_state():
    """Schedule game state to be saved without blocking."""
    if IS_DEV_MODE:
        print(f"🔧 DEV MODE: Skipping save_state()")
        return
    
    with SHARED_DATA_LOCK:
        game_state_copy = {
            'next_number': next_number,
            'last_correct_user': last_correct_user,
            'total_correct': total_correct,
            'last_streak_milestone': last_streak_milestone,
            'testing_mode': testing_mode,
        }
    
    # Save game state
    executor.submit(_write_game_state_to_db, game_state_copy)
    
    # Save all user stats
    with SHARED_DATA_LOCK:
        for uid, stats in user_stats.items():
            executor.submit(_write_user_stats_to_db, uid, stats.copy())


def load_state():
    """Load game state and user stats from database."""
    global next_number, user_stats, last_correct_user, total_correct, last_streak_milestone, testing_mode
    
    if IS_DEV_MODE:
        print(f"🔧 DEV MODE: Skipping load_state() from database, using defaults")
        return
    
    with SHARED_DATA_LOCK:
        try:
            conn = get_db_connection()
            
            # Load game state
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM game_state WHERE id = 1")
                game_state = cursor.fetchone()
                
                if game_state:
                    next_number = game_state['next_number']
                    last_correct_user = game_state['last_correct_user']
                    total_correct = game_state['total_correct']
                    last_streak_milestone = game_state['last_streak_milestone']
                    testing_mode = bool(game_state['testing_mode'])
                    print(f"✅ Loaded game state from database.")
                else:
                    print("⚠️ No game state found in database, using defaults.")
            
            # Load user stats
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user_stats")
                users = cursor.fetchall()
                
                for user in users:
                    user_id = user['user_id']
                    achievements = set(json.loads(user['achievements'])) if user['achievements'] else set()
                    
                    user_stats[user_id] = {
                        'username': user['username'],
                        'correct': user['correct'],
                        'wrong': user['wrong'],
                        'streak': user['streak'],
                        'best_streak': user['best_streak'],
                        'achievements': achievements,
                        'consecutive_wrong': user['consecutive_wrong'],
                        'back_to_back_violations': user['back_to_back_violations'],
                        'timeout_until': user['timeout_until']
                    }
                
                print(f"✅ Loaded {len(user_stats)} user records from database.")
            
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Could not load state from database, starting fresh. Reason: {e}")


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
        
        if not IS_DEV_MODE:
            save_state()
        else:
            print(f"🔧 DEV MODE: Skipping save after reset")


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
    
    # Save to database asynchronously (only if not in dev mode)
    if not IS_DEV_MODE:
        executor.submit(_write_user_stats_to_db, user_id, stats.copy())
    else:
        print(f"🔧 DEV MODE: Skipping user stats update for {username}")


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
            'history': list(number_history),
            'is_dev_mode': IS_DEV_MODE
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
    
    # Save game state to database (only if not in dev mode)
    if not IS_DEV_MODE:
        executor.submit(_write_game_state_to_db, {
            'next_number': next_number,
            'last_correct_user': last_correct_user,
            'total_correct': total_correct,
            'last_streak_milestone': last_streak_milestone,
            'testing_mode': testing_mode,
        })
    else:
        print(f"🔧 DEV MODE: Skipping game state save after correct answer")
    
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
        
        # Save game state to database (only if not in dev mode)
        if not IS_DEV_MODE:
            executor.submit(_write_game_state_to_db, {
                'next_number': next_number,
                'last_correct_user': last_correct_user,
                'total_correct': total_correct,
                'last_streak_milestone': last_streak_milestone,
                'testing_mode': testing_mode,
            })
        else:
            print(f"🔧 DEV MODE: Skipping game state save after wrong answer")
        
        return True
    
    return False