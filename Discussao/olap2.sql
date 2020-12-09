insert into regiao values (1, 'f', 1);
-- insert into concelho values (2, 1, 'c', 123);
-- insert into instituicao values ('i', 'farmacia', 1, 2);
-- insert into medico values (3, 'e', 'g');
-- insert into consulta  values (3, 4, '2020-01-01', 'i');
-- insert into prescricao values (3, 4, '2020-01-01', 'subs', 1);
-- insert into venda_farmacia values (1, '2020-01-01', 'subs', 1, 7, 'i');
-- insert into prescricao_venda values (3, 4, '2020-01-01', 'subs', 1);
-- insert into venda_farmacia values (2, '2020-01-01', 'subs', 1, 7, 'i');
-- insert into prescricao_venda values (3, 4, '2020-01-01', 'subs', 2);
-- insert into consulta  values (3, 4, '2020-01-08', 'i');
-- insert into prescricao values (3, 4, '2020-01-08', 'subs', 1);
-- insert into venda_farmacia values (3, '2020-01-08', 'subs', 1, 7, 'i');
-- insert into prescricao_venda values (3, 4, '2020-01-08', 'subs', 3);


-- SELECT id_tempo, num_concelho, substancia
--      FROM (
--          SELECT id_inst, DI.num_regiao, num_concelho
--          FROM d_instituicao AS DI, regiao AS R
--          WHERE DI.num_regiao = R.num_regiao AND R.nome='f') AS I, f_presc_venda as F, d_tempo as T
--      WHERE trimestre = 1 and ano = 2020 and I.id_inst=F.id_inst and F.id_data_registo=T.id_tempo;



WITH T (id_tempo, num_concelho, substancia, c) AS (
    SELECT id_tempo, num_concelho, substancia, COUNT(*) as c 
    FROM (
        SELECT id_inst, DI.num_regiao, num_concelho
        FROM d_instituicao AS DI, regiao AS R
        WHERE DI.num_regiao = R.num_regiao AND R.nome='Lisboa') AS I, 
        f_presc_venda AS F, d_tempo AS T
    WHERE trimestre = 1 and ano = 2020 and I.id_inst=F.id_inst and F.id_data_registo=T.id_tempo
    GROUP BY (id_tempo, num_concelho, substancia)
)
SELECT substancia, num_concelho, dia_da_semana, mes, SUM(c), AVG(c)
FROM T NATURAL JOIN d_tempo
GROUP BY ROLLUP (substancia, num_concelho, dia_da_semana, mes)
ORDER BY (substancia, num_concelho, dia_da_semana, mes);