# Instapaper Reader Console App

A Python console application for reading and managing Instapaper bookmarks.

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
- `bookmarks` - List all bookmarks
- `add` - Add a new bookmark
- `title` - Show current bookmark title
- `next` - Move to next bookmark
- `prev` / `previous` - Move to previous bookmark
- `first` - Jump to first bookmark
- `last` - Jump to last bookmark
- `read` - Read current bookmark content
- `exit` - Quit the application

## Dependencies

- `instapaper==0.5` - Instapaper API client
- `oauth2==1.9.0.post1` - OAuth authentication
- `httplib2==0.31.0` - HTTP client library