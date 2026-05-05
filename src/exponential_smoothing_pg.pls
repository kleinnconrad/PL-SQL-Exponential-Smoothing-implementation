CREATE OR REPLACE PROCEDURE analytics.exponential_smoothing()
LANGUAGE plpgsql
AS $$
DECLARE
    i INT := 0;
    max_k INT;
    alpha NUMERIC := 0.2;
BEGIN
    -- Anzahl Beobachtungen
    SELECT MAX(K) INTO max_k  
    FROM
    (
        SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER,
               ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM ASC) AS K
        FROM analytics.source_table
        WHERE KUENDIGER IS NOT NULL
        GROUP BY datum
    ) sub1; -- Postgres requires aliases for subqueries

    EXECUTE 'TRUNCATE TABLE analytics.var_x';

    -- Berechnungsfenster erzeugen.
    FOR i IN 0..10 LOOP
        
        -- Explicitly insert into the prog_1 column so the ID auto-generates
        INSERT INTO analytics.var_x (prog_1)
        SELECT X + POWER((1-alpha), ANZ + 1) *
        (
            SELECT kuendiger 
            FROM
            (
                SELECT KUENDIGER, ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM DESC) AS rn
                FROM
                (
                    SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER
                    FROM analytics.source_table
                    WHERE KUENDIGER IS NOT NULL
                    GROUP BY datum
                ) sub2
            ) sub3
            WHERE rn = max_k - (10-i)
        ) as prog_1
        FROM
        (
            SELECT COUNT(*) AS ANZ, SUM(X) AS X
            FROM
            (
                SELECT alpha * POWER((1-alpha), k) * KUENDIGER AS X, Z.*
                FROM 
                (
                    SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER,
                           ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM ASC) AS K
                    FROM analytics.source_table
                    WHERE KUENDIGER IS NOT NULL
                    GROUP BY datum
                ) Z
                WHERE K BETWEEN 1 + i AND max_k - (10-i)
            ) sub4
        ) sub5;
        
    END LOOP;

END;
$$;
