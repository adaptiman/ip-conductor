"""A simple console application to interact with Instapaper bookmarks."""

from article_manager import ArticleManager


def main():
    """Main function to run the Instapaper console app."""
    try:
        manager = ArticleManager()
        manager.run()
    except (AttributeError, ValueError, RuntimeError, OSError, KeyError) as e:
        print(f"Error starting application: {e}")
        return
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return


if __name__ == "__main__":
    main()