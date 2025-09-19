# Analyse Comparative des Structures de Tables

## Introduction

Ce rapport présente une analyse détaillée des différences structurelles entre la table de référence `temp_football_matches_scraped` et les 6 tables filtrées.

---

## 1. Résumé Général

- **Table de référence** : `temp_football_matches_scraped` (18 colonnes)
- **Tables filtrées** : 23-24 colonnes chacune

---

## 2. Différences Structurelles par Table

### 2.1. Colonnes Communes

- Toutes les colonnes de la table de référence sont présentes dans chaque table filtrée.

### 2.2. Colonnes Supplémentaires dans les Tables Filtrées

- `temp_match_id` (integer, NOT NULL) : Référence vers la table source
- `filtered_at` (timestamp, NOT NULL) : Horodatage du filtrage
- `source_url` (text, nullable) : URL source des données
- `filter_criteria` (text, nullable) : Critères de filtrage appliqués
- `filter_reason` (text, nullable) : Raison du filtrage
- `analysis_status` (varchar, nullable) : Statut d'analyse
- `auto_selected` (boolean, nullable, default: false) : Sélection automatique
- `total_odds` (numeric, nullable) : Total des cotes *(absente de la table `football_matches_filtered_home_1_5_1_7`)*

---

## 3. Analyse Détaillée par Paire

### 3.1. `temp_football_matches_scraped` vs `football_matches_filtered_home_draw_starting_2`

- **Colonnes supplémentaires** : 6 (voir liste ci-dessus)
- **Différences de types/contraintes** :
  - `id` : auto-incrémenté vs integer simple
  - `scrape_timestamp` : NOT NULL → nullable
- **Contraintes et index** :
  - Contrainte unique : `(temp_match_id, match_name, match_date)`
  - Index unique correspondant

### 3.2. `temp_football_matches_scraped` vs `football_matches_filtered_home_away_starting_2`

- Structure identique à la paire précédente
- Contrainte unique : `unique_match_home_away_2`

### 3.3. `temp_football_matches_scraped` vs `football_matches_filtered_home_1_5_1_7`

- **Colonnes supplémentaires** : 5 (absence de `total_odds`)
- Contrainte unique : `unique_match_home_1_5_1_7`

### 3.4. `temp_football_matches_scraped` vs `football_matches_filtered_draw_away_starting_3`

- Structure identique aux paires 1 & 2
- Contrainte unique : `unique_match_draw_away_3`

### 3.5. `temp_football_matches_scraped` vs `football_matches_filtered_draw_away_starting_2`

- Structure identique aux paires 1, 2 & 4
- Contrainte unique : `unique_match_draw_away_2`

### 3.6. `temp_football_matches_scraped` vs `football_matches_filtered_any_starting_2`

- Structure identique aux paires 1, 2, 4 & 5
- Contrainte unique : `unique_match_any_2`

---

## 4. Points Clés à Retenir

### 4.1. Colonnes Manquantes

- La table de référence ne possède aucune des colonnes de métadonnées de filtrage.

### 4.2. Anomalie Structurelle

- `football_matches_filtered_home_1_5_1_7` est la seule table filtrée sans la colonne `total_odds`.

### 4.3. Contraintes d'Unicité

- Chaque table filtrée possède une contrainte unique sur `(temp_match_id, match_name, match_date)`.

### 4.4. Modifications de Nullabilité

- `scrape_timestamp` : NOT NULL → nullable dans les tables filtrées
- `created_at` : remplacé par `filtered_at`

---

## 5. Recommandations

1. **Corriger l'incohérence** : Ajouter la colonne `total_odds` à `football_matches_filtered_home_1_5_1_7`.
2. **Standardiser les index** : Ajouter des index sur `country` et `tournament` dans les tables filtrées.
3. **Documenter les métadonnées** : Clarifier l'utilisation des colonnes `filter_criteria`, `filter_reason` et `analysis_status`.

---