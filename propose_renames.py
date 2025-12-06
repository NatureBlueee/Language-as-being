import os
import re
import sys

log_path = r"d:\Profolio\Language-as-being\renames_log.txt"

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

# Clear log
with open(log_path, "w", encoding="utf-8") as f:
    f.write("Starting script...\n")

directory = r"d:\Profolio\Language-as-being\Thesis"

def clean_filename(title):
    # Remove invalid filename characters
    cleaned = re.sub(r'[\\/*?:"<>|]', "", title)
    # Replace newlines/tabs with spaces
    cleaned = " ".join(cleaned.split())
    # Limit length just in case
    return cleaned[:200]

def get_title(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for _ in range(20):
                line = f.readline()
                if not line:
                    break
                stripped = line.strip()
                if not stripped:
                    continue
                
                if stripped.startswith('# '):
                    return stripped[2:].strip()
                
    except Exception as e:
        return None
    
    try:
         with open(filepath, 'r', encoding='utf-8') as f:
            for _ in range(10):
                line = f.readline()
                if line.strip():
                    return line.strip()
    except:
        pass
    return "Untitled"

files = [f for f in os.listdir(directory) if f.endswith('.md')]

log(f"Found {len(files)} markdown files.")

for filename in files:
    filepath = os.path.join(directory, filename)
    title = get_title(filepath)
    if title:
        new_name = clean_filename(title) + ".md"
        if new_name != filename:
            log(f"RENAME: '{filename}' -> '{new_name}'")
        else:
            log(f"KEEP: '{filename}'")
    else:
        log(f"SKIP: '{filename}' (No title found)")
