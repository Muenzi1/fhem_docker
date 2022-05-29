CREATE TABLE IF NOT EXISTS fhem.d_t_device_dashboard (
    ID TINYINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    DEVICE varchar(64),
    DASHBOARD varchar(64),
    _CREATED_AT TIMESTAMP NOT NULL DEFAULT NOW()
);

TRUNCATE TABLE fhem.dim_device_dashboard_mapping;

LOAD DATA LOCAL INFILE '/home/config/input_device_dashboard_mapping.csv'
INTO TABLE fhem.dim_device_dashboard_mapping
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;