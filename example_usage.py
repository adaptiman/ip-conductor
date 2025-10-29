"""Example showing how to use ArticleManager in other programs."""

from article_manager import ArticleManager


def example_usage():
    """Demonstrates various ways to use the ArticleManager class."""
    
    # Initialize the manager
    print("Creating ArticleManager instance...")
    try:
        manager = ArticleManager(bookmark_limit=10)  # Limit to 10 bookmarks for this example
        print("✅ ArticleManager initialized successfully!")
    except (AttributeError, ValueError, RuntimeError, OSError, KeyError, FileNotFoundError) as e:
        print(f"❌ Failed to initialize ArticleManager: {e}")
        return

    # Example 1: Get current bookmark title
    print("\n📖 Current bookmark:")
    manager.read_title()

    # Example 2: Navigate through bookmarks programmatically
    print("\n🔄 Navigating bookmarks...")
    if manager.next_bookmark():
        print("Moved to next bookmark:")
        manager.read_title()
    
    if manager.prev_bookmark():
        print("Moved back to previous bookmark:")
        manager.read_title()

    # Example 3: Show all bookmarks
    print("\n📚 All bookmarks:")
    manager.show_bookmarks()

    # Example 4: Add a new bookmark programmatically
    print("\n➕ Adding a bookmark programmatically...")
    # Uncomment the next line to actually add a bookmark
    # manager.instapaper_client.add_bookmark("https://example.com")
    print("(Commented out to avoid adding test bookmarks)")

    # Example 5: Use the manager in a custom loop
    print("\n🎮 Custom navigation example:")
    print("Going to first bookmark...")
    if manager.first_bookmark():
        manager.read_title()
    
    print("Going to last bookmark...")  
    if manager.last_bookmark():
        manager.read_title()

    print("\n✅ Example completed!")


if __name__ == "__main__":
    example_usage()