"""Flask web dashboard and API endpoints."""

from flask import Flask, render_template, jsonify
import asyncio
import game_logic
from bot import client, bot_ready

app = Flask(__name__)


@app.route('/')
def dashboard():
    """Serve the dashboard HTML."""
    return render_template('dashboard.html')


@app.route('/api/data')
def get_data():
    """Get current game data for the dashboard."""
    game_state = game_logic.get_game_state()
    
    leaderboard_data = []
    for user_id, stats in game_state['user_stats'].items():
        total = stats['correct'] + stats['wrong']
        percentage = (stats['correct'] / total * 100) if total > 0 else 0
        leaderboard_data.append({
            'username': stats['username'],
            'correct': stats['correct'],
            'wrong': stats['wrong'],
            'percentage': round(percentage, 1),
            'total': total,
            'streak': stats.get('streak', 0)
        })
    
    leaderboard_data.sort(key=lambda x: (x['correct'], x['percentage']), reverse=True)
    
    response_data = {
        'next_number': game_state['next_number'],
        'history': list(reversed(game_state['history'][-10:])),
        'leaderboard': leaderboard_data[:20],
        'bot_ready': bot_ready,
        'mystery_pending': False,
        'testing_mode': game_state['testing_mode']
    }
    
    return jsonify(response_data)


@app.route('/api/restart_bot', methods=['POST'])
def restart_bot():
    """Restart the bot and clear all data."""
    game_logic.reset_game(preserve_stats=False)
    
    if bot_ready and client.loop and not client.loop.is_closed():
        msg = "🔄 Bot restarting... Counting reset to **1** and leaderboard cleared!"
        client.loop.call_soon_threadsafe(
            asyncio.create_task,
            client.get_channel(CHANNEL_ID).send(msg)
        )
    
    return jsonify({'success': True, 'message': 'Bot restarted successfully'})


@app.route('/api/reset_game', methods=['POST'])
def reset_game():
    """Reset the game but keep statistics."""
    game_logic.reset_game(preserve_stats=True)
    
    if bot_ready and client.loop and not client.loop.is_closed():
        msg = "🔢 Game reset! Starting from **1** again. Leaderboard preserved."
        client.loop.call_soon_threadsafe(
            asyncio.create_task,
            client.get_channel(CHANNEL_ID).send(msg)
        )
    
    return jsonify({'success': True, 'message': 'Game reset to #1'})


def run():
    """Run the Flask app."""
    app.run(host='0.0.0.0', port=5000, debug=False)