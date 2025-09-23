"""Utility functions for the counting bot."""

import random
import time
from constants import MISTAKE_PUNS, STREAK_MESSAGES


def get_mistake_severity(user_stats):
    """Determine mistake message severity based on user performance."""
    if not user_stats:
        return 'gentle'
    
    total = user_stats['correct'] + user_stats['wrong']
    consecutive_wrong = user_stats.get('consecutive_wrong', 0)
    
    if total == 0:
        return 'gentle'
    
    accuracy = user_stats['correct'] / total
    
    if consecutive_wrong >= 5 or (consecutive_wrong >= 3 and accuracy < 0.3):
        return 'brutal'
    if consecutive_wrong >= 3 or (consecutive_wrong >= 2 and accuracy < 0.5):
        return 'harsh'
    if consecutive_wrong >= 2 or accuracy < 0.7:
        return 'medium'
    
    return 'gentle'


def get_mistake_message(user_stats):
    """Get a random mistake message based on user performance."""
    severity = get_mistake_severity(user_stats)
    return random.choice(MISTAKE_PUNS[severity])


def get_streak_message(total, last_milestone):
    """Get a streak celebration message if milestone reached."""
    if total % 10 == 0 and total > last_milestone:
        return random.choice(STREAK_MESSAGES).format(total), total
    return None, last_milestone


def check_user_timeout(user_stats):
    """Check if a user is in timeout."""
    if not user_stats:
        return False, 0
    
    timeout_until = user_stats.get('timeout_until', 0)
    if timeout_until > time.time():
        return True, int(timeout_until - time.time())
    
    return False, 0


def apply_timeout(user_stats, seconds):
    """Apply a timeout to a user."""
    user_stats['timeout_until'] = time.time() + seconds
    return user_stats


def truncate_input(input_text, max_length=25):
    """Truncate input text for display."""
    if len(input_text) <= max_length:
        return input_text
    return input_text[:max_length] + '...'