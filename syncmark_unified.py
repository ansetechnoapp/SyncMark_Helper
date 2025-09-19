#!/usr/bin/env python3
"""
SyncMark - Application Unifiée
Consolide toutes les fonctionnalités de SyncMark en une seule application :
- Native Host pour communication avec l'extension Chrome
- Interface de configuration
- Service d'arrière-plan
- Installation automatique du Native Host
"""

import sys
import json
import os
import struct
import logging
import time
import threading
import argparse
import tkinter as tk
from tkinter import messagebox
import winreg
from pathlib import Path

# --- Configuration Globale ---
HOME_DIR = os.path.expanduser("~")
SYNC_DIR = os.path.join(HOME_DIR, 'Documents', 'SyncMark')
os.makedirs(SYNC_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(SYNC_DIR, 'config.json')
LOG_FILE = os.path.join(SYNC_DIR, 'syncmark_unified.log')
BOOKMARKS_FILE_PATH = os.path.join(SYNC_DIR, 'syncmark_bookmarks.json')

# --- Configuration du Logging ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SyncMarkConfig:
    """Gestionnaire de configuration centralisé"""
    
    @staticmethod
    def is_sync_enabled():
        """Vérifie si la synchronisation est activée"""
        try:
            if not os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump({'enabled': True}, f)
                return True
            
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('enabled', False)
        except Exception as e:
            logging.error(f"Erreur lors de la lecture de la configuration : {e}")
            return False
    
    @staticmethod
    def set_sync_enabled(enabled):
        """Active ou désactive la synchronisation"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump({'enabled': enabled}, f, indent=4)
            return True
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la configuration : {e}")
            return False

class NativeHostManager:
    """Gestionnaire du Native Host pour communication avec Chrome"""
    
    def __init__(self):
        self.running = False
    
    def get_message(self):
        """Lit un message depuis stdin"""
        raw_length = sys.stdin.buffer.read(4)
        if not raw_length:
            return None
        
        message_length = struct.unpack('@I', raw_length)[0]
        message_json = sys.stdin.buffer.read(message_length).decode('utf-8')
        logging.info(f"Message reçu de longueur {message_length}")
        return json.loads(message_json)
    
    def send_message(self, message_content):
        """Envoie un message à stdout"""
        encoded_content = json.dumps(message_content).encode('utf-8')
        message_length = struct.pack('@I', len(encoded_content))
        
        sys.stdout.buffer.write(message_length)
        sys.stdout.buffer.write(encoded_content)
        sys.stdout.buffer.flush()
        logging.info("Message envoyé à l'extension")
    
    def process_bookmarks(self, message):
        """Traite la synchronisation des favoris"""
        extension_bookmarks = message.get('bookmarks', [])
        
        local_bookmarks = []
        if os.path.exists(BOOKMARKS_FILE_PATH):
            try:
                with open(BOOKMARKS_FILE_PATH, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content:
                        local_bookmarks = json.loads(content)
            except (IOError, json.JSONDecodeError) as e:
                logging.error(f"Erreur lecture favoris locaux : {e}")
                self.send_message({
                    'status': 'error',
                    'message': 'Could not read local bookmarks file'
                })
                return
        
        # Fusion des favoris
        merged_bookmarks_map = {bm['url']: bm for bm in local_bookmarks if 'url' in bm}
        merged_bookmarks_map.update({bm['url']: bm for bm in extension_bookmarks if 'url' in bm})
        
        synced_bookmarks = list(merged_bookmarks_map.values())
        logging.info(f"Fusion : {len(local_bookmarks)} locaux + {len(extension_bookmarks)} extension = {len(synced_bookmarks)} uniques")
        
        # Sauvegarde
        try:
            with open(BOOKMARKS_FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump(synced_bookmarks, f, indent=4, ensure_ascii=False)
            logging.info("Favoris sauvegardés")
        except IOError as e:
            logging.error(f"Erreur sauvegarde favoris : {e}")
            self.send_message({
                'status': 'error',
                'message': 'Could not write bookmarks file'
            })
            return
        
        self.send_message({'status': 'success', 'bookmarks': synced_bookmarks})
    
    def run_host(self):
        """Boucle principale du Native Host"""
        logging.info("Native Host SyncMark démarré")
        self.running = True
        
        while self.running:
            try:
                message = self.get_message()
                
                if message is None:
                    logging.info("Canal fermé par le navigateur")
                    break
                
                if SyncMarkConfig.is_sync_enabled():
                    logging.info("Synchronisation activée - traitement du message")
                    self.process_bookmarks(message)
                else:
                    logging.info("Synchronisation désactivée")
                    self.send_message({
                        'status': 'disabled',
                        'message': 'Sync is disabled by user'
                    })
                    
            except Exception as e:
                logging.error(f"Erreur dans la boucle principale : {e}", exc_info=True)
                try:
                    self.send_message({'status': 'error', 'message': str(e)})
                except:
                    pass
                break
    
    def stop(self):
        """Arrête le Native Host"""
        self.running = False

class SettingsUI:
    """Interface graphique de configuration"""
    
    def __init__(self, root=None):
        if root is None:
            self.root = tk.Tk()
            self.own_root = True
        else:
            self.root = root
            self.own_root = False
            
        self.setup_window()
        self.sync_enabled = tk.BooleanVar()
        self.load_config()
        self.create_widgets()
    
    def setup_window(self):
        """Configure la fenêtre principale"""
        self.root.title("SyncMark - Paramètres")
        
        window_width = 400
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)
    
    def load_config(self):
        """Charge la configuration actuelle"""
        try:
            self.sync_enabled.set(SyncMarkConfig.is_sync_enabled())
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger la configuration :\n{e}")
            self.sync_enabled.set(False)
    
    def save_config(self):
        """Sauvegarde la configuration"""
        if SyncMarkConfig.set_sync_enabled(self.sync_enabled.get()):
            logging.info(f"Configuration sauvegardée : sync_enabled = {self.sync_enabled.get()}")
        else:
            messagebox.showerror("Erreur", "Impossible de sauvegarder la configuration")
    
    def create_widgets(self):
        """Crée l'interface utilisateur"""
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(
            main_frame,
            text="SyncMark - Configuration",
            font=('Helvetica', 14, 'bold')
        )
        title_label.pack(pady=(0, 15))
        
        desc_label = tk.Label(
            main_frame,
            text="Contrôlez la synchronisation de vos favoris entre\nvotre navigateur et votre système local.",
            wraplength=350,
            justify=tk.CENTER
        )
        desc_label.pack(pady=(0, 15))
        
        checkbox = tk.Checkbutton(
            main_frame,
            text="Activer la synchronisation en arrière-plan",
            variable=self.sync_enabled,
            command=self.save_config,
            font=('Helvetica', 10, 'bold')
        )
        checkbox.pack(pady=10)
        
        # Bouton pour fermer
        if self.own_root:
            close_button = tk.Button(
                main_frame,
                text="Fermer",
                command=self.root.quit,
                width=10
            )
            close_button.pack(pady=(15, 0))
    
    def run(self):
        """Lance l'interface graphique"""
        if self.own_root:
            self.root.mainloop()

class NativeHostInstaller:
    """Gestionnaire d'installation du Native Host"""
    
    @staticmethod
    def install_manifest(extension_id=None):
        """Installe le manifest Native Host dans le registre Windows"""
        print("🔧 Installation du Native Host SyncMark...")
        
        # Chemin du manifest
        manifest_path = Path(__file__).parent / "native_host_manifest.json"
        
        if not manifest_path.exists():
            print("❌ Fichier native_host_manifest.json non trouvé")
            return False
        
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception as e:
            print(f"❌ Erreur lecture manifest: {e}")
            return False
        
        # Mise à jour de l'ID d'extension si fourni
        if extension_id:
            manifest["allowed_origins"] = [f"chrome-extension://{extension_id}/"]
            print(f"✅ ID d'extension configuré: {extension_id}")
        
        # Mise à jour du chemin de l'exécutable
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
        manifest["path"] = exe_path.replace('\\', '\\\\')
        
        # Création du manifest temporaire
        temp_manifest_path = Path(__file__).parent / "temp_manifest.json"
        try:
            with open(temp_manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=2)
        except Exception as e:
            print(f"❌ Erreur création manifest temporaire: {e}")
            return False
        
        # Installation dans le registre
        try:
            registry_key = r"SOFTWARE\Google\Chrome\NativeMessagingHosts\com.syncmark.host"
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, str(temp_manifest_path))
            
            print("✅ Native Host installé avec succès")
            
            # Nettoyage
            try:
                temp_manifest_path.unlink()
            except:
                pass
                
            return True
            
        except Exception as e:
            print(f"❌ Erreur installation registre: {e}")
            return False
    
    @staticmethod
    def uninstall_manifest():
        """Désinstalle le manifest du registre"""
        try:
            registry_key = r"SOFTWARE\Google\Chrome\NativeMessagingHosts\com.syncmark.host"
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, registry_key)
            print("✅ Native Host désinstallé")
            return True
        except FileNotFoundError:
            print("ℹ️ Native Host n'était pas installé")
            return True
        except Exception as e:
            print(f"❌ Erreur désinstallation: {e}")
            return False

def main():
    """Fonction principale avec gestion des arguments"""
    parser = argparse.ArgumentParser(description='SyncMark - Application Unifiée')
    parser.add_argument('--mode', choices=['host', 'settings', 'install', 'uninstall'], 
                       default='settings', help='Mode de fonctionnement')
    parser.add_argument('--extension-id', help='ID de l\'extension Chrome pour l\'installation')
    
    args = parser.parse_args()
    
    if args.mode == 'host':
        # Mode Native Host
        host_manager = NativeHostManager()
        host_manager.run_host()
        
    elif args.mode == 'settings':
        # Mode Interface de configuration
        settings_ui = SettingsUI()
        settings_ui.run()
        
    elif args.mode == 'install':
        # Mode Installation
        success = NativeHostInstaller.install_manifest(args.extension_id)
        sys.exit(0 if success else 1)
        
    elif args.mode == 'uninstall':
        # Mode Désinstallation
        success = NativeHostInstaller.uninstall_manifest()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()