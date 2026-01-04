CREATE OR REPLACE FUNCTION update_available_copies()
RETURNS TRIGGER AS $$
BEGIN
    -- Zmiana z false -> true (oddanie kopii)
    IF OLD.available = false AND NEW.available = true THEN
        UPDATE game
        SET available_copies = available_copies + 1
        WHERE id = NEW.game_id;

    -- Zmiana z true -> false (wypożyczenie kopii)
    ELSIF OLD.available = true AND NEW.available = false THEN
        UPDATE game
        SET available_copies = available_copies - 1
        WHERE id = NEW.game_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
