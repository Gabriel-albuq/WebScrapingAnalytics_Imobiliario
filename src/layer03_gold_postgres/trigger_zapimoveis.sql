CREATE OR REPLACE FUNCTION update_gold_zapimoveis() 
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO gold.zapimoveis (
        property_id,
        state_name,
        city_name,
        location,
        street,
        type_realese,
        area,
        rooms,
        bathrooms,
        price,
        link,
        update_at
    )
    VALUES (
        NEW.property_id,
        UPPER(TRIM(SPLIT_PART(NEW.state_city, '+', 1))),
        INITCAP(TRIM(SPLIT_PART(REPLACE(NEW.state_city, '-',''), '+', 2))),
        NEW.location,
        NEW.street,
        NEW.type_realese,
        TRIM(REPLACE(
            CASE
                WHEN POSITION('-' IN REPLACE(NEW.area, 'm²', '')) > 0 
                    THEN SUBSTRING(REPLACE(NEW.area, 'm²', '') FROM 1 FOR POSITION('-' IN REPLACE(NEW.area, 'm²', '')) - 1)
                ELSE REPLACE(NEW.area, 'm²', '')
            END, ' ', '')),
        CASE
            WHEN NEW.rooms LIKE '%-%' THEN SUBSTRING(NEW.rooms FROM 1 FOR POSITION('-' IN NEW.rooms) - 1)
            ELSE NEW.rooms
        END,
        CASE
            WHEN NEW.bathrooms LIKE '%-%' THEN SUBSTRING(NEW.bathrooms FROM 1 FOR POSITION('-' IN NEW.bathrooms) - 1)
            ELSE NEW.bathrooms
        END,
        REGEXP_REPLACE(NEW.price, '[^0-9]', '', 'g'),
        NEW.link,
        NEW.update_at
    )
    ON CONFLICT (property_id, update_at) DO UPDATE
    SET 
        state_name = EXCLUDED.state_name,
        city_name = EXCLUDED.city_name,
        location = EXCLUDED.location,
        street = EXCLUDED.street,
        type_realese = EXCLUDED.type_realese,
        area = EXCLUDED.area,
        rooms = EXCLUDED.rooms,
        bathrooms = EXCLUDED.bathrooms,
        price = EXCLUDED.price,
        link = EXCLUDED.link,
        update_at = EXCLUDED.update_at;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_gold_zapimoveis_trigger
AFTER INSERT OR UPDATE ON silver.zapimoveis
FOR EACH ROW
EXECUTE FUNCTION update_gold_zapimoveis();


CREATE OR REPLACE FUNCTION delete_gold_zapimoveis() 
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM gold.zapimoveis WHERE property_id = OLD.property_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER delete_gold_zapimoveis_trigger
AFTER DELETE ON silver.zapimoveis
FOR EACH ROW
EXECUTE FUNCTION delete_gold_zapimoveis();
