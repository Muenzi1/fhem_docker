CREATE OR REPLACE VIEW
    fhem.f_v_current_battery_status AS
SELECT
    facts.TIMESTAMP
  , facts.VALUE
  , ddm.DISPLAY_NAME
FROM
    (
        SELECT
            FK_DEVICE_ID
          , MAX(ID) AS ID
        FROM
            fhem.f_t_battery
        GROUP BY
            FK_DEVICE_ID
    ) AS maxids
    LEFT JOIN fhem.f_t_battery AS facts ON maxids.ID = facts.ID
    LEFT JOIN fhem.d_t_device_mapping AS ddm ON facts.FK_DEVICE_ID = ddm.ID