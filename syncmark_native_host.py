import sys
import json
import os
import struct
import logging

# --- Setup Logging ---
# It's better to log to a file for debugging native messaging hosts
# because stdout/stderr are used for communication with the extension.
home_dir = os.path.expanduser("~")
sync_dir = os.path.join(home_dir, 'Documents', 'SyncMark')
os.makedirs(sync_dir, exist_ok=True)
# The log file will be created in Documents/SyncMark/native_host.log
logging.basicConfig(filename=os.path.join(sync_dir, 'native_host.log'), level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_message():
    """
    Reads a message from stdin, sent by the browser extension.
    The first 4 bytes represent the message length.
    """
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        logging.warning("Received no message length. Exiting.")
        sys.exit(0)
    
    message_length = struct.unpack('@I', raw_length)[0]
    message_json = sys.stdin.buffer.read(message_length).decode('utf-8')
    logging.info(f"Received message of length {message_length}.")
    return json.loads(message_json)

def send_message(message_content):
    """
    Encodes a message as JSON and sends it to stdout for the extension to receive.
    Prepends the message with a 4-byte length.
    """
    encoded_content = json.dumps(message_content).encode('utf-8')
    message_length = struct.pack('@I', len(encoded_content))
    
    sys.stdout.buffer.write(message_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()
    logging.info("Successfully sent message to extension.")

def main():
    """
    Main function to run the native host.
    """
    try:
        # Define the path for the local bookmarks backup file.
        bookmarks_file_path = os.path.join(sync_dir, 'syncmark_bookmarks.json')
        logging.info(f"Using bookmarks file at: {bookmarks_file_path}")

        # 1. Get bookmarks sent by the browser extension.
        message = get_message()
        extension_bookmarks = message.get('bookmarks', [])
        
        # 2. Read local bookmarks from the file if it exists.
        local_bookmarks = []
        if os.path.exists(bookmarks_file_path):
            try:
                with open(bookmarks_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Ensure file is not empty before trying to parse JSON
                    if content:
                        local_bookmarks = json.loads(content)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Could not read or parse local bookmarks file: {e}")
                # Proceed with an empty list if the file is corrupted or unreadable.

        # 3. Advanced Merge Logic
        # This logic combines both lists and removes duplicates based on the 'url' field.
        # It creates a dictionary where keys are bookmark URLs and values are bookmark objects.
        # This ensures each URL is unique in the final list.
        merged_bookmarks_map = {}

        # First, add all local bookmarks to the map.
        for bm in local_bookmarks:
            if 'url' in bm:
                merged_bookmarks_map[bm['url']] = bm
        
        # Then, add/update with bookmarks from the extension.
        # If a URL already exists, it will be updated with the version from the extension.
        for bm in extension_bookmarks:
            if 'url' in bm:
                merged_bookmarks_map[bm['url']] = bm
        
        # Convert the dictionary's values back into a list for the final result.
        synced_bookmarks = list(merged_bookmarks_map.values())
        logging.info(f"Merged {len(local_bookmarks)} local and {len(extension_bookmarks)} extension bookmarks into {len(synced_bookmarks)} unique bookmarks.")

        # 4. Save the fully synchronized list back to the local file.
        with open(bookmarks_file_path, 'w', encoding='utf-8') as f:
            # Use indent for readability and ensure_ascii=False for special characters.
            json.dump(synced_bookmarks, f, indent=4, ensure_ascii=False)
        logging.info("Successfully saved merged bookmarks to local file.")

        # 5. Send the complete, synchronized list back to the extension.
        send_message({'status': 'success', 'bookmarks': synced_bookmarks})

    except Exception as e:
        # If any unexpected error occurs, log it and inform the extension.
        logging.error(f"An unexpected error occurred in main: {e}", exc_info=True)
        send_message({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    main()
