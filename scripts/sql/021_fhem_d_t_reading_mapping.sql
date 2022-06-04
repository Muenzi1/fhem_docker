CREATE TABLE IF NOT EXISTS fhem.d_t_reading_mapping (
    ID TINYINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    READING_ORIG varchar(64),
    READING varchar(64),
    UNIT varchar(64),
    _CREATED_AT TIMESTAMP NOT NULL DEFAULT NOW()
);

TRUNCATE TABLE fhem.d_t_reading_mapping;

LOAD DATA LOCAL INFILE '/home/config/input_reading_mapping.csv'
INTO TABLE fhem.d_t_reading_mapping
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;