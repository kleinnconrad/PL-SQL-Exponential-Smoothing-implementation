create or replace PROCEDURE EXPONENTIAL_SMOOTHING AS
I NUMBER := 0;
MAX_K NUMBER(5);
alpha decimal := 0.2;

BEGIN

SELECT MAX(K) INTO MAX_K  -- Anzahl Beobachtungen
    FROM
        (
            SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER
            ,ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM ASC) AS K
                FROM source_table
            WHERE KUENDIGER IS NOT NULL
            group by datum
            ORDER BY DATUM ASC
        )
;
EXECUTE IMMEDIATE 'truncate table analytics.var_x'
;
-- Berechnungsfenster erzeugen
FOR I IN 0..10 LOOP

    INSERT INTO ANALYTICS.VAR_X

    SELECT X + POWER((1-alpha),ANZ + 1)*
                                        (
                                            select kuendiger
                                                FROM
                                                    (
                                                        SELECT KUENDIGER
                                                        ,ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM DESC) AS rn
                                                            FROM
                                                                (
                                                                    SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER
                                                                        FROM source_table
                                                                    WHERE KUENDIGER IS NOT NULL
                                                                    group by datum
                                                                )
                                                    )
                                            WHERE rn = max_k - (10-i)
                                        ) as prog_1
        FROM
            (
                SELECT COUNT(*) AS ANZ, SUM(X) AS X
                    FROM
                        (
                            SELECT alpha*POWER((1-alpha),k)*KUENDIGER AS X
                            ,Z.*
                                FROM (
                                        SELECT DATUM, SUM(KUENDIGER) AS KUENDIGER
                                        ,ROW_NUMBER() OVER(PARTITION BY 1 ORDER BY DATUM ASC) AS K
                                            FROM source_table
                                        WHERE KUENDIGER IS NOT NULL
                                        group by datum
                                        ORDER BY DATUM ASC
                                     ) Z
                            WHERE K BETWEEN 1 + i AND max_K - (10-i)
                        )
            )
    ;
END LOOP;

END EXPONENTIAL_SMOOTHING;
