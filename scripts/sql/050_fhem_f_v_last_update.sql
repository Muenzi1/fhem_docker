CREATE OR REPLACE VIEW fhem.f_v_last_update AS
SELECT 
    last_vals.ID,
    last_vals.TIMESTAMP, 
    last_vals.VALUE, 
    ddm.DEVICE
FROM (
    -- Retrieve last values from battery table
    SELECT 
    fb.ID,
    fb.TIMESTAMP, 
    fb.FK_DEVICE_ID, 
    fb.FK_READING_ID,
    fb.VALUE
    FROM fhem.f_t_battery AS fb
    RIGHT JOIN (
        -- Get latest row per device
        SELECT 
            FK_DEVICE_ID, 
            MAX(ID) AS ID
        FROM fhem.f_t_battery
        GROUP BY FK_DEVICE_ID
    ) AS last_bat
    ON fb.ID = last_bat.ID
    UNION 
    -- Retrieve last values from climate table
    SELECT
    fc.ID,
    fc.TIMESTAMP, 
    fc.FK_DEVICE_ID, 
    fc.FK_READING_ID,
    fc.VALUE
    FROM fhem.f_t_climate AS fc
    RIGHT JOIN (
        -- Get latest row per device
        SELECT 
            FK_DEVICE_ID, 
            MAX(ID) AS ID
        FROM fhem.f_t_climate
        GROUP BY FK_DEVICE_ID
    ) AS last_cli
    ON fc.ID = last_cli.ID
) AS last_vals
-- Join mapping tables 
LEFT JOIN fhem.d_t_device_mapping as ddm
    ON last_vals.FK_DEVICE_ID = ddm.ID
LEFT JOIN fhem.d_t_reading_mapping as drm
    ON last_vals.FK_READING_ID = drm.ID