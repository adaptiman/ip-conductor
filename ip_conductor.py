"""A simple console application to interact with Instapaper bookmarks."""

import time
from article_manager import ArticleManager


def slow_print(text, delay=0.05):
    """Prints strings slowly to the console."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def display_title(manager):
    """Display the current bookmark title."""
    title = manager.get_current_title()
    if title:
        print(title)
    else:
        if manager.get_bookmark_count() == 0:
            print("No bookmarks found.")
        else:
            print("Current index is out of range.")


def display_article(manager, bookmark_number=None):
    """Display the bookmark content.

    Args:
        manager: The ArticleManager instance
        bookmark_number: Optional bookmark number (1-based) to read. If None, reads current bookmark.
    """
    if bookmark_number is not None:
        # Navigate to and read specific bookmark by number
        if manager.set_bookmark_by_number(bookmark_number):
            article = manager.get_current_article()
            if article:
                print(article)
            else:
                print(f"Unable to read bookmark {bookmark_number}")
        else:
            print(f"Invalid bookmark number: {bookmark_number}")
    else:
        # Read current bookmark
        article = manager.get_current_article()
        if article:
            print(article)
        else:
            if manager.get_bookmark_count() == 0:
                print("No bookmarks found.")
            else:
                print("Current index is out of range.")


def display_bookmarks(manager):
    """Display all bookmarks with numbers."""
    bookmarks = manager.get_bookmarks_list()
    if not bookmarks:
        print("No bookmarks found.")
    else:
        for i, title in enumerate(bookmarks, start=1):
            print(f"{i}. {title}")


def handle_add_bookmark(manager):
    """Handle adding a new bookmark."""
    url = input("Enter the URL to bookmark: ").strip()
    if not url:
        print("No URL entered. Bookmark not added.")
        return

    success, url, error = manager.add_bookmark_url(url)
    if success:
        print(f"Bookmark added successfully: {url}")
    else:
        print(f"Error adding bookmark: {error}")


def handle_delete_bookmark(manager):
    """Handle deleting the current bookmark."""
    # Get current bookmark info for confirmation
    info = manager.get_current_bookmark_info()
    if not info:
        print("No bookmark to delete.")
        return

    title = info[0]
    confirmation = input(f"Are you sure you want to delete '{title}'? (y/N): ").strip().lower()
    if confirmation in ['y', 'yes']:
        success, deleted_title, error = manager.delete_current_bookmark()
        if success:
            print(f"Bookmark '{deleted_title}' deleted.")
        else:
            print(f"Error deleting bookmark: {error}")
    else:
        print("Deletion cancelled.")


def handle_star_bookmark(manager):
    """Handle starring the current bookmark."""
    success, title, error = manager.star_current_bookmark()
    if success:
        print(f"Bookmark '{title}' starred successfully.")
    else:
        print(f"Error starring bookmark: {error}")


def handle_create_highlight(manager):
    """Handle creating a highlight for the current bookmark."""
    info = manager.get_current_bookmark_info()
    if not info:
        print("No bookmark to create highlight for.")
        return

    title = info[0]
    print(f"Creating highlight for: {title}")
    print("Enter the text you want to highlight (press Enter twice to finish):")

    lines = []
    empty_line_count = 0
    while empty_line_count < 2:
        line = input()
        if line.strip() == "":
            empty_line_count += 1
        else:
            empty_line_count = 0
        lines.append(line)

    # Remove the last empty lines
    while lines and lines[-1].strip() == "":
        lines.pop()

    highlight_text = "\n".join(lines).strip()

    if not highlight_text:
        print("No text entered. Highlight cancelled.")
        return

    success, title, highlight, error = manager.create_highlight_for_current(highlight_text)
    if success:
        print("Highlight created successfully!")
        ellipsis = '...' if len(highlight) > 100 else ''
        print(f"Highlighted text: {highlight[:100]}{ellipsis}")
    else:
        print(f"Error creating highlight: {error}")


def handle_archive_bookmark(manager):
    """Handle archiving the current bookmark."""
    success, title, error = manager.archive_current_bookmark()
    if success:
        print(f"Bookmark '{title}' archived successfully.")
    else:
        print(f"Error archiving bookmark: {error}")


def handle_navigation(manager, direction):
    """Handle navigation commands."""
    if direction == "next":
        if manager.next_bookmark():
            display_title(manager)
        else:
            print("Already at the last bookmark.")
    elif direction == "prev":
        if manager.prev_bookmark():
            display_title(manager)
        else:
            print("Already at the first bookmark.")
    elif direction == "first":
        if manager.first_bookmark():
            display_title(manager)
        else:
            print("No bookmarks found.")
    elif direction == "last":
        if manager.last_bookmark():
            display_title(manager)
        else:
            print("No bookmarks found.")


def run_console(manager):
    """Main console interface."""
    print("Welcome to the Instapaper Console App!")
    print("Type 'bookmarks' to list bookmarks, 'add' to add a bookmark, "
          "'delete' to delete current bookmark, 'star' to star current bookmark, "
          "'highlight' to create a highlight, 'archive' to archive current bookmark, "
          "or 'exit' to quit.")
    print("Navigation: 'title', 'next', 'prev', 'first', 'last', 'read', 'read <number>'")

    # Display the current bookmark title at startup
    display_title(manager)

    while True:
        try:
            cmd = input('> ').strip()
            cmd_lower = cmd.lower()

            if cmd_lower == 'exit':
                print("Goodbye!")
                break
            elif cmd_lower == 'bookmarks' or cmd_lower == 'articles':
                display_bookmarks(manager)
            elif cmd_lower == 'add':
                handle_add_bookmark(manager)
            elif cmd_lower == 'delete':
                handle_delete_bookmark(manager)
            elif cmd_lower == 'star':
                handle_star_bookmark(manager)
            elif cmd_lower == 'highlight':
                handle_create_highlight(manager)
            elif cmd_lower == 'archive':
                handle_archive_bookmark(manager)
            elif cmd_lower == 'title':
                display_title(manager)
            elif cmd_lower == 'next':
                handle_navigation(manager, "next")
            elif cmd_lower == 'previous' or cmd_lower == 'prev':
                handle_navigation(manager, "prev")
            elif cmd_lower == 'first':
                handle_navigation(manager, "first")
            elif cmd_lower == 'last':
                handle_navigation(manager, "last")
            elif cmd_lower == 'read':
                display_article(manager)
            elif cmd_lower.startswith('read '):
                # Handle "read <number>" command
                try:
                    parts = cmd.split()
                    if len(parts) == 2:
                        bookmark_num = int(parts[1])
                        display_article(manager, bookmark_num)
                    else:
                        print("Usage: read <number>")
                except ValueError:
                    print("Invalid bookmark number. Usage: read <number>")
            else:
                print("Unknown command. Try 'bookmarks', 'articles', 'add', 'delete', 'star', "
                      "'highlight', 'archive', 'title', 'next', 'prev', 'first', "
                      "'last', 'read', 'read <number>', or 'exit'.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except (AttributeError, ValueError, RuntimeError, OSError) as e:
            print(f"An error occurred: {e}")


def main():
    """Main function to run the Instapaper console app."""
    try:
        manager = ArticleManager()
        run_console(manager)
    except (AttributeError, ValueError, RuntimeError, OSError, KeyError) as e:
        print(f"Error starting application: {e}")
        return
    except KeyboardInterrupt:
        print("\nGoodbye!")
        return


if __name__ == "__main__":
    main()
