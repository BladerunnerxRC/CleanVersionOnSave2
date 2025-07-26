import os
import json
import time
import traceback

# Resolve the path to the history file (sibling “data” folder)
HISTORY_FILE = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', 'data', 'rename_history.json')
)

def log_rename(old_name: str, new_name: str, trigger: str) -> None:
    """
    Append a rename event to the history JSON file.
    
    old_name : previous document name
    new_name : cleaned document name
    trigger  : what caused the rename (e.g. 'autosave', 'export', 'manual')
    """
    entry = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'old_name': old_name,
        'new_name': new_name,
        'trigger': trigger
    }
    try:
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception as e:
        log_error(f"Failed to write rename history: {e}")

def log_error(message: str) -> None:
    """
    Log an error message to the console.
    You could extend this to write to a separate error log file.
    """
    # Print to Fusion’s console
    print(f"[CleanVersionOnSave2 Error] {message}")
    # Optionally write the stack trace too:
    traceback.print_exc()
