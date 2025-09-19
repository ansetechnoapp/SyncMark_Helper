#!/usr/bin/env python3
"""
Script de construction pour SyncMark Unifié
Automatise la compilation et la préparation de l'application unifiée
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def clean_build_directories():
    """Nettoie les répertoires de build précédents"""
    print("🧹 Nettoyage des répertoires de build...")
    
    directories_to_clean = ['build', 'dist/__pycache__']
    files_to_clean = ['temp_manifest.json']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            try:
                shutil.rmtree(directory)
                print(f"   ✅ Supprimé: {directory}")
            except Exception as e:
                print(f"   ⚠️ Impossible de supprimer {directory}: {e}")
    
    for file in files_to_clean:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"   ✅ Supprimé: {file}")
            except Exception as e:
                print(f"   ⚠️ Impossible de supprimer {file}: {e}")

def check_dependencies():
    """Vérifie que les dépendances nécessaires sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = ['pyinstaller']
    missing_packages = []
    
    for package in required_packages:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'show', package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {package} installé")
            else:
                missing_packages.append(package)
                print(f"   ❌ {package} manquant")
        except Exception as e:
            missing_packages.append(package)
            print(f"   ❌ {package} manquant (erreur: {e})")
    
    if missing_packages:
        print(f"\n❌ Packages manquants: {', '.join(missing_packages)}")
        print("Installez-les avec: pip install " + " ".join(missing_packages))
        return False
    
    return True

def build_unified_executable():
    """Compile l'application unifiée avec PyInstaller"""
    print("🔨 Compilation de l'application unifiée...")
    
    spec_file = "SyncMarkUnified.spec"
    
    if not os.path.exists(spec_file):
        print(f"❌ Fichier spec non trouvé: {spec_file}")
        return False
    
    try:
        # Commande PyInstaller
        cmd = [sys.executable, "-m", "PyInstaller", spec_file, "--clean"]
        
        print(f"   Exécution: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Compilation réussie")
            return True
        else:
            print("   ❌ Erreur de compilation:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la compilation: {e}")
        return False

def verify_build():
    """Vérifie que l'exécutable a été créé correctement"""
    print("🔍 Vérification du build...")
    
    exe_path = Path("dist/SyncMark.exe")
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ Exécutable créé: {exe_path}")
        print(f"   📏 Taille: {size_mb:.2f} MB")
        return True
    else:
        print(f"   ❌ Exécutable non trouvé: {exe_path}")
        return False

def create_deployment_package():
    """Crée un package de déploiement avec tous les fichiers nécessaires"""
    print("📦 Création du package de déploiement...")
    
    package_dir = Path("deployment_package")
    
    # Créer le répertoire de package
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copier l'exécutable
    exe_source = Path("dist/SyncMark.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, package_dir / "SyncMark.exe")
        print("   ✅ Exécutable copié")
    else:
        print("   ❌ Exécutable source non trouvé")
        return False
    
    # Copier les fichiers de configuration nécessaires
    config_files = [
        "native_host_manifest.json",
        "manifest.json",
        "README.md"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            shutil.copy2(config_file, package_dir / config_file)
            print(f"   ✅ {config_file} copié")
        else:
            print(f"   ⚠️ {config_file} non trouvé (optionnel)")
    
    # Créer un script d'installation simplifié
    install_script = package_dir / "install.bat"
    with open(install_script, 'w', encoding='utf-8') as f:
        f.write("""@echo off
echo Installation de SyncMark...
echo.

REM Installation du Native Host
SyncMark.exe --mode install

echo.
echo Installation terminée !
echo.
echo Pour configurer SyncMark, lancez: SyncMark.exe --mode settings
echo Pour utiliser comme Native Host: SyncMark.exe --mode host
echo.
pause
""")
    
    print(f"   ✅ Package créé dans: {package_dir}")
    return True

def main():
    """Fonction principale du script de build"""
    print("🚀 Construction de SyncMark Unifié")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        sys.exit(1)
    
    # Nettoyer les builds précédents
    clean_build_directories()
    
    # Compiler l'application
    if not build_unified_executable():
        print("\n❌ Échec de la compilation")
        sys.exit(1)
    
    # Vérifier le build
    if not verify_build():
        print("\n❌ Échec de la vérification")
        sys.exit(1)
    
    # Créer le package de déploiement
    if not create_deployment_package():
        print("\n❌ Échec de la création du package")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 Construction terminée avec succès !")
    print("\nFichiers générés:")
    print("  - dist/SyncMark.exe (exécutable principal)")
    print("  - deployment_package/ (package de déploiement)")
    print("\nUtilisation:")
    print("  - Configuration: SyncMark.exe --mode settings")
    print("  - Native Host: SyncMark.exe --mode host")
    print("  - Installation: SyncMark.exe --mode install")

if __name__ == "__main__":
    main()