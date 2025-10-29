"""ArticleManager class for managing Instapaper bookmark operations and navigation."""

import time
import netrc
import instapaper


class ArticleManager:
    """Manages Instapaper bookmark operations and navigation."""
    
    def __init__(self, bookmark_limit=25):
        """Initialize the ArticleManager with Instapaper API connection."""
        self.bookmark_limit = bookmark_limit
        self.current_index = 0
        self.instapaper_client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Instapaper client with credentials from .netrc."""
        try:
            secrets = netrc.netrc()
            login, _, password = secrets.authenticators('instapaper.com')
            consumerkey, _, consumersecret = secrets.authenticators('api.instapaper.com')
            self.instapaper_client = instapaper.Instapaper(consumerkey, consumersecret)
            self.instapaper_client.login(login, password)
        except (AttributeError, ValueError, RuntimeError, OSError, KeyError, FileNotFoundError) as e:
            print(f"Error initializing Instapaper client: {e}")
            raise
    
    def _get_bookmarks(self):
        """Get bookmarks with error handling."""
        try:
            return self.instapaper_client.bookmarks(limit=self.bookmark_limit)
        except (AttributeError, ValueError, RuntimeError, OSError) as e:
            print(f"Error fetching bookmarks: {e}")
            return None
    
    def slow_print(self, text, delay=0.05):
        """Prints strings slowly to the console."""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def read_title(self):
        """Reads the bookmark title."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return
            
        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            print(str(m.title))
        else:
            print("Current index is out of range.")

    def read_article(self):
        """Reads the content of the bookmark title."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return
            
        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            print(str(m.text))
        else:
            print("Current index is out of range.")

    def next_bookmark(self):
        """Navigates to the next bookmark."""
        marks = self._get_bookmarks()
        if marks and self.current_index < len(marks) - 1:
            self.current_index += 1
            return True
        print("Already at the last bookmark.")
        return False

    def prev_bookmark(self):
        """Navigates to the previous bookmark."""
        if self.current_index > 0:
            self.current_index -= 1
            return True
        print("Already at the first bookmark.")
        return False

    def first_bookmark(self):
        """Navigates to the first bookmark."""
        marks = self._get_bookmarks()
        if marks:
            self.current_index = 0
            return True
        print("No bookmarks found.")
        return False

    def last_bookmark(self):
        """Navigates to the last bookmark."""
        marks = self._get_bookmarks()
        if marks:
            self.current_index = len(marks) - 1
            return True
        print("No bookmarks found.")
        return False

    def show_bookmarks(self):
        """Displays a list of all bookmarks."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return
        for m in marks:
            print(f"{m.title}")

    def delete_bookmark(self):
        """Deletes the currently selected bookmark."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return False
            
        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            confirmation = input(
                f"Are you sure you want to delete '{m.title}'? (y/N): "
            ).strip().lower()
            if confirmation == 'y' or confirmation == 'yes':
                m.delete()
                print(f"Bookmark '{m.title}' deleted.")
                return True
            else:
                print("Deletion cancelled.")
                return False
        else:
            print("Current index is out of range.")
            return False

    def star_bookmark(self):
        """Stars the currently selected bookmark."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return False
            
        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            try:
                m.star()
                print(f"Bookmark '{m.title}' starred successfully.")
                return True
            except (AttributeError, ValueError, RuntimeError, OSError) as e:
                print(f"Error starring bookmark: {e}")
                return False
        else:
            print("Current index is out of range.")
            return False

    def add_bookmark(self):
        """Adds a new bookmark."""
        url = input("Enter the URL to bookmark: ").strip()
        if url:
            try:
                self.instapaper_client.add_bookmark(url)
                print(f"Bookmark added successfully: {url}")
                return True
            except (AttributeError, ValueError, RuntimeError, OSError) as e:
                print(f"Error adding bookmark: {e}")
                return False
        else:
            print("No URL entered. Bookmark not added.")
            return False

    def create_highlight(self):
        """Creates a highlight for the current bookmark."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return False

        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            print(f"Creating highlight for: {m.title}")
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

            if highlight_text:
                try:
                    # Create the highlight using the instapaper create_highlight method
                    m.create_highlight(highlight_text)
                    print("Highlight created successfully!")
                    ellipsis = '...' if len(highlight_text) > 100 else ''
                    print(f"Highlighted text: {highlight_text[:100]}{ellipsis}")
                    return True
                except (AttributeError, ValueError, RuntimeError, OSError) as e:
                    print(f"Error creating highlight: {e}")
                    return False
            else:
                print("No text entered. Highlight cancelled.")
                return False
        else:
            print("Current index is out of range.")
            return False

    def archive_bookmark(self):
        """Archives the currently selected bookmark."""
        marks = self._get_bookmarks()
        if not marks:
            print("No bookmarks found.")
            return False

        if 0 <= self.current_index < len(marks):
            m = marks[self.current_index]
            try:
                m.archive()
                print(f"Bookmark '{m.title}' archived successfully.")
                return True
            except (AttributeError, ValueError, RuntimeError, OSError) as e:
                print(f"Error archiving bookmark: {e}")
                return False
        else:
            print("Current index is out of range.")
            return False

    def run(self):
        """Main method to run the interactive console."""
        print("Welcome to the Instapaper Console App!")
        print("Type 'bookmarks' to list bookmarks, 'add' to add a bookmark, "
              "'delete' to delete current bookmark, 'star' to star current bookmark, "
              "'highlight' to create a highlight, 'archive' to archive current bookmark, "
              "or 'exit' to quit.")
        print("Navigation: 'title', 'next', 'prev', 'first', 'last', 'read'")

        # Display the current bookmark title at startup
        self.read_title()

        while True:
            cmd = input('> ').strip().lower()
            if cmd == 'exit':
                print("Goodbye!")
                break
            elif cmd == 'bookmarks':
                self.show_bookmarks()
            elif cmd == 'add':
                self.add_bookmark()
            elif cmd == 'delete':
                self.delete_bookmark()
            elif cmd == 'star':
                self.star_bookmark()
            elif cmd == 'highlight':
                self.create_highlight()
            elif cmd == 'archive':
                self.archive_bookmark()
            elif cmd == 'title':
                self.read_title()
            elif cmd == 'next':
                if self.next_bookmark():
                    self.read_title()
            elif cmd == 'previous' or cmd == 'prev':
                if self.prev_bookmark():
                    self.read_title()
            elif cmd == 'first':
                if self.first_bookmark():
                    self.read_title()
            elif cmd == 'last':
                if self.last_bookmark():
                    self.read_title()
            elif cmd == 'read':
                self.read_article()
            else:
                print("Unknown command. Try 'bookmarks', 'add', 'delete', 'star', "
                      "'highlight', 'archive', 'title', 'next', 'prev', 'first', "
                      "'last', 'read', or 'exit'.")