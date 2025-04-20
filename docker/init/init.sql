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


COPY player_stats
FROM '/docker-entrypoint-initdb.d/data/file1.csv'
DELIMITER ','
CSV HEADER;

COPY player_stats
FROM '/docker-entrypoint-initdb.d/data/file2.csv'
DELIMITER ','
CSV HEADER;

COPY player_stats
FROM '/docker-entrypoint-initdb.d/data/file3.csv'
DELIMITER ','
CSV HEADER;