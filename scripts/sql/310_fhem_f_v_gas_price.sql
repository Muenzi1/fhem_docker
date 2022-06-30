CREATE OR REPLACE VIEW fhem.f_v_gas_price AS 
SELECT 
    TIMESTAMP
    , YEAR
    , MONTH
    , WEEK
    , DAY
    , REF_LOC
    , BRAND
    , FK_STATION_ID
    , e5
    , e10
    , diesel
FROM fhem.f_t_gas_price AS f
INNER JOIN fhem.d_t_gas_station AS dim
ON f.FK_STATION_ID = dim.ID
;