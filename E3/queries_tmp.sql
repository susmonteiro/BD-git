
WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

-- SELECT num_regiao AS Numero_Regiao, num_concelho AS Numero_Concelho, num_doente AS Numero_Doente, MIN(quant) AS Quantidade_Min, MAX(quant) AS Quantidade_Max
-- FROM EG,
--     (SELECT num_doente, MIN(quant) FROM EG AS E WHERE E.num_regiao=EG.num_regiao AND E.num_concelho=EG.num_concelho) AS MI,
--     (SELECT num_doente, MAX(quant) FROM EG AS E WHERE E.num_regiao=EG.num_regiao AND E.num_concelho=EG.num_concelho) AS MA

-- GROUP BY (num_regiao, num_concelho);

SELECT num_regiao AS Numero_Regiao, num_concelho AS Numero_Concelho, 
    MI.num_doente AS Numero_Doente_Minimo, MI.q AS Quantidade_Min,
    MA.num_doente AS Numero_Doente_Maximo, MA.q AS Quantidade_Max
FROM EG,
    (SELECT num_regiao, num_concelho, num_doente, MIN(quant) AS q FROM EG GROUP BY (num_regiao, num_concelho)) AS MI,
    (SELECT num_regiao, num_concelho, num_doente, MAX(quant) AS q FROM EG GROUP BY (num_regiao, num_concelho)) AS MA
WHERE num_regiao = MI.num_regiao AND num_regiao=MA.num_regiao AND num_concelho = MI.num_concelho AND num_concelho=MA.num_concelho; 


SELECT num_regiao AS Numero_Regiao, num_concelho AS Numero_Concelho, 
    MI.num_doente AS Numero_Doente_Minimo, MI.q AS Quantidade_Min,
    MA.num_doente AS Numero_Doente_Maximo, MA.q AS Quantidade_Max
FROM 
    (SELECT num_regiao, num_concelho, MIN(quant) AS q FROM EG GROUP BY (num_regiao, num_concelho)) AS MI,
    (SELECT num_regiao, num_concelho, MAX(quant) AS q FROM EG GROUP BY (num_regiao, num_concelho)) AS MA,
    EG EXCEPT (SELECT num_regiao, num_concelho, num_doente, quant FROM EG
                WHERE MI.num_regiao=MA.num_regiao AND MI.num_concelho=MA.num_concelho AND (MI.q=quant OR MA.q=quant))
WHERE num_regiao = MI.num_regiao AND num_regiao=MA.num_regiao AND num_concelho = MI.num_concelho AND num_concelho=MA.num_concelho; 






WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant
FROM EG, (
    SELECT num_regiao, num_concelho, MAX(quant) AS maxQ
    FROM EG
    GROUP BY (num_regiao, num_concelho)
    ) AS M
WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.maxQ
ORDER BY (EG.num_regiao, EG.num_concelho);


WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant
FROM EG, (
    SELECT num_regiao, num_concelho, MIN(quant) AS minQ
    FROM EG
    GROUP BY (num_regiao, num_concelho)
    ) AS M
WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.minQ
ORDER BY (EG.num_regiao, EG.num_concelho);




WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

SELECT MN.num_regiao, MN.num_concelho, MN.num_doente, MN.quant, MX.num_doente, MX.quant
FROM (SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant
    FROM EG, (
        SELECT num_regiao, num_concelho, MAX(quant) AS maxQ
        FROM EG
        GROUP BY (num_regiao, num_concelho)
        ) AS M
    WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.maxQ) AS MX,
    (SELECT EG.num_regiao, EG.num_concelho, EG.num_doente, EG.quant
    FROM EG, (
        SELECT num_regiao, num_concelho, MIN(quant) AS minQ
        FROM EG
        GROUP BY (num_regiao, num_concelho)
        ) AS M
    WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.minQ) AS MN
WHERE MN.num_regiao=MX.num_regiao AND MN.num_concelho=MX.num_concelho
ORDER BY (MN.num_regiao, MN.num_concelho);






WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

SELECT EG.num_regiao, EG.num_concelho, MIX.minDoe, MIX.minQuant, MIX.maxDoe, MIX.maxQuant
FROM EG,
    (
        (SELECT EG.num_regiao, EG.num_concelho, EG.num_doente AS maxDoe, EG.quant AS maxQuant
            FROM EG, (
                SELECT num_regiao, num_concelho, MAX(quant) AS maxQ
                FROM EG
                GROUP BY (num_regiao, num_concelho)
                ) AS M
            WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.maxQ) AS MX 
    FULL OUTER JOIN
        (SELECT EG.num_regiao, EG.num_concelho, EG.num_doente AS minDoe, EG.quant AS minQuant
        FROM EG, (
            SELECT num_regiao, num_concelho, MIN(quant) AS minQ
            FROM EG
            GROUP BY (num_regiao, num_concelho)
            ) AS M
        WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.minQ) AS MN
    ON MN.num_regiao=MX.num_regiao AND MN.num_concelho=MX.num_concelho
    ) AS MIX
WHERE EG.num_regiao=MIX.num_regiao AND EG.num_concelho=MIX.num_concelho
ORDER BY (EG.num_regiao, EG.num_concelho);



WITH EG(num_regiao, num_concelho, num_doente, quant) AS
    (SELECT I.num_regiao, I.num_concelho, A.num_doente, A.quant
    FROM instituicao AS I, analise AS A
    WHERE I.nome = A.inst AND A.especialidade='Glicémia')

SELECT maxReg, maxConc, maxDoe, maxQuant, minDoe, minQuant
FROM  ((SELECT EG.num_regiao AS minReg, EG.num_concelho AS minConc, EG.num_doente AS minDoe, EG.quant AS minQuant
        FROM EG, (
            SELECT num_regiao, num_concelho, MIN(quant) AS minQ
            FROM EG
            GROUP BY (num_regiao, num_concelho)
            ) AS M
        WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.minQ) AS MN

    NATURAL JOIN
       
        (SELECT EG.num_regiao AS maxReg, EG.num_concelho AS maxConc, EG.num_doente AS maxDoe, EG.quant AS maxQuant
            FROM EG, (
                SELECT num_regiao, num_concelho, MAX(quant) AS maxQ
                FROM EG
                GROUP BY (num_regiao, num_concelho)
                ) AS M
            WHERE EG.num_regiao=M.num_regiao AND EG.num_concelho=M.num_concelho AND EG.quant=M.maxQ) AS MX 

    -- ON MN.minReg=MX.maxReg AND MN.minConc=MX.maxConc
    ) AS MIX

ORDER BY (maxReg, maxConc)
;
