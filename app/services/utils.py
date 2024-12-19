from datetime import datetime

def log_error(file_name: str, message: str) -> None:
    """
    Log error messages with timestamp to errors.log file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_name, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")
