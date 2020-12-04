-- 1)

-- SELECT especialidade, ano, mes, COUNT(*)
-- FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
-- WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020
-- GROUP BY ROLLUP (especialidade, ano, mes) -- GROUPING SETS ((especialidade, mes, ano), (especialidade, mes), (especialidade), ())
-- ORDER BY especialidade;

-- ou

SELECT especialidade, ano, mes, COUNT(*)
FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020 -- confirmar inclusao do between <= ou < ?
GROUP BY CUBE (especialidade, ano, mes); 
ORDER BY (especialidade, ano, mes);

-- ou 

-- SELECT especialidade, ano, mes, COUNT(*)
-- FROM f_analise NATURAL JOIN analise NATURAL JOIN d_tempo
-- WHERE nome='Glicémia' AND ano BETWEEN 2017 AND 2020 -- confirmar inclusao do between <= ou < ?
-- GROUP BY GROUPING SETS ((especialidade, ano, mes), especialidade, ano, mes);





-- 2)

SELECT substancia, dia_da_semana, mes, COUNT(*), AVG(*)
FROM (
    SELECT id_inst, DI.num_regiao, num_concelho
    FROM d_instituicao AS DI, regiao AS R
    WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I NATURAL JOIN f_presc_venda NATURAL JOIN d_tempo
WHERE trimestre = 1 AND ano = 2020
GROUP BY GROUPING SETS (
    (substancia, dia_da_semana),
    ROLLUP (num_concelho, mes, dia_da_semana)
);