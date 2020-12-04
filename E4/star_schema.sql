--Eliminar tabelas que podem ter sido criadas anteriomente com o mesmo nome
drop table if exists d_tempo cascade;
drop table if exists d_instituicao cascade;
drop table if exists f_presc_venda cascade;
drop table if exists f_analise cascade;

--Adicionar restricao
ALTER TABLE prescricao_venda
drop CONSTRAINT if exists Unique_num_venda;

ALTER TABLE prescricao_venda
ADD CONSTRAINT Unique_num_venda UNIQUE(num_venda);

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
    nome varchar(128) not null,
    tipo varchar(128) not null,
    num_regiao int not null,
    num_concelho int not null,
    foreign key(nome) references instituicao(nome),
    foreign key(num_regiao) references regiao(num_regiao),
    foreign key(num_regiao, num_concelho) references concelho(num_regiao, num_concelho),
    primary key(id_inst)
);

create table f_presc_venda(
    id_presc_venda smallint not null, -- unique?
    id_medico int not null,
    num_doente int not null,
    id_data_registo int not null,
    id_inst int not null,
    substancia varchar(64) not null,
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
    nome varchar(128) not null,
    quant int not null,
    foreign key(id_analise) references analise(num_analise),
    foreign key(id_medico) references medico(num_cedula),
    foreign key(id_data_registo) references d_tempo(id_tempo),
    foreign key(id_inst) references d_instituicao(id_inst),
    primary key(id_analise)
    --primary key(id_analise, id_medico, id_data_registo, id_inst)
);
