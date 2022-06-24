DELIMITER // 

DROP TRIGGER IF EXISTS fhem.insert_after_gas_staging;

CREATE TRIGGER fhem.insert_after_gas_staging
AFTER
INSERT
    ON fhem.history FOR EACH ROW BEGIN

    INSERT INTO
        fhem.f_t_gas_price (
            FK_STATION_ID,
            TIMESTAMP,
            E5,
            E10,
            DIESEL
        )
            SELECT
            NEW.ID,
            NEW.TIMESTAMP,
            NEW.e5, 
            NEW.e10,
            NEW.diesel
        ;

    END IF;
END; //

DELIMITER ;