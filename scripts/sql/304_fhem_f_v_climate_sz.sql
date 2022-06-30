CREATE OR REPLACE VIEW fhem.f_v_climate_sz AS 
SELECT 
    facts.ID,
    facts.TIMESTAMP,
    facts.YEAR, 
    facts.MONTH, 
    facts.WEEK, 
    facts.DAY, 
    facts.VALUE,
    facts.DASHBOARD,
    facts.DISPLAY_NAME,
    facts.READING,
    facts.UNIT
FROM fhem.f_v_climate AS facts
WHERE DASHBOARD = 'climate_sz'
;