# Instapaper Reader Console App

A Python console application for reading and managing Instapaper bookmarks.

## Architecture

The application is built with a modular design:

- **`article_manager.py`** - Contains the `ArticleManager` class with all Instapaper functionality
- **`ip_conductor.py`** - Console interface that uses the `ArticleManager` class  
- **`example_usage.py`** - Demonstrates how to use `ArticleManager` in other programs

This design allows you to easily integrate Instapaper functionality into other Python applications by importing the `ArticleManager` class.

## Setup

### Prerequisites
- Python 3.13 or higher
- Conda (recommended) or pip

### Installation

1. Clone or download this repository
2. Create a conda environment:
   ```bash
   conda create --name ipc python=3.13
   conda activate ipc
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Create a `.netrc` file in your home directory with your Instapaper credentials:

```
machine instapaper.com
login your_username
password your_password

machine api.instapaper.com
login your_consumer_key
password your_consumer_secret
```

## Usage

Run the application:
```bash
python ip_conductor.py
```

### Available Commands

#### Bookmark Management
- `bookmarks` - List all bookmarks (up to 25 by default)
- `add` - Add a new bookmark by entering a URL
- `delete` - Delete the currently selected bookmark (with confirmation)
- `star` - Star the currently selected bookmark
- `archive` - Archive the currently selected bookmark
- `highlight` - Create a highlight for the current bookmark (multi-line text input)

#### Navigation
- `title` - Show current bookmark title
- `next` - Move to next bookmark
- `prev` / `previous` - Move to previous bookmark
- `first` - Jump to first bookmark
- `last` - Jump to last bookmark
- `read` - Read current bookmark content

#### System
- `exit` - Quit the application

### Features

- **Configurable bookmark limit**: The application fetches 25 bookmarks by default (configurable via `BOOKMARK_LIMIT` constant)
- **Error handling**: Comprehensive error handling for network issues, API errors, and invalid operations
- **Interactive highlights**: Create multi-line highlights by entering text and pressing Enter twice to finish
- **Confirmation prompts**: Safe deletion with confirmation prompts

### Example Workflow

```bash
# Start the application
python ip_conductor.py

# List all bookmarks
> bookmarks

# Navigate to a specific bookmark
> first
> next

# Read the current bookmark
> read

# Create a highlight
> highlight
Enter the text you want to highlight (press Enter twice to finish):
This is important text
that I want to remember.

# Star the bookmark
> star

# Archive when done
> archive

# Exit
> exit
```

## Dependencies

- `instapaper==0.5` - Instapaper API client
- `oauth2==1.9.0.post1` - OAuth authentication
- `httplib2==0.31.0` - HTTP client library

## Customization

### Bookmark Limit
To change the number of bookmarks fetched, modify the `BOOKMARK_LIMIT` constant at the top of `ip_conductor.py`:

```python
# Global configuration
BOOKMARK_LIMIT = 50  # Change from default 25 to 50
```

## Using ArticleManager in Other Programs

The `ArticleManager` class can be easily imported and used in other Python applications:

```python
from article_manager import ArticleManager

# Create an instance
manager = ArticleManager(bookmark_limit=25)

# Use the methods programmatically
manager.read_title()           # Print current bookmark title
manager.next_bookmark()       # Navigate to next bookmark
manager.show_bookmarks()      # Display all bookmarks
manager.add_bookmark()        # Add a new bookmark (interactive)

# Access the Instapaper client directly for advanced operations
bookmarks = manager.instapaper_client.bookmarks(limit=10)
```

See `example_usage.py` for a complete demonstration of using `ArticleManager` programmatically.

### Adding New Commands
The application is designed to be easily extensible. To add new commands:

1. Add a new method to the `ArticleManager` class in `article_manager.py`
2. Add error handling using the established exception types
3. Add the command to the main command loop in the `run()` method
4. Update the help messages to include the new command