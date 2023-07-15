-- 1) Check data by querying:
USE bcn_real_state;
SELECT *
FROM habitaclia_data;

-- 2) Descriptive data querying: Average price in Barcelona
USE bcn_real_state;
SELECT AVG(Price_€)
FROM habitaclia_data;

-- 3) Descriptive data querying: Get the ad with the max price currently on sale
USE bcn_real_state;
SELECT *
FROM habitaclia_data
WHERE Price_€ = (SELECT MAX(Price_€) FROM habitaclia_data);

-- 4) Descriptive data querying: Get the ad with the min price currently on sale
USE bcn_real_state;
SELECT *
FROM habitaclia_data
WHERE Price_€ = (SELECT MIN(Price_€) FROM habitaclia_data);

-- 5) Descriptive data querying: Checking different neightborhoods and number of ads
USE bcn_real_state;
SELECT DISTINCT Neightbourhood, COUNT(Neightbourhood) AS ads_by_Neigh
FROM habitaclia_data
GROUP BY 1
ORDER BY 2 DESC;

-- 6) Descriptive data querying: Checking different Districts and number of ads
USE bcn_real_state;
SELECT DISTINCT District, COUNT(District) as ads_by_Districs
FROM habitaclia_data
GROUP BY 1
ORDER BY 2 DESC;

-- Checking joins between tables - Adding latitude and longitude to ayuntamiento price m2 datset
USE bcn_real_state;
SELECT *
FROM bcn_ayuntamiento_hist_data a
JOIN bcn_neighborhoods_coordinates n ON a.Barrios = n.nom_barri;

-- Checking joins between tables - Adding latitude and longitude of neightborhoods and districts to habitaclia datset
USE bcn_real_state;
SELECT *
FROM habitaclia_data h
JOIN bcn_neighborhoods_coordinates n ON h.nom_barri = n.nom_barri
JOIN bcn_district_coordinates d ON h.District = d.nom_districte;