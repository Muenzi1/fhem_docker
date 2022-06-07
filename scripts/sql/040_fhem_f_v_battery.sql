CREATE OR REPLACE VIEW fhem.f_v_battery AS
SELECT 
    facts.ID,
    facts.TIMESTAMP,
    facts.YEAR, 
    facts.MONTH, 
    facts.WEEK, 
    facts.DAY, 
    facts.VALUE,
    ddm.DASHBOARD,
    ddm.DISPLAY_NAME,
    drm.READING,
    drm.UNIT
FROM fhem.f_t_battery AS facts
LEFT JOIN fhem.d_t_device_mapping AS ddm
    ON facts.FK_DEVICE_ID = ddm.ID
LEFT JOIN fhem.d_t_reading_mapping AS drm
    ON facts.FK_READING_ID = drm.ID
;