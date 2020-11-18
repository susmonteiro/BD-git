WITH VV(nome, volume_vendas) AS
    (SELECT C.nome AS nome, SUM(V.preco) AS volume_vendas 
    FROM venda_farmacia AS V, instituicao AS I, concelho AS C
    WHERE V.data_registo=CURRENT_DATE AND  V.inst=I.nome AND I.num_concelho=C.num_concelho AND I.num_regiao=C.num_regiao
    GROUP BY C.nome)
SELECT VV.nome
FROM VV, (
    SELECT MAX(volume_vendas) AS vmax
    FROM VV) AS T
WHERE VV.volume_vendas=T.vmax;