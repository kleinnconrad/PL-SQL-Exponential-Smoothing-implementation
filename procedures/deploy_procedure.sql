-- procedures/deploy_procedure.sql

CREATE OR REPLACE PROCEDURE analytics.process_dummy_data()
LANGUAGE plpgsql
AS $$
BEGIN
    -- This syntax operates almost exactly like Oracle PL/SQL
    RAISE NOTICE 'Procedure executed successfully.';
END;
$$;
