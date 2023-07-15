-- 1) Creating the Dtabase that will be used to load data from Python
DROP DATABASE IF EXISTS bcn_real_state;
CREATE DATABASE bcn_real_state;
-- 2) Tables created and uploaded from Python
-- 3) Altering tables to assign correct datatypes, Primary Keys and Foreign Keys:
USE bcn_real_state;
ALTER TABLE bcn_neighborhoods_coordinates 
MODIFY COLUMN nom_barri VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN Neighborhood_lat FLOAT(6),
MODIFY COLUMN Neighborhood_long FLOAT(6);

USE bcn_real_state;
ALTER TABLE bcn_district_coordinates 
MODIFY COLUMN nom_districte VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN District_lat FLOAT(6),
MODIFY COLUMN District_long FLOAT(6);

USE bcn_real_state;
ALTER TABLE habitaclia_data 
MODIFY COLUMN ID VARCHAR(255) PRIMARY KEY,
MODIFY COLUMN Address VARCHAR(255),
MODIFY COLUMN Property_type VARCHAR(255),
MODIFY COLUMN City VARCHAR(255),
MODIFY COLUMN Neightbourhood VARCHAR(255),
MODIFY COLUMN Links VARCHAR(255),
MODIFY COLUMN Date_Scraped DATE,
MODIFY COLUMN District VARCHAR(255),
MODIFY COLUMN nom_barri VARCHAR(255);

USE bcn_real_state;
ALTER TABLE monthly_euribor_data 
MODIFY COLUMN Año INT,
MODIFY COLUMN Mes VARCHAR(255),
MODIFY COLUMN Valor FLOAT,
MODIFY COLUMN Fecha DATE PRIMARY KEY;

USE bcn_real_state;
ALTER TABLE bcn_ayuntamiento_hist_data 
MODIFY COLUMN Barrios VARCHAR(255),
MODIFY COLUMN Year INT,
MODIFY COLUMN Price_m2 INT;

-- Relationing habitaclia_data with bcn_neighborhoods_coordinates & bcn_district_coordinates
USE bcn_real_state;
ALTER TABLE habitaclia_data
	ADD FOREIGN KEY (nom_barri)
    REFERENCES bcn_neighborhoods_coordinates(nom_barri)
    ON DELETE CASCADE;
    
USE bcn_real_state;
ALTER TABLE habitaclia_data
	ADD FOREIGN KEY (District)
    REFERENCES bcn_district_coordinates(nom_districte)
    ON DELETE CASCADE;
    
USE bcn_real_state;
ALTER TABLE bcn_ayuntamiento_hist_data
	ADD FOREIGN KEY (Barrios)
    REFERENCES bcn_neighborhoods_coordinates(nom_barri)
    ON DELETE CASCADE;