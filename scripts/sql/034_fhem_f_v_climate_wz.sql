CREATE OR REPLACE VIEW fhem.f_v_climate_wz AS 
    SELECT 
        facts.TIMESTAMP, 
        facts.DEVICE,
        facts.READING,
        facts.VALUE
    FROM fhem.f_t_climate AS facts
    LEFT JOIN d_t_device_dashboard AS dim
        ON facts.DEVICE = dim.DEVICE
    WHERE DASHBOARD = 'climate_wz';