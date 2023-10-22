-- players table
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    token VARCHAR(100) NOT NULL UNIQUE,
    player_name VARCHAR(50) NOT NULL,
    character_name VARCHAR(50) NOT NULL,
);

-- game_info table
CREATE TABLE game_info (
    game_id SERIAL PRIMARY KEY,
    active BOOLEAN NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    board_data JSONB, -- Game board data
    current_player INT REFERENCES players(player_id), 
);

-- game_states table
CREATE TABLE game_states (
    state_id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game_info(game_id),
    timestamp TIMESTAMP NOT NULL,
    -- Fields to represent the game state, e.g., player positions, card locations, game events, etc.
);

-- game_actions table
CREATE TABLE game_actions (
    action_id SERIAL PRIMARY KEY,
    game_id INT REFERENCES game_info(game_id),
    player_id INT REFERENCES players(player_id),
    timestamp TIMESTAMP NOT NULL,
    action_type VARCHAR(50) NOT NULL,
);

-- cards table
CREATE TABLE cards (
    card_id SERIAL PRIMARY KEY,
    card_type VARCHAR(20) NOT NULL,
    card_name VARCHAR(50) NOT NULL,
);
