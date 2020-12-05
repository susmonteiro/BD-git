-- 1)

-- SELECT especialidade, ano, mes, COUNT(*)
-- FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
-- WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020
-- GROUP BY ROLLUP (especialidade, ano, mes) -- GROUPING SETS ((especialidade, mes, ano), (especialidade, mes), (especialidade), ())
-- ORDER BY especialidade;

-- ou

SELECT especialidade, ano, mes, COUNT(*)
FROM f_analise NATURAL JOIN analise, d_tempo
WHERE nome='Glicémia' AND id_data_registo=id_tempo AND ano BETWEEN 2017 AND 2020
GROUP BY CUBE (especialidade, ano, mes) 
ORDER BY (especialidade, ano, mes);

-- ou 

-- SELECT especialidade, ano, mes, COUNT(*)
-- FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
-- WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020
-- GROUP BY GROUPING SETS ((especialidade, ano, mes), especialidade, ano, mes);




-- 2)


SELECT substancia, dia_da_semana, mes, num_concelho, SUM(c), AVG(c)
FROM
    (SELECT substancia, dia_da_semana, mes, num_concelho, COUNT(*) AS c
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    WHERE trimestre = 4 AND ano = 2020
    GROUP BY (substancia, id_tempo, num_concelho)
    ) AS A
GROUP BY GROUPING SETS (
    (substancia, dia_da_semana),
    ROLLUP (substancia, num_concelho, mes, dia_da_semana))
ORDER BY (substancia, dia_da_semana, mes);




WITH T (id_tempo, num_concelho, substancia, c) AS (
    SELECT id_tempo, num_concelho, substancia, COUNT(*) as c 
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I 
        NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    WHERE trimestre = 1 and ano = 2019
    GROUP BY (id_tempo, num_concelho, substancia)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);



-- obter quantidade total de prescricoes por dia da semana e mes no primeiro trimestre
SELECT dia_da_semana, mes, COUNT(*) 
FROM f_presc_venda NATURAL JOIN d_tempo 
WHERE trimestre = 1 
GROUP BY (dia_da_semana, mes) 
ORDER BY (dia_da_semana, mes);

-- obter quantidade total de prescricoes por dia da semana, mes e concelho no primeiro trimestre
WITH T (id_tempo, c) AS (
    SELECT id_tempo, COUNT(*) as c 
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I 
        NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    WHERE trimestre = 1 and ano = 2019
    GROUP BY (id_presc_venda, id_tempo)
)
SELECT dia_da_semana, mes, num_concelho, substancia, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo NATURAL JOIN f_presc_venda NATURAL JOIN d_instituicao 
GROUP BY (dia_da_semana, mes, num_concelho, substancia) 
ORDER BY (dia_da_semana, mes, num_concelho, substancia);


WITH T (id_tempo, c) AS (
   SELECT DISTINCT id_tempo, COUNT(*) as c
   FROM (
        SELECT id_inst
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa'
        ) AS I
        NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
   WHERE trimestre = 1 and ano = 2019
   GROUP BY (id_presc_venda, id_tempo)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo NATURAL JOIN f_presc_venda NATURAL JOIN d_instituicao
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);

-- CORRETOOOO

WITH T (id_data_registo, num_concelho, substancia, c) AS (
   SELECT id_data_registo, num_concelho, substancia, COUNT(*) as c
   FROM (
       SELECT id_inst, DI.num_regiao, num_concelho
       FROM d_instituicao AS DI, regiao AS R
       WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I, f_presc_venda AS F, d_tempo AS DT
   WHERE I.id_inst=F.id_inst AND F.id_data_registo=DT.id_tempo -- AND trimestre = 4 and ano = 2020
   GROUP BY (id_data_registo, num_concelho, substancia)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T, d_tempo AS DT
WHERE T.id_data_registo=DT.id_tempo
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);


SELECT COUNT(*) as c
   FROM (
       SELECT DISTINCT id_inst, DI.num_regiao, num_concelho
       FROM d_instituicao AS DI, regiao AS R
       WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I
       NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
   WHERE trimestre = 1 and ano = 2019;


select * from f_presc_venda as F, d_instituicao as I, d_tempo as DT 
where F.id_inst=I.id_inst and F.id_data_registo=DT.id_tempo 
    and trimestre=4 and num_regiao=3 and substancia='Aspirina';








-- check populate
 SELECT substancia, dia_da_semana, ano, mes, trimestre
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    ;



-- test igualdade


    (WITH T (id_tempo, num_concelho, substancia, c) AS (
        SELECT id_tempo, num_concelho, substancia, COUNT(*) as c 
        FROM (
            SELECT id_inst, DI.num_regiao, num_concelho
            FROM d_instituicao AS DI, regiao AS R
            WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I 
            NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
        WHERE trimestre = 1 and ano = 2019
        GROUP BY (id_tempo, num_concelho, substancia)
    )
    SELECT substancia, dia_da_semana, mes, num_concelho, SUM(c), AVG(c)
    FROM T NATURAL JOIN d_tempo
    GROUP BY GROUPING SETS (
        (substancia, dia_da_semana),
        ROLLUP (substancia, num_concelho, mes, dia_da_semana))
    ORDER BY (substancia, dia_da_semana, mes))

    EXCEPT

    (SELECT substancia, dia_da_semana, mes, num_concelho, SUM(c), AVG(c)
FROM
    (SELECT substancia, dia_da_semana, mes, num_concelho, COUNT(*) AS c
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    WHERE trimestre = 1 AND ano = 2019
    GROUP BY (substancia, id_tempo, num_concelho)
    ) AS A
GROUP BY GROUPING SETS (
    (substancia, dia_da_semana),
    ROLLUP (substancia, num_concelho, mes, dia_da_semana))
ORDER BY (substancia, dia_da_semana, mes)) ;


----------------------------------------------------------
----------------------------------------------------------
----------------------------------------------------------


select id_data_registo, num_concelho, substancia from f_presc_venda as F, d_instituicao as I, d_tempo as DT 
where F.id_inst=I.id_inst and F.id_data_registo=DT.id_tempo 
    and trimestre=4 and num_regiao=3;




-- CORRETOOOO

WITH T (id_tempo, num_concelho, substancia, c) AS (
   SELECT id_tempo, num_concelho, substancia, COUNT(*) as c
   FROM (
       SELECT id_inst, DI.num_regiao, num_concelho
       FROM d_instituicao AS DI, regiao AS R
       WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I, f_presc_venda AS F, d_tempo AS DT
   WHERE I.id_inst=F.id_inst AND F.id_data_registo=DT.id_tempo -- AND trimestre = 4 and ano = 2020
   GROUP BY (id_tempo, num_concelho, substancia)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);



select substancia, COUNT(*) from prescricao_venda as P, consulta as C, instituicao as I
where P.num_cedula=C.num_cedula AND P.num_doente=C.num_doente AND P.num_doente=C.num_doente
    AND C.nome_instituicao=I.nome AND I.num_regiao=3
GROUP BY substancia;
-- 407 rows

