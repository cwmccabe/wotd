CREATE TABLE wotd (
 word_lc text NOT NULL,
 word text NOT NULL,
 type text NOT NULL,
 pronunciation text NOT NULL,
 definition text NOT NULL,
 example text DEFAULT NULL,
 interesting_fact text DEFAULT NULL,
 contributor_name text NOT NULL,
 wotd_date DATETIME, 
 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
