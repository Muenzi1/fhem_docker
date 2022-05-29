CREATE OR REPLACE VIEW fhem.f_climate_sz AS 
    SELECT 
        facts.TIMESTAMP, 
        facts.DEVICE,
        facts.READING,
        facts.VALUE
    FROM fhem.climate AS facts
    LEFT JOIN dim_device_dashboard_mapping AS dim
        ON facts.DEVICE = dim.DEVICE
    WHERE DASHBOARD = 'climate_sz';