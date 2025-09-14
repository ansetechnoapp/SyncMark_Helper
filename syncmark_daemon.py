import sys
import json
import os
import struct
import logging
import time

# --- Configuration ---
# Le démon va maintenant vérifier un fichier de configuration pour savoir s'il doit s'exécuter.
HOME_DIR = os.path.expanduser("~")
SYNC_DIR = os.path.join(HOME_DIR, 'Documents', 'SyncMark')
os.makedirs(SYNC_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(SYNC_DIR, 'config.json')
LOG_FILE = os.path.join(SYNC_DIR, 'native_host.log')
BOOKMARKS_FILE_PATH = os.path.join(SYNC_DIR, 'syncmark_bookmarks.json')

# --- Mise en place du logging ---
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_sync_enabled():
    """Vérifie le fichier de configuration pour voir si la synchronisation est activée."""
    try:
        if not os.path.exists(CONFIG_FILE):
            # Si le fichier n'existe pas, on l'active par défaut
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'enabled': True}, f)
            return True
        
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('enabled', False)
    except Exception as e:
        logging.error(f"Erreur lors de la lecture du fichier de configuration : {e}")
        return False

def get_message():
    """Lit un message depuis stdin, envoyé par l'extension du navigateur."""
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        logging.warning("Aucune longueur de message reçue. Sortie.")
        sys.exit(0)
    
    message_length = struct.unpack('@I', raw_length)[0]
    message_json = sys.stdin.buffer.read(message_length).decode('utf-8')
    logging.info(f"Message reçu de longueur {message_length}.")
    return json.loads(message_json)

def send_message(message_content):
    """Encode un message en JSON et l'envoie à stdout pour que l'extension le reçoive."""
    encoded_content = json.dumps(message_content).encode('utf-8')
    message_length = struct.pack('@I', len(encoded_content))
    
    sys.stdout.buffer.write(message_length)
    sys.stdout.buffer.write(encoded_content)
    sys.stdout.buffer.flush()
    logging.info("Message envoyé avec succès à l'extension.")

def main():
    """Fonction principale pour exécuter l'hôte natif."""
    
    # Première vérification : la synchronisation est-elle activée ?
    if not is_sync_enabled():
        logging.info("La synchronisation est désactivée dans le fichier de configuration. Le script ne fera rien.")
        # Il est important de quand même boucler pour ne pas fermer le canal de communication
        # avec le navigateur, mais sans traiter les messages.
        while True:
            time.sleep(60) # Attend simplement pour garder le processus en vie

    try:
        logging.info(f"Utilisation du fichier de favoris : {BOOKMARKS_FILE_PATH}")

        # 1. Obtenir les favoris envoyés par l'extension.
        message = get_message()
        extension_bookmarks = message.get('bookmarks', [])
        
        # 2. Lire les favoris locaux depuis le fichier s'il existe.
        local_bookmarks = []
        if os.path.exists(BOOKMARKS_FILE_PATH):
            try:
                with open(BOOKMARKS_FILE_PATH, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        local_bookmarks = json.loads(content)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Impossible de lire ou d'analyser le fichier de favoris local : {e}")

        # 3. Logique de fusion avancée
        merged_bookmarks_map = {bm['url']: bm for bm in local_bookmarks if 'url' in bm}
        merged_bookmarks_map.update({bm['url']: bm for bm in extension_bookmarks if 'url' in bm})
        
        synced_bookmarks = list(merged_bookmarks_map.values())
        logging.info(f"{len(local_bookmarks)} favoris locaux et {len(extension_bookmarks)} de l'extension fusionnés en {len(synced_bookmarks)} favoris uniques.")

        # 4. Sauvegarder la liste synchronisée dans le fichier local.
        with open(BOOKMARKS_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(synced_bookmarks, f, indent=4, ensure_ascii=False)
        logging.info("Favoris fusionnés enregistrés avec succès dans le fichier local.")

        # 5. Envoyer la liste complète et synchronisée à l'extension.
        send_message({'status': 'success', 'bookmarks': synced_bookmarks})

    except Exception as e:
        logging.error(f"Une erreur inattendue est survenue dans main : {e}", exc_info=True)
        send_message({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    main()
