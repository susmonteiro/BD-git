-- RI-100
create or replace function medico_100_consultas_proc()
returns trigger as
$$
declare num_consultas integer;
begin

    SELECT count(*) into num_consultas
    FROM (
        SELECT num_cedula, nome_instituicao, _year, _week
        FROM consulta, 
        EXTRACT(YEAR FROM _data) AS _year, EXTRACT(WEEK FROM _data) AS _week,
        EXTRACT(YEAR FROM new._data) AS newYear, EXTRACT(WEEK FROM new._data) AS newWeek
        WHERE num_cedula = new.num_cedula AND nome_instituicao = new.nome_instituicao AND _year = newYear AND _week = newWeek
        ) AS A;
    
    if num_consultas >= 100 then
        raise exception 'O medico % ja excedeu o limite de consultas para esta semana na instituicao %', new.num_cedula, new.nome_instituicao;
    else
        return new;
    end if;

end
$$language plpgsql;

drop trigger medico_100_consultas on consulta;
create trigger medico_100_consultas before insert on consulta
for each row execute procedure medico_100_consultas_proc();


--RI-analise
