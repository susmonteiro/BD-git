-- clean prev tables
drop table regiao cascade;
drop table concelho cascade;
drop table instituicao cascade;
drop table medico cascade;
drop table consulta cascade;
drop table prescricao cascade;
drop table analise cascade;
drop table venda_farmacia cascade;
drop table prescricao_venda cascade;
drop table constants

create table constants( 
    nome_regiao char(16) not null,
    -- tipo_instituicao char(16) not null
);

-- grant select on constants to user;

insert into constants
    (nome_regiao)
values
    ('Norte'),
    ('Centro'),
    ('Lisboa'),
    ('Alentejo'),
    ('Algarve');


create table regiao(
    num_regiao serial not null unique,
--  num_regiao smallserial not null unique,
    nome char(50) not null check(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
    -- nome char(50) not null check(nome in (SELECT nome_regiao FROM constants),
    num_habitantes integer not null,
    constraint pk_regiao primary key(num_regiao)
    -- porque renomear a primary key?
);
-- grant select on regiao to user;

create table concelho(
    num_concelho serial not null,
    -- num_concelho serial not null unique,
    num_regiao serial not null, 
    -- num_regiao serial not null unique, 
    nome char(50) not null, 
    -- verificar se o nome do concelho é real
    num_habitantes integer not null,
    constraint fk_concelho_regiao foreign key(num_regiao) references regiao(num_regiao) ON DELETE CASCADE,
    constraint pk_concelho primary key(num_concelho, num_regiao)
);

create table instituicao(
    nome char(50) not null,
    -- nome char(50) not null unique,
    tipo char(50) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_regiao serial not null,
    num_concelho serial not null,
    constraint fk_instituicao_concelho foreign key(num_regiao, num_concelho) references concelho(num_regiao, num_concelho) ON DELETE CASCADE,
    constraint pk_instituicao primary key(nome);
);

create table medico(
    num_cedula serial not null unique,
    nome char(50) not null,
    especialidade char(50) not null,
    constraint pk_medico primary key(num_cedula)
);

create table consulta(
    num_cedula serial not null,
    -- num_cedula serial not null unique,
    num_doente serial not null unique,
    -- num_doente serial not null unique check ,
    _data date not null,
    -- data date not null unique check (DATENAME(DW, data) in ('Saturday', 'Sunday')),
    nome_instituicao char(50) not null,
    constraint fk_consulta_medico foreign key(num_cedula) references medico(num_cedula) ON DELETE CASCADE,
    constraint fk_consulta_instituicao foreign key(nome_instituicao) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_consulta primary key(num_cedula, num_doente, _data)
);

create table prescricao(
    num_cedula serial not null,
    num_doente serial not null,
    data date not null,
    substancia char(50) not null,
    quant integer not null,
    constraint fk_prescricao_consulta foreign key(num_cedula, num_doente, data) references conuslta(num_cedula, num_doente, data) ON DELETE CASCADE,
    constraint pk_prescricao primary key(num_cedula, num_doente, data, substancia)
);

create table analise(
    num_analise serial not null unique,
    especialidade char(50) not null,
    num_cedula serial not null,
    num_doente serial not null,
    data date not null,
    data_registo date not null, 
    nome char(50) not null, 
    quant integer not null, 
    inst char(50) not null,
    constraint fk_analise_consulta foreign key(num_cedula, num_doente, data) references consulta(num_cedula, num_doente, data) ON DELETE CASCADE,
    constraint fk_analise_instituicao foreign key(inst) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_analise primary key(num_analise)
);

create table venda_farmacia(
    num_venda serial not null unique,
    data_registo date not null,
    substancia char(50) not null,
    quant integer not null,
    preco integer not null,
    inst char(50) not null,
    constraint fk_venda_farmacia_instituicao foreign key(inst) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_venda_farmacia primary key(num_venda)
);

create table prescricao_venda(
    num_cedula serial not null,
    num_doente serial not null,
    data date not null,
    substancia char(50) not null,
    num_venda serial not null,
    constraint fk_prescricao_venda_venda_farmacia foreign key(num_venda) references venda_farmacia(num_venda) ON DELETE CASCADE,
    constraint fk_prescricao_venda_prescricao foreign key(num_cedula, num_doente, data, substancia) references prescricao(num_cedula, num_doente, data, substancia) ON DELETE CASCADE,
    constraint pk_prescricao_venda primary key(num_cedula, num_doente, data, substancia, num_venda)
);
