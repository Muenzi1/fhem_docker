CREATE TABLE IF NOT EXISTS fhem.d_t_device_mapping (
    ID TINYINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    DEVICE varchar(64),
    DISPLAY_NAME varchar(64),
    TYPE varchar(20),
    DASHBOARD varchar(64),
    _CREATED_AT TIMESTAMP NOT NULL DEFAULT NOW()
);

TRUNCATE TABLE fhem.d_t_device_mapping;

LOAD DATA LOCAL INFILE '/home/config/input_device_mapping.csv'
INTO TABLE fhem.d_t_device_mapping
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;