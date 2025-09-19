# SyncMark - Application Unifiée

## Vue d'ensemble

Cette version unifiée de SyncMark consolide toutes les fonctionnalités précédemment réparties en trois exécutables distincts (`SyncMarkHost.exe`, `SyncMarkSettings.exe`, `SyncMarkDaemon.exe`) en une seule application polyvalente.

## Avantages de l'Application Unifiée

✅ **Simplicité de déploiement** : Un seul fichier exécutable à distribuer  
✅ **Maintenance facilitée** : Une seule base de code à maintenir  
✅ **Réduction de l'espace disque** : Élimination des redondances  
✅ **Configuration centralisée** : Gestion unifiée des paramètres  
✅ **Installation simplifiée** : Processus d'installation en une étape  

## Modes de Fonctionnement

L'application unifiée `SyncMark.exe` peut fonctionner dans différents modes selon les arguments fournis :

### 1. Mode Configuration (par défaut)
```bash
SyncMark.exe
# ou explicitement
SyncMark.exe --mode settings
```
Lance l'interface graphique de configuration permettant d'activer/désactiver la synchronisation.

### 2. Mode Native Host
```bash
SyncMark.exe --mode host
```
Fonctionne comme Native Host pour la communication avec l'extension Chrome. Ce mode est utilisé automatiquement par le navigateur.

### 3. Mode Installation
```bash
SyncMark.exe --mode install
# ou avec un ID d'extension spécifique
SyncMark.exe --mode install --extension-id YOUR_EXTENSION_ID
```
Installe automatiquement le Native Host dans le registre Windows.

### 4. Mode Désinstallation
```bash
SyncMark.exe --mode uninstall
```
Supprime le Native Host du registre Windows.

## Architecture Technique

### Classes Principales

- **`SyncMarkConfig`** : Gestionnaire centralisé de la configuration
- **`NativeHostManager`** : Gestion de la communication avec Chrome
- **`SettingsUI`** : Interface graphique de configuration
- **`NativeHostInstaller`** : Installation/désinstallation automatique

### Fonctionnalités Intégrées

1. **Synchronisation des favoris** : Fusion intelligente entre favoris locaux et du navigateur
2. **Configuration persistante** : Sauvegarde automatique des paramètres
3. **Logging centralisé** : Journalisation unifiée dans `syncmark_unified.log`
4. **Gestion d'erreurs robuste** : Récupération automatique en cas d'erreur

## Installation et Déploiement

### Construction de l'Exécutable

1. **Préparation de l'environnement** :
   ```bash
   pip install pyinstaller
   ```

2. **Construction automatique** :
   ```bash
   python build_unified.py
   ```

3. **Construction manuelle** :
   ```bash
   pyinstaller SyncMarkUnified.spec --clean
   ```

### Déploiement

Après la construction, vous obtenez :
- `dist/SyncMark.exe` : L'exécutable principal
- `deployment_package/` : Package complet avec script d'installation

## Configuration des Fichiers

### Manifest Native Host (`native_host_manifest.json`)
```json
{
  "name": "com.syncmark.host",
  "description": "SyncMark Native Host",
  "path": "C:\\path\\to\\SyncMark.exe",
  "type": "stdio",
  "allowed_origins": [
    "chrome-extension://YOUR_EXTENSION_ID/"
  ]
}
```

### Configuration Utilisateur (`~/Documents/SyncMark/config.json`)
```json
{
  "enabled": true
}
```

## Utilisation

### Installation Initiale

1. **Copier l'exécutable** dans le répertoire souhaité
2. **Installer le Native Host** :
   ```bash
   SyncMark.exe --mode install --extension-id YOUR_EXTENSION_ID
   ```
3. **Configurer les paramètres** :
   ```bash
   SyncMark.exe --mode settings
   ```

### Utilisation Quotidienne

- L'application fonctionne automatiquement en arrière-plan
- Utilisez l'interface de configuration pour activer/désactiver la synchronisation
- Les logs sont disponibles dans `~/Documents/SyncMark/syncmark_unified.log`

## Dépannage

### Problèmes Courants

1. **Extension non reconnue** :
   - Vérifiez l'ID de l'extension dans le manifest
   - Réinstallez le Native Host avec le bon ID

2. **Synchronisation inactive** :
   - Vérifiez que la synchronisation est activée dans les paramètres
   - Consultez les logs pour identifier les erreurs

3. **Erreurs de permissions** :
   - Exécutez l'installation en tant qu'administrateur
   - Vérifiez les permissions du répertoire `~/Documents/SyncMark/`

### Logs et Diagnostic

Les logs sont automatiquement sauvegardés dans :
```
%USERPROFILE%\Documents\SyncMark\syncmark_unified.log
```

## Migration depuis la Version Multi-Exécutables

Si vous migrez depuis l'ancienne version avec trois exécutables :

1. **Arrêtez** tous les processus SyncMark existants
2. **Désinstallez** l'ancien Native Host si nécessaire
3. **Remplacez** les anciens exécutables par `SyncMark.exe`
4. **Réinstallez** le Native Host avec la nouvelle version
5. **Testez** la configuration avec l'interface

## Support et Contribution

Pour signaler des problèmes ou contribuer au développement :
- Consultez les logs pour identifier les erreurs
- Vérifiez la configuration des manifests
- Testez les différents modes de fonctionnement

---

*Cette version unifiée représente une évolution majeure de SyncMark, offrant une expérience utilisateur simplifiée tout en conservant toutes les fonctionnalités essentielles.*