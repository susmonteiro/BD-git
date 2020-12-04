--Carregar dados nas tabelas
INSERT INTO d_tempo(dia, dia_da_semana, semana, mes, trimestre, ano)
    SELECT DISTINCT 
        extract(DAY FROM _data) AS dia, 
        extract(DOW FROM _data) AS dia_da_semana,
        extract(WEEK FROM _data) AS semana, 
        extract(MONTH FROM _data) AS mes, 
        extract(QUARTER FROM _data) AS trimestre,
        extract(YEAR FROM _data) AS ano 
    FROM (
        SELECT _data FROM analise
        UNION
        SELECT _data FROM prescricao_venda) AS DATAS --equivalente as datas da relacao consulta
    ORDER BY dia, mes, ano;

INSERT INTO d_instituicao(nome, tipo, num_regiao, num_concelho)
    SELECT nome, tipo, num_regiao, num_concelho FROM instituicao;

INSERT INTO f_presc_venda(id_presc_venda, id_medico, num_doente, id_data_registo, id_inst, substancia, quant)
    SELECT 
        P.num_venda, 
        P.num_cedula, 
        P.num_doente, 
        T.id_tempo, 
        I.id_inst, 
        P.substancia, 
        V.quant
    FROM 
        prescricao_venda AS P, venda_farmacia AS V, d_tempo as T, d_instituicao as I
    WHERE
        V.num_venda = P.num_venda AND
        extract(DAY FROM P._data) = T.dia AND
        extract(MONTH FROM P._data) = T.mes AND
        extract(YEAR FROM P._data) = T.ano AND
        V.inst = I.nome;
        
        
INSERT INTO f_analise(id_analise, id_medico, num_doente, id_data_registo, id_inst, nome, quant)
    SELECT 
        A.num_analise,
        A.num_cedula,
        A.num_doente,
        T.id_tempo,
        I.id_inst,
        A.nome,
        A.quant
    FROM
        analise AS A, d_tempo AS T, d_instituicao AS I
    WHERE
        extract(DAY FROM A._data) = T.dia AND
        extract(MONTH FROM A._data) = T.mes AND
        extract(YEAR FROM A._data) = T.ano AND
        A.inst = I.nome;