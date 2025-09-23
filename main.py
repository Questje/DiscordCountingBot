"""Main entry point for the Discord counting bot."""

import threading
from bot import run as run_discord
from web_dashboard import run as run_flask
from parser import executor

#from keep_alive import keep_alive # Webapp keepalive (optional for us)

def main():
    """Start both the Flask server and Discord bot."""
    # Start Flask in a daemon thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        # Run Keep alive Thread
        #keep_alive()

        # Run Discord bot in main thread
        run_discord()        
    finally:
        print("Shutting down thread pool...")
        executor.shutdown(wait=True)

if __name__ == '__main__':
    main()