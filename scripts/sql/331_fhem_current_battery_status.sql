CREATE OR REPLACE VIEW fhem.f_v_current_battery_status AS
SELECT 
    facts.TIMESTAMP,
    facts.DISPLAY_NAME,
    facts.VALUE
FROM fhem.f_v_battery AS facts
RIGHT JOIN (
    SELECT 
        DISPLAY_NAME, 
        MAX(ID) AS ID
    FROM fhem.f_v_battery
    GROUP BY DISPLAY_NAME
) AS max_id 
ON facts.ID = max_id.ID