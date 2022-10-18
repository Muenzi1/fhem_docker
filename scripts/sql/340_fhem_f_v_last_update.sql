CREATE OR REPLACE VIEW
    fhem.f_v_last_update AS
SELECT DISTINCT
  last_vals.TIMESTAMP
  , ddm.DEVICE
FROM
    (
        -- Retrieve last values from battery table
        SELECT
          fb.TIMESTAMP
          , fb.FK_DEVICE_ID
        FROM
            fhem.f_t_battery AS fb
            RIGHT JOIN (
                -- Get latest row per device
                SELECT
                    FK_DEVICE_ID
                  , MAX(ID) AS ID
                FROM
                    fhem.f_t_battery
                GROUP BY
                    FK_DEVICE_ID
            ) AS last_bat ON fb.ID = last_bat.ID
        UNION
        -- Retrieve last values from climate table
        SELECT
            fc.TIMESTAMP
          , fc.FK_DEVICE_ID
        FROM
            fhem.f_t_climate AS fc
            RIGHT JOIN (
                -- Get latest row per device
                SELECT
                    FK_DEVICE_ID
                  , MAX(ID) AS ID
                FROM
                    fhem.f_t_climate
                GROUP BY
                    FK_DEVICE_ID
            ) AS last_cli ON fc.ID = last_cli.ID
    ) AS last_vals
    -- Join mapping tables 
    LEFT JOIN fhem.d_t_device_mapping AS ddm ON last_vals.FK_DEVICE_ID = ddm.ID