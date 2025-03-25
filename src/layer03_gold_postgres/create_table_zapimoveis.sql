CREATE TABLE gold.zapimoveis AS
SELECT
    property_id,
    UPPER(TRIM(SPLIT_PART(state_city, '+', 1))) AS state_name,
    INITCAP(TRIM(SPLIT_PART(REPLACE(state_city, '-',' '), '+', 2))) AS city_name,
	CONCAT(
		INITCAP(TRIM(SPLIT_PART(REPLACE(state_city, '-',' '), '+', 2))), 
		' - ', 
		UPPER(TRIM(SPLIT_PART(state_city, '+', 1)))
	) city_state_name,
    location,
    street,
    type_realese,
	TRIM(
	    CASE 
	        WHEN POSITION('-' IN area) > 0 THEN REPLACE(LEFT(area, POSITION('-' IN area) - 1), 'm²', '')
	        ELSE REPLACE(area, 'm²', '')
	    END
	) AS area,
    CASE
        WHEN rooms LIKE '%-%' THEN SUBSTRING(rooms FROM 1 FOR POSITION('-' IN rooms) - 1)
        ELSE rooms
    END AS rooms,
    CASE
        WHEN bathrooms LIKE '%-%' THEN SUBSTRING(bathrooms FROM 1 FOR POSITION('-' IN bathrooms) - 1)
        ELSE bathrooms
    END AS bathrooms,
    REGEXP_REPLACE(price, '[^0-9]', '', 'g') AS price,
	ROUND(
		CAST(NULLIF(REGEXP_REPLACE(price, '[^0-9]', '', 'g'), '') AS DECIMAL) 
		/
		CAST(NULLIF(
		        TRIM(
		            CASE 
		                WHEN POSITION('-' IN area) > 0 THEN REPLACE(LEFT(area, POSITION('-' IN area) - 1), 'm²', '')
		                ELSE REPLACE(area, 'm²', '')
		            END), 
			'') 
		AS DECIMAL),2) AS area_price_ratio,
    link,
	TO_TIMESTAMP(update_at, 'YYYY-MM-DD HH24-MI-SS') AS update_at,
    CAST(LEFT(update_at, 4) AS INTEGER) AS year_update_at
FROM silver.zapimoveis;

ALTER TABLE gold.zapimoveis
ADD PRIMARY KEY (property_id, update_at);

