#!/usr/bin/env python3
import sys
from config.environment import check_environment
from ui.app import TranscriberApp


def main():
    """Main entry point for the application."""
    try:
        config = check_environment()
        app = TranscriberApp(config)
        app.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
