CREATE TABLE gold.zapimoveis AS
SELECT
    property_id,
    UPPER(TRIM(SPLIT_PART(state_city, '+', 1))) AS state_name,
    INITCAP(TRIM(SPLIT_PART(REPLACE(state_city, '-',''), '+', 2))) AS city_name,
    location,
    street,
    type_realese,
    TRIM(REPLACE(
        CASE
            WHEN POSITION('-' IN REPLACE(area, 'm²', '')) > 0 
                THEN SUBSTRING(REPLACE(area, 'm²', '') FROM 1 FOR POSITION('-' IN REPLACE(area, 'm²', '')) - 1)
            ELSE REPLACE(area, 'm²', '')
        END, ' ', '')) AS area,
    CASE
        WHEN rooms LIKE '%-%' THEN SUBSTRING(rooms FROM 1 FOR POSITION('-' IN rooms) - 1)
        ELSE rooms
    END AS rooms,
    CASE
        WHEN bathrooms LIKE '%-%' THEN SUBSTRING(bathrooms FROM 1 FOR POSITION('-' IN bathrooms) - 1)
        ELSE bathrooms
    END AS bathrooms,
    REGEXP_REPLACE(price, '[^0-9]', '', 'g') AS price,
    link,
    update_at
FROM silver.zapimoveis;

ALTER TABLE gold.zapimoveis
ADD PRIMARY KEY (property_id, update_at);
