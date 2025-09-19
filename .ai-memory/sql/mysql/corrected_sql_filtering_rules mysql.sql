-- ====================================================================
-- SQL FILTERING RULES - VERSION SÉCURISÉE AVEC CRÉATION DE TABLES
-- Garantit que toutes les tables de destination existent avant l'insertion.
-- ====================================================================

-- Création de la table pour la règle 1: ALL ODDS entre 2.0 et 2.99
CREATE TABLE IF NOT EXISTS football_matches_filtered_any_starting_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temp_match_id INT NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    sport VARCHAR(50),
    scrape_timestamp DATETIME,
    filtered_at DATETIME NOT NULL,
    country VARCHAR(100),
    tournament VARCHAR(150),
    home_score INT,
    away_score INT,
    live_status VARCHAR(50),
    INDEX idx_temp_match_id (temp_match_id),
    UNIQUE KEY unique_match (temp_match_id, match_name, match_date)
);

-- Création de la table pour la règle 2: HOME & DRAW entre 2.0 et 2.99
CREATE TABLE IF NOT EXISTS football_matches_filtered_home_draw_starting_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temp_match_id INT NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    sport VARCHAR(50),
    scrape_timestamp DATETIME,
    filtered_at DATETIME NOT NULL,
    country VARCHAR(100),
    tournament VARCHAR(150),
    home_score INT,
    away_score INT,
    live_status VARCHAR(50),
    INDEX idx_temp_match_id (temp_match_id),
    UNIQUE KEY unique_match (temp_match_id, match_name, match_date)
);

-- Création de la table pour la règle 3: HOME & AWAY entre 2.0 et 2.99
CREATE TABLE IF NOT EXISTS football_matches_filtered_home_away_starting_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temp_match_id INT NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    sport VARCHAR(50),
    scrape_timestamp DATETIME,
    filtered_at DATETIME NOT NULL,
    country VARCHAR(100),
    tournament VARCHAR(150),
    home_score INT,
    away_score INT,
    live_status VARCHAR(50),
    INDEX idx_temp_match_id (temp_match_id),
    UNIQUE KEY unique_match (temp_match_id, match_name, match_date)
);

-- Création de la table pour la règle 4: DRAW & AWAY entre 2.0 et 2.99
CREATE TABLE IF NOT EXISTS football_matches_filtered_draw_away_starting_2 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temp_match_id INT NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    sport VARCHAR(50),
    scrape_timestamp DATETIME,
    filtered_at DATETIME NOT NULL,
    country VARCHAR(100),
    tournament VARCHAR(150),
    home_score INT,
    away_score INT,
    live_status VARCHAR(50),
    INDEX idx_temp_match_id (temp_match_id),
    UNIQUE KEY unique_match (temp_match_id, match_name, match_date)
);

-- Création de la table pour la règle 5: DRAW & AWAY entre 3.0 et 3.99 (Schéma spécifique)
CREATE TABLE IF NOT EXISTS football_matches_filtered_draw_away_starting_3 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    country VARCHAR(100),
    tournament VARCHAR(150),
    timestamp DATETIME,
    created_at DATETIME,
    updated_at DATETIME,
    UNIQUE KEY unique_match (match_name, home_team, away_team, match_date)
);

-- Création de la table pour la règle 6: HOME odds entre 1.5 et 1.7
CREATE TABLE IF NOT EXISTS football_matches_filtered_home_1_5_1_7 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temp_match_id INT NOT NULL,
    match_name VARCHAR(255) NOT NULL,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_odds FLOAT,
    draw_odds FLOAT,
    away_odds FLOAT,
    match_date DATE,
    sport VARCHAR(50),
    scrape_timestamp DATETIME,
    filtered_at DATETIME NOT NULL,
    country VARCHAR(100),
    tournament VARCHAR(150),
    home_score INT,
    away_score INT,
    live_status VARCHAR(50),
    INDEX idx_temp_match_id (temp_match_id),
    UNIQUE KEY unique_match (temp_match_id, match_name, match_date)
);


-- ===============================================
--          RÈGLES D'INSERTION ET DE MISE À JOUR
-- ===============================================

-- 1) ALL ODDS entre 2.0 et 2.99
INSERT INTO football_matches_filtered_any_starting_2 (temp_match_id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, filtered_at, country, tournament, home_score, away_score, live_status)
SELECT id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, NOW(), country, tournament, home_score, away_score, live_status
FROM temp_football_matches_scraped
WHERE home_odds BETWEEN 2.0 AND 2.99 AND draw_odds BETWEEN 2.0 AND 2.99 AND away_odds BETWEEN 2.0 AND 2.99 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), scrape_timestamp = VALUES(scrape_timestamp), filtered_at = NOW();

-- 2) HOME & DRAW entre 2.0 et 2.99
INSERT INTO football_matches_filtered_home_draw_starting_2 (temp_match_id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, filtered_at, country, tournament, home_score, away_score, live_status)
SELECT id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, NOW(), country, tournament, home_score, away_score, live_status
FROM temp_football_matches_scraped
WHERE home_odds BETWEEN 2.0 AND 2.99 AND draw_odds BETWEEN 2.0 AND 2.99 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), scrape_timestamp = VALUES(scrape_timestamp), filtered_at = NOW();

-- 3) HOME & AWAY entre 2.0 et 2.99
INSERT INTO football_matches_filtered_home_away_starting_2 (temp_match_id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, filtered_at, country, tournament, home_score, away_score, live_status)
SELECT id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, NOW(), country, tournament, home_score, away_score, live_status
FROM temp_football_matches_scraped
WHERE home_odds BETWEEN 2.0 AND 2.99 AND away_odds BETWEEN 2.0 AND 2.99 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), scrape_timestamp = VALUES(scrape_timestamp), filtered_at = NOW();

-- 4) DRAW & AWAY entre 2.0 et 2.99
INSERT INTO football_matches_filtered_draw_away_starting_2 (temp_match_id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, filtered_at, country, tournament, home_score, away_score, live_status)
SELECT id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, NOW(), country, tournament, home_score, away_score, live_status
FROM temp_football_matches_scraped
WHERE draw_odds BETWEEN 2.0 AND 2.99 AND away_odds BETWEEN 2.0 AND 2.99 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), scrape_timestamp = VALUES(scrape_timestamp), filtered_at = NOW();

-- 5) DRAW & AWAY entre 3.0 et 3.99
INSERT INTO football_matches_filtered_draw_away_starting_3 (timestamp, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, country, tournament, created_at)
SELECT NOW(), match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, country, tournament, NOW()
FROM temp_football_matches_scraped
WHERE draw_odds BETWEEN 3.0 AND 3.99 AND away_odds BETWEEN 3.0 AND 3.99 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), timestamp = VALUES(timestamp), updated_at = NOW();

-- 6) HOME odds entre 1.5 et 1.7
INSERT INTO football_matches_filtered_home_1_5_1_7 (temp_match_id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, filtered_at, country, tournament, home_score, away_score, live_status)
SELECT id, match_name, home_team, away_team, home_odds, draw_odds, away_odds, match_date, sport, scrape_timestamp, NOW(), country, tournament, home_score, away_score, live_status
FROM temp_football_matches_scraped
WHERE home_odds BETWEEN 1.5 AND 1.7 AND sport = 'football'
ON DUPLICATE KEY UPDATE home_odds = VALUES(home_odds), draw_odds = VALUES(draw_odds), away_odds = VALUES(away_odds), scrape_timestamp = VALUES(scrape_timestamp), filtered_at = NOW();