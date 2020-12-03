--Eliminar tabelas que podem ter sido criadas anteriomente com o mesmo nome
drop table if exists d_tempo cascade;
drop table if exists d_instituicao cascade;
drop table if exists f_presc_venda cascade;
drop table if exists f_analise cascade;

--Definir as tabelas
create table d_tempo(
    id_tempo serial not null,
    dia int not null,
    dia_da_semana int not null,
    semana int not null,
    mes int not null,
    trimestre int not null,
    ano int not null,
    primary key(id_tempo)
);

create table d_instituicao(
    id_inst serial not null,
    nome varchar(50) not null,
    tipo varchar(25) not null,
    num_regiao int not null,
    num_concelho int not null,
    foreign key(nome) references instituicao(nome),
    foreign key(num_regiao) references regiao(num_concelho),
    foreign key(num_concelho) references concelho(num_concelho),
    primary key(id_inst)
);

create table f_presc_venda(
    id_presc_venda smallint not null, -- unique?
    id_medico int not null,
    num_doente int not null,
    id_data_registo int not null,
    id_inst int not null,
    substancia varchar(50) not null,
    quant int not null,
    foreign key(id_presc_venda) references prescricao_venda(num_venda), --??????
    foreign key(id_medico) references medico(num_cedula),
    foreign key(id_data_registo) references d_tempo(id_tempo),
    foreign key(id_inst) references d_instituicao(id_inst),
    primary key(id_presc_venda)
    --primary key(id_presc_venda, id_medico, id_data_registo, id_inst)
);

create table f_analise(
    id_analise smallint not null, 
    id_medico int not null,
    num_doente int not null,
    id_data_registo int not null,
    id_inst int not null,
    nome varchar(50) not null,
    quant int not null,
    foreign key(id_analise) references analise(num_analise),
    foreign key(id_medico) references medico(num_cedula),
    foreign key(id_data_registo) references d_tempo(id_tempo),
    foreign key(id_inst) references d_instituicao(id_inst),
    primary key(id_analise)
    --primary key(id_analise, id_medico, id_data_registo, id_inst)
);

--Carregar dados nas tabelas
insert into d_tempo(dia, dia_da_semana, semana, mes, trimestre, ano)
    select distinct 
    extract(DAY from _data) as dia, 
    extract(DOW from _data) as dia_da_semana,
    extract(WEEK from _data) as semana, 
    extract(MONTH from _data) as mes, 
    extract(QUARTER from _data) as trimestre,
    extract(YEAR from _data) as ano 
    from consulta
    order by dia, mes, ano;
    -- data da consulta ou ver data de analise e data de prescricao_venda???
    -- escrever no relatorio: assumimos que id_data_registo refere-se a _data em ambas as tabelas

insert into d_instituicao(nome, tipo, num_regiao, num_concelho)
    select nome, tipo, num_regiao, num_concelho from instituicao;

insert into f_presc_venda(id_presc_venda, id_medico, num_doente, id_data_registo, id_inst, substancia, quant)
    --?????

insert into f_analise(id_analise, id_medico, num_doente, id_data_registo, id_inst, nome, quant)
    --?????
