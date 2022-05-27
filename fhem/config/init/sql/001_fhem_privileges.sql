GRANT ALL PRIVILEGES ON fhem.* TO 'fhemuser'@'%';

CREATE USER 'grafana'@'%' IDENTIFIED BY 'SET_CREDENTIALS_HERE';
GRANT SELECT ON fhem.* TO 'grafana'@'%';
