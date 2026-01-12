import sys
import os

def parse_mirror_list(filepath):
    """Parses the mirror-list.txt file into pending and complete lists."""
    pending = []
    complete = []
    current_section = None
    
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    with open(filepath, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line == '[pending]':
            current_section = 'pending'
        elif line == '[complete]':
            current_section = 'complete'
        elif current_section == 'pending':
            pending.append(line)
        elif current_section == 'complete':
            complete.append(line)
            
    return pending, complete

def get_pending_images(filepath):
    pending, _ = parse_mirror_list(filepath)
    for img in pending:
        print(img)

def move_to_complete(filepath, success_images):
    """Moves successfully synced images from pending to complete section."""
    pending, complete = parse_mirror_list(filepath)
    
    # Filter out success_images from pending and add to complete
    new_pending = [img for img in pending if img not in success_images]
    
    # Avoid duplicates in complete
    existing_complete_set = set(complete)
    for img in success_images:
        if img not in existing_complete_set:
            complete.append(img)
            
    # Rewrite the file
    with open(filepath, 'w') as f:
        f.write("[pending]\n")
        for img in new_pending:
            f.write(f"{img}\n")
        
        f.write("\n[complete]\n")
        for img in complete:
            f.write(f"{img}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_list.py [get_pending | move_to_complete <image1> <image2> ...]")
        sys.exit(1)

    command = sys.argv[1]
    filepath = "mirror-list.txt"

    if command == "get_pending":
        get_pending_images(filepath)
    elif command == "move_to_complete":
        success_images = sys.argv[2:]
        if success_images:
            move_to_complete(filepath, success_images)
            print(f"Moved {len(success_images)} images to [complete] section.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
