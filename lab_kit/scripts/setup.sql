-- Tricon CoCo lab: creates your own schema, DEMO_DB.TPCH_<INITIALS>.
-- You don't need to edit anything: your initials are already filled in.
-- Stops with an error if someone else already uses these initials.
USE ROLE DEMO_ROLE;
USE WAREHOUSE DEMO_WH;

EXECUTE IMMEDIATE $$
DECLARE
  initials_taken EXCEPTION (-20002, 'Another participant already uses these initials. Pick new initials in the lab guide sidebar and download the lab kit again.');
  schema_name VARCHAR DEFAULT 'TPCH_<INITIALS>';
  claimed_by VARCHAR;
  me VARCHAR DEFAULT CURRENT_USER();
  orders INTEGER;
  leftover INTEGER;
BEGIN
  SELECT MAX(COMMENT) INTO :claimed_by
    FROM DEMO_DB.INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :schema_name;
  IF (claimed_by IS NOT NULL AND claimed_by <> 'Workshop schema for ' || me) THEN
    RAISE initials_taken;
  END IF;
  EXECUTE IMMEDIATE 'CREATE SCHEMA IF NOT EXISTS DEMO_DB.' || schema_name;
  EXECUTE IMMEDIATE 'ALTER SCHEMA DEMO_DB.' || schema_name || ' SET COMMENT = ''Workshop schema for ' || me || '''';
  SELECT COUNT(*) INTO :orders FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.ORDERS;
  SELECT COUNT(*) INTO :leftover FROM DEMO_DB.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = :schema_name;
  RETURN 'READY: DEMO_DB.' || schema_name || ' for ' || me || ' (sample data: ' || orders || ' orders; '
    || CASE WHEN leftover = 0 THEN 'empty schema, a fresh start' ELSE leftover || ' tables from an earlier run, rebuilt on your next Build' END || ')';
END;
$$;
