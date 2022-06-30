CREATE TABLE IF NOT EXISTS fhem.l_t_gas_price (
    id varchar(64),
    name varchar(64),
    brand varchar(64),
    street varchar(64),
    place varchar(64),
    ref_loc, varchar(32),
    lat DOUBLE,
    lng DOUBLE,
    dist DOUBLE,
    diesel DOUBLE,
    e5 DOUBLE,
    e10 DOUBLE,
    isOpen BOOLEAN,
    houseNumber varchar(8),
    postCode INT, 
    _CREATED_AT TIMESTAMP NOT NULL DEFAULT NOW()
);
