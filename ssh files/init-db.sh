#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be fully ready..."
until PGPASSWORD=${POSTGRES_PASSWORD} psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "SELECT 1;" &> /dev/null; do
    sleep 2
    echo "Waiting for database connection..."
done

echo "Creating player_stats table..."
PGPASSWORD=${POSTGRES_PASSWORD} psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} <<EOSQL
CREATE TABLE IF NOT EXISTS player_stats (
    season_year TEXT,
    game_date DATE,
    game_id INTEGER,
    matchup TEXT,
    team_id INTEGER,
    team_city TEXT,
    team_name TEXT,
    team_tricode TEXT,
    team_slug TEXT,
    person_id INTEGER,
    person_name TEXT,
    position TEXT,
    comment TEXT,
    jersey_num TEXT,
    minutes TEXT,
    field_goals_made INTEGER,
    field_goals_attempted INTEGER,
    field_goals_percentage FLOAT,
    three_pointers_made INTEGER,
    three_pointers_attempted INTEGER,
    three_pointers_percentage FLOAT,
    free_throws_made INTEGER,
    free_throws_attempted INTEGER,
    free_throws_percentage FLOAT,
    rebounds_offensive INTEGER,
    rebounds_defensive INTEGER,
    rebounds_total INTEGER,
    assists INTEGER,
    steals INTEGER,
    blocks INTEGER,
    turnovers INTEGER,
    fouls_personal INTEGER,
    points INTEGER,
    plus_minus_points INTEGER
);
EOSQL

echo "Importing CSV files..."
for file in /csv/*.csv; do
    echo "Processing $file..."
    PGPASSWORD=${POSTGRES_PASSWORD} psql -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB} -c "\COPY player_stats FROM '$file' DELIMITER ',' CSV HEADER;"
done

echo "Data import completed!"
