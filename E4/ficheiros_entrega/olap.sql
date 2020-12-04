-- 1)

SELECT especialidade, ano, mes, COUNT(*)
FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020
GROUP BY CUBE (especialidade, ano, mes); 
ORDER BY (especialidade, ano, mes);

-- ou 

-- SELECT especialidade, ano, mes, COUNT(*)
-- FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
-- WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020
-- GROUP BY GROUPING SETS ((especialidade, ano, mes), especialidade, ano, mes);


-- 2)

WITH T (id_tempo, num_concelho, substancia, c) AS (
    SELECT id_tempo, num_concelho, substancia, COUNT(*) as c 
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I 
        NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
    WHERE trimestre = 1 and ano = 2020
    GROUP BY (id_tempo, num_concelho, substancia)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);