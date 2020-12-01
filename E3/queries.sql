-- query 1
WITH VV(num_regiao, num_concelho, nome, volume_vendas) AS
    (SELECT C.num_regiao, C.num_concelho, C.nome AS nome, SUM(V.preco) AS volume_vendas 
    roROM venda_farmacia AS V, instituicao AS I, concelho AS C
    WHERE V.data_registo=CURRENT_DATE AND  V.inst=I.nome AND I.num_concelho=C.num_concelho AND I.num_regiao=C.num_regiao
    GROUP BY C.num_regiao, C.num_concelho)
SELECT VV.num_regiao, VV.num_concelho, VV.nome
FROM VV, (
    SELECT MAX(volume_vendas) AS vmax
    FROM VV) AS T
WHERE VV.volume_vendas=T.vmax;

-- query 2
WITH PC(num_cedula, num_regiao, num_pres) AS
    (SELECT P.num_cedula, I.num_regiao, COUNT(*) AS num_pres
    FROM prescricao AS P, consulta AS C, instituicao AS I
    WHERE P.num_cedula=C.num_cedula AND P.num_doente=C.num_doente AND P._data=C._data
        AND C.nome_instituicao=I.nome AND P._data BETWEEN '2019-01-01' AND '2019-06-30'
    GROUP BY P.num_cedula, I.num_regiao)

SELECT PC.num_cedula, M.nome, R.num_regiao, R.nome AS regiao
FROM medico AS M, regiao AS R, PC, (
    SELECT num_regiao, MAX(num_pres) AS pmax
    FROM PC
    GROUP BY num_regiao) AS PCMAX
WHERE M.num_cedula=PC.num_cedula AND R.num_regiao=PC.num_regiao 
    AND PC.num_regiao=PCMAX.num_regiao AND PC.num_pres=PCMAX.pmax
ORDER BY R.num_regiao;

-- query 3
-- farmacias de Arouca
WITH FA(inst) AS
    (SELECT I.nome AS inst
    FROM instituicao AS I, regiao AS R, concelho AS C
    WHERE I.num_regiao=R.num_regiao AND I.num_concelho=C.num_concelho AND C.num_regiao=R.num_regiao 
        AND I.tipo='farmacia' AND C.nome='Arouca')
        
SELECT DISTINCT M.num_cedula, M.nome
FROM medico AS M
WHERE NOT EXISTS(
        (SELECT inst FROM FA)   -- farmacias em Arouca
        EXCEPT 
        (SELECT DISTINCT FA.inst    -- farmacias em Arouca que venderam aspirina este ano por medico
            FROM FA, venda_farmacia AS VF, prescricao_venda AS PV,
                EXTRACT(YEAR FROM V.data_registo) AS ano, EXTRACT(YEAR FROM CURRENT_DATE) AS ano_atual
            WHERE M.num_cedula=PV.num_cedula AND VF.num_venda=PV.num_venda AND VF.inst=FA.inst
                AND PV.substancia='Aspirina' AND ano=ano_atual)
);


-- WORKING no data checks
WITH FA(inst) AS
    (SELECT I.nome AS inst
    FROM instituicao AS I, regiao AS R, concelho AS C
    WHERE I.num_regiao=R.num_regiao AND I.num_concelho=C.num_concelho AND C.num_regiao=R.num_regiao 
        AND I.tipo='farmacia' AND C.nome='Arouca')
SELECT M.num_cedula
FROM medico AS M
WHERE NOT EXISTS(
        (SELECT inst FROM FA)
        EXCEPT 
        (SELECT DISTINCT FA.inst
            FROM venda_farmacia AS VF, prescricao_venda AS P, FA
            WHERE M.num_cedula=P.num_cedula AND VF.num_venda=P.num_venda AND VF.inst=FA.inst
                AND P.substancia='Aspirina')
);


-- returns farmacias onde nao foi vendido aspirina WORKING
WITH FA(inst) AS
    (SELECT I.nome AS inst
    FROM instituicao AS I, regiao AS R, concelho AS C
    WHERE I.num_regiao=R.num_regiao AND I.num_concelho=C.num_concelho AND C.num_regiao=R.num_regiao
        AND I.tipo='farmacia' AND C.nome='Arouca')
SELECT inst FROM FA
EXCEPT
    -- farmacias em Arouca que venderam aspirina
SELECT DISTINCT FA.inst
    FROM venda_farmacia AS VF, prescricao_venda AS P, FA
    WHERE VF.num_venda=P.num_venda AND VF.inst=FA.inst
        AND P.substancia='Aspirina';




SELECT distinct PV.num_cedula
FROM prescricao_venda AS PV
WHERE PV.substancia='Aspirina' AND NOT EXISTS (
    (SELECT nome
    FROM instituicao
    WHERE tipo='farmacia' AND num_regiao=2 AND num_concelho=104)
    EXCEPT
    (SELECT VFA.inst
    FROM prescricao_venda AS PVA, venda_farmacia AS VFA
    WHERE PV.num_venda=VFA.num_venda AND PV.num_cedula=PVA.num_cedula)
);





-- query 4
SELECT DISTINCT A.num_doente
FROM analise AS A,
    EXTRACT(YEAR FROM _data) AS ano, EXTRACT(YEAR FROM CURRENT_DATE) AS ano_atual, 
    EXTRACT(MONTH FROM _data) AS mes, EXTRACT(MONTH FROM CURRENT_DATE) AS mes_atual
WHERE mes = mes_atual AND ano = ano_atual AND NOT EXISTS
    (SELECT PV.num_doente
    FROM prescricao_venda AS PV, venda_farmacia AS VF,
        EXTRACT(YEAR FROM VF.data_registo) AS nano, EXTRACT(MONTH FROM VF.data_registo) AS nmes
    WHERE PV.num_doente=A.num_doente AND PV.num_venda=VF.num_venda
        AND nmes = mes_atual AND nano = ano_atual)
ORDER BY A.num_doente;

-- alternativa, dependendo se queremos analises so deste mes ou desde sempre

SELECT DISTINCT A.num_doente
FROM analise AS A
WHERE NOT EXISTS
    (SELECT PV.num_doente
    FROM prescricao_venda AS PV, venda_farmacia AS VF,
        EXTRACT(YEAR FROM CURRENT_DATE) AS ano_atual, EXTRACT(YEAR FROM VF.data_registo) AS ano, 
        EXTRACT(MONTH FROM CURRENT_DATE) AS mes_atual, EXTRACT(MONTH FROM VF.data_registo) AS mes
    WHERE PV.num_doente=A.num_doente AND PV.num_venda=VF.num_venda
        AND mes = mes_atual AND ano = ano_atual)
ORDER BY A.num_doente;


-- teste

SELECT distinct A.num_doente
FROM analise AS A,
    EXTRACT(YEAR FROM _data) AS ano, EXTRACT(YEAR FROM CURRENT_DATE) AS ano_atual, 
    EXTRACT(MONTH FROM _data) AS mes, EXTRACT(MONTH FROM CURRENT_DATE) AS mes_atual
WHERE mes = mes_atual AND ano = ano_atual
ORDER BY A.num_doente;


SELECT PV.num_doente
    FROM prescricao_venda AS PV, venda_farmacia AS VF,
    EXTRACT(YEAR FROM CURRENT_DATE) as ano_atual, EXTRACT(MONTH FROM CURRENT_DATE) AS mes_atual,
        EXTRACT(YEAR FROM VF.data_registo) AS nano, EXTRACT(MONTH FROM VF.data_registo) AS nmes
    WHERE PV.num_venda=VF.num_venda
        AND nmes = mes_atual AND nano = ano_atual
    ORDER BY num_doente;



-- nao interes- testar quais sao os doentes que nao tem prescricoes list
WITH VP(num_doente, num_cedula) AS
    (SELECT num_doente, num_cedula
    FROM prescricao_venda AS PV, venda_farmacia AS VF, EXTRACT(MONTH FROM VF.data_registo) AS mes, EXTRACT(MONTH FROM CURRENT_DATE)
    WHERE PV.num_venda=VF.num_venda)
SELECT distinct analise.num_doente, VP.num_cedula
FROM analise LEFT JOIN VP
ON analise.num_doente=VP.num_doente, 
EXTRACT(MONTH FROM _data) AS mes, EXTRACT(MONTH FROM CURRENT_DATE) AS mes_atual
WHERE mes=mes_atual
ORDER BY analise.num_doente;
