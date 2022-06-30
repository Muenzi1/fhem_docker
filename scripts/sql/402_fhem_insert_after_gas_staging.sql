DELIMITER // 

DROP TRIGGER IF EXISTS fhem.insert_after_gas_staging;

CREATE TRIGGER fhem.insert_after_gas_staging
AFTER INSERT
    ON fhem.l_t_gas_price FOR EACH ROW BEGIN

INSERT IGNORE INTO fhem.d_t_gas_station (
        STATION_ID,
        BRAND,
        STREET,
        HOUSE_NUMBER,
        POST_CODE,
        PLACE,
        LATITUDE,
        LONGITUDE,
        REF_LOC,
        _CREATED_AT
    )
SELECT
    NEW.id,
    NEW.brand,
    NEW.street,
    NEW.houseNumber,
    NEW.postCode,
    NEW.place,
    NEW.lat,
    NEW.lng,
    NEW.ref_loc,
    NEW._CREATED_AT;

INSERT INTO
    fhem.f_t_gas_price (
        FK_STATION_ID,
        TIMESTAMP,
        E5,
        E10,
        DIESEL
    )
SELECT
    dim.ID,
    NEW._CREATED_AT,
    NEW.e5,
    NEW.e10,
    NEW.diesel
FROM
    fhem.l_t_gas_price as ld
INNER JOIN fhem.d_t_gas_station AS dim
    ON dim.STATION_ID = NEW.ID
WHERE NEW.ID = ld.ID;

END;

// DELIMITER ;
