CREATE TRIGGER trg_update_available_copies
AFTER UPDATE OF available
ON copy
FOR EACH ROW
WHEN (OLD.available IS DISTINCT FROM NEW.available)
EXECUTE FUNCTION update_available_copies();
