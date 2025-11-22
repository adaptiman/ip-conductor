# Instapaper Reader Console App

A Python console application for reading and managing Instapaper articles.

## Architecture

The application is built with a modular design:

- **`article_manager.py`** - Contains the `ArticleManager` class with all Instapaper functionality
- **`ip_conductor.py`** - Console interface that uses the `ArticleManager` class
- **`example_usage.py`** - Demonstrates how to use `ArticleManager` in other programs

This design allows you to easily integrate Instapaper functionality into other Python applications by importing the `ArticleManager` class.

## Setup

### Prerequisites
- Python 3.12 or higher
- pip and venv

### Installation

1. Clone or download this repository:
   ```bash
   cd /path/to/ip-conductor
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

3. Activate the virtual environment:
   ```bash
   source .venv/bin/activate  # On Linux/macOS/WSL
   # or
   .venv\Scripts\activate     # On Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Instapaper credentials:
   ```bash
   INSTAPAPER_USERNAME=your_email@example.com
   INSTAPAPER_PASSWORD=your_password
   INSTAPAPER_CONSUMER_KEY=your_consumer_key
   INSTAPAPER_CONSUMER_SECRET=your_consumer_secret
   ```

**Note**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

Activate the virtual environment (if not already active):
```bash
source .venv/bin/activate
```

Run the application:
```bash
python ip_conductor.py
```

### Available Commands

#### Article Management
- `articles` / `bookmarks` - List all articles with numbers (up to 25 by default)
- `add` - Add a new article by entering a URL
- `delete` - Delete the currently selected article (with confirmation)
- `star` - Star the currently selected article
- `archive` - Archive the currently selected article
- `highlight` - Create a highlight for the current article (multi-line text input)

#### Navigation
- `title` - Show current article title
- `<number>` - Navigate to article by number and display its title (e.g., `5` jumps to article 5)
- `next` - Move to next article
- `prev` / `previous` - Move to previous article
- `first` - Jump to first article
- `last` - Jump to last article
- `read` - Read current article content
- `read <number>` - Navigate to and read a specific article by its number from the list

#### System
- `exit` - Quit the application

### Features

- **Environment-based configuration**: Secure credential storage using `.env` files
- **Virtual environment support**: Isolated dependencies per project
- **Numbered article listing**: Articles are displayed with numbers for easy reference
- **Quick navigation**: Jump to any article by simply entering its number
- **Direct article access**: Jump to and read any article by its number
- **Configurable article limit**: The application fetches 25 articles by default (configurable in `ArticleManager` initialization)
- **Error handling**: Comprehensive error handling for network issues, API errors, and invalid operations
- **Interactive highlights**: Create multi-line highlights by entering text and pressing Enter twice to finish
- **Confirmation prompts**: Safe deletion with confirmation prompts

### Example Workflow

```bash
# Activate the virtual environment
source .venv/bin/activate

# Start the application
python ip_conductor.py

# List all articles with numbers
> articles
1. Understanding Python Decorators
2. Introduction to Machine Learning
3. Web Development Best Practices
4. Advanced Git Techniques
5. Docker for Beginners

# Quick jump to article 3 by entering just the number
> 3
Web Development Best Practices

# Read the current article (now article 3)
> read

# Or jump and read in one command
> read 5
[Displays content of "Docker for Beginners"]

# Navigate to next article
> next
[Now at article 6]

# Create a highlight
> highlight
Enter the text you want to highlight (press Enter twice to finish):
This is important text
that I want to remember.

# Star the article
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
- `python-dotenv==1.2.1` - Environment variable management
- `setuptools==80.9.0` - Python package utilities (required for Python 3.12+)

All dependencies are listed in `requirements.txt` and will be installed automatically.

## Customization

### Article Limit
To change the number of articles fetched, pass a different limit when creating the `ArticleManager` instance:

```python
# In ip_conductor.py main() function
manager = ArticleManager(bookmark_limit=50)  # Change from default 25 to 50
```

## Using ArticleManager in Other Programs

The `ArticleManager` class can be easily imported and used in other Python applications. Make sure your `.env` file is properly configured in your project directory.

```python
from article_manager import ArticleManager

# Create an instance
manager = ArticleManager(bookmark_limit=25)

# Get article information
title = manager.get_current_title()
article_text = manager.get_current_article()
article_list = manager.get_bookmarks_list()

# Navigate articles
manager.next_bookmark()
manager.prev_bookmark()
manager.first_bookmark()
manager.last_bookmark()

# Jump to a specific article by number (1-based)
manager.set_bookmark_by_number(5)

# Manage articles
success, url, error = manager.add_bookmark_url("https://example.com")
success, title, error = manager.star_current_bookmark()
success, title, error = manager.archive_current_bookmark()
success, title, error = manager.delete_current_bookmark()

# Create highlights
success, title, highlight, error = manager.create_highlight_for_current("Important text")

# Access the Instapaper client directly for advanced operations
bookmarks = manager.instapaper_client.bookmarks(limit=10)
```

See `example_usage.py` for a complete demonstration of using `ArticleManager` programmatically.

### Adding New Commands
The application is designed to be easily extensible. To add new commands:

1. Add a new method to the `ArticleManager` class in `article_manager.py`
2. Add error handling using try-except blocks with appropriate exception types
3. Add a command handler function in `ip_conductor.py` (following the pattern of existing handlers)
4. Add the command to the main command loop in the `run_console()` function
5. Update the help messages to include the new command

## VS Code Setup (WSL)

If you're using VS Code with WSL, the project includes VS Code settings in `.vscode/settings.json` that will:
- Automatically use the project's virtual environment
- Activate the venv when opening new terminals

This provides seamless integration without manual activation within VS Code.

## Troubleshooting

### Missing Environment Variables
If you see an error about missing environment variables, ensure:
1. Your `.env` file exists in the project root
2. All four required variables are set (USERNAME, PASSWORD, CONSUMER_KEY, CONSUMER_SECRET)
3. There are no extra spaces or quotes around the values

### Import Errors in WSL Terminal
If you get import errors when running from a WSL terminal outside VS Code:
```bash
cd /path/to/ip-conductor
source .venv/bin/activate
```

The virtual environment must be activated to access the installed packages.