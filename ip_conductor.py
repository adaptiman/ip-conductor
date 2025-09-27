"""A simple console application to interact with Instapaper bookmarks."""

import time
import netrc
import instapaper

def slow_print(text, delay=0.05):
    """Prints strings slowly to the console."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def read_title(i, current_index):
    """Reads the bookmark title."""
    marks = i.bookmarks()
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            #slow_print(str(m.title))
            print(str(m.title))
        else:
            print("Current index is out of range.")
    else:
        print("No bookmarks found.")

def read_article(i, current_index):
    """Reads the content of the bookmark title."""
    marks = i.bookmarks()
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            #slow_print(str(m.text))
            print(str(m.text))
        else:
            print("Current index is out of range.")
    else:
        print("No bookmarks found.")

def next_bookmark(i, current_index):
    """Navigates to the next bookmark."""
    marks = i.bookmarks()
    if marks and current_index < len(marks) - 1:
        return current_index + 1
    print("Already at the last bookmark.")
    return current_index

def prev_bookmark(current_index):
    """Navigates to the previous bookmark."""
    if current_index > 0:
        return current_index - 1
    print("Already at the first bookmark.")
    return current_index

def first_bookmark(i):
    """Navigates to the first bookmark."""
    marks = i.bookmarks()
    if marks:
        return 0
    print("No bookmarks found.")
    return 0

def last_bookmark(i):
    """Navigates to the last bookmark."""
    marks = i.bookmarks()
    if marks:
        return len(marks) - 1
    print("No bookmarks found.")
    return 0

def show_bookmarks(i):
    """Displays a list of all bookmarks."""
    marks = i.bookmarks()
    for m in marks:
        print(f"{m.title}")

def delete_bookmark(i, current_index):
    """Deletes the currently selected bookmark."""
    marks = i.bookmarks()
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            confirmation = input(f"Are you sure you want to delete '{m.title}'? (y/N): ").strip().lower()
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
    else:
        print("No bookmarks found.")
        return False

def tag_bookmark(i, current_index):
    """Tags the currently selected bookmark with the 'Review' tag."""
    marks = i.bookmarks()
    if marks:
        if 0 <= current_index < len(marks):
            m = marks[current_index]
            try:
                m.add_tag("Review")
                print(f"Bookmark '{m.title}' tagged with 'Review'.")
                return True
            except Exception as e:
                print(f"Error tagging bookmark: {e}")
                return False
        else:
            print("Current index is out of range.")
            return False
    else:
        print("No bookmarks found.")
        return False

def add_bookmark(i):
    """Adds a new bookmark."""
    url = input('Enter URL to add: ').strip()
    # Uncomment and adjust if instapaper.Bookmark works as expected
    b = instapaper.Bookmark(i, {"url": url})
    b.save()
    print(f"Bookmark for {url} added.")

def main():
    """Main function to run the Instapaper console app."""
    # This is the login block where we authenticate with Instapaper
    # and create an Instapaper instance.
    secrets = netrc.netrc()
    login, _, password = secrets.authenticators('instapaper.com')
    consumerkey, _, consumersecret = secrets.authenticators('api.instapaper.com')
    i = instapaper.Instapaper(consumerkey, consumersecret)
    i.login(login, password)

    # Here begins the interactive console
    print("Welcome to the Instapaper Console App!")
    print("Type 'bookmarks' to list bookmarks, 'add' to add a bookmark, 'delete' to delete current bookmark, 'tag' to tag current bookmark, or 'exit' to quit.")
    print("Navigation: 'title', 'next', 'prev', 'first', 'last', 'read'")
    current_index = 0
    
    # Display the current bookmark title at startup
    #print("\nCurrent bookmark:")
    read_title(i, current_index)
    
    while True:
        cmd = input('> ').strip().lower()
        if cmd == 'exit':
            print("Goodbye!")
            break
        elif cmd == 'bookmarks':
            show_bookmarks(i)
        elif cmd == 'add':
            add_bookmark(i)
        elif cmd == 'delete':
            delete_bookmark(i, current_index)
        elif cmd == 'tag':
            tag_bookmark(i, current_index)
        elif cmd == 'title':
            read_title(i, current_index)
        elif cmd == 'next':
            current_index = next_bookmark(i, current_index)
            read_title(i, current_index)
        elif cmd == 'previous' or cmd == 'prev':
            current_index = prev_bookmark(current_index)
            read_title(i, current_index)
        elif cmd == 'first':
            current_index = first_bookmark(i)
            read_title(i, current_index)
        elif cmd == 'last':
            current_index = last_bookmark(i)
            read_title(i, current_index)
        elif cmd == 'read':
            read_article(i, current_index)
        else:
            print("Unknown command. Try 'bookmarks', 'add', 'delete', 'tag', 'title', 'next', 'prev', "
                  "'first', 'last', 'read', or 'exit'.")

if __name__ == "__main__":
    main()
