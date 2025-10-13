"""Main entry point for the Discord counting bot."""

from bot import run as run_discord
from parser import executor

def main():
    """Start the Discord bot."""
    try:
        # Run Discord bot in main thread
        run_discord()        
    finally:
        print("Shutting down thread pool...")
        executor.shutdown(wait=True)

if __name__ == '__main__':
    main()