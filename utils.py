def smart_open(filepath, mode='r', encodings=None):
    """
    Tries to open a file with multiple encodings until one works.
    Returns the opened file as a list of lines.
    """
    if encodings is None:
        encodings = ['utf-8', 'utf-16', 'latin1', 'windows-1252']

    last_exception = None
    for enc in encodings:
        try:
            with open(filepath, mode, encoding=enc) as f:
                return f.readlines()
        except UnicodeDecodeError as e:
            last_exception = e
            continue

    raise UnicodeDecodeError(
        f"Failed to decode {filepath} with tried encodings: {encodings}. "
        f"Last error: {str(last_exception)}"
    )



def detect_experiment_type(filepath):
    lines = smart_open(filepath)
    for line in lines:
        if line.startswith("TAG"):
            return line.split('\t')[1].strip().upper()
    return "UNKNOWN"

