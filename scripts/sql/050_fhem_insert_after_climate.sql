DELIMITER // 

CREATE TRIGGER fhem.insert_after_climate
AFTER
INSERT
    ON fhem.history FOR EACH ROW BEGIN

    IF NEW.READING IN ('Temperature', 'Humidity', 'Pressure') THEN

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

DELIMITER;