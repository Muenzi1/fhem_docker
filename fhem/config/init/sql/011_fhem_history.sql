CREATE TABLE fhem.current (
    TIMESTAMP TIMESTAMP,
    DEVICE varchar(64),
    TYPE varchar(64),
    EVENT varchar(512),
    READING varchar(64),
    VALUE varchar(255),
    UNIT varchar(32)
);