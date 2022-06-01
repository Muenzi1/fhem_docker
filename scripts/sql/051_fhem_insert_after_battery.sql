DELIMITER // 

DROP TRIGGER IF EXISTS fhem.insert_after_battery;

CREATE TRIGGER fhem.insert_after_battery
AFTER
INSERT
    ON fhem.history FOR EACH ROW BEGIN

    IF NEW.READING IN (
        'batteryLevel' 
    ) THEN

    INSERT INTO
        fhem.f_t_climate (
            TIMESTAMP,
            YEAR,
            MONTH,
            WEEK,
            DAY,
            DEVICE,
            TYPE,
            READING,
            VALUE,
            _CREATED_AT
        )
    VALUES
        (
            NEW.TIMESTAMP,
            NEW.YEAR,
            NEW.MONTH,
            NEW.WEEK,
            NEW.DAY,
            NEW.DEVICE,
            NEW.TYPE,
            NEW.READING,
            CAST(NEW.VALUE AS DOUBLE),
            NOW()
        );

    END IF;
END; //

DELIMITER ;