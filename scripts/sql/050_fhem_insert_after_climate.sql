DELIMITER // 

DROP TRIGGER IF EXISTS fhem.insert_after_climate;

CREATE TRIGGER fhem.insert_after_climate
AFTER
INSERT
    ON fhem.history FOR EACH ROW BEGIN

    IF NEW.READING IN (
        'Temperature', 
        'Humidity', 
        'Pressure', 
        'desired-temp', 
        'ValvePosition' 
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
            REPLACE(NEW.READING, 'desired-temp', 'Desired-Temperature'),
            CAST(NEW.VALUE AS DOUBLE),
            NOW()
        );

    END IF;
END; //

DELIMITER ;