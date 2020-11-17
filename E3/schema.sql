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
-- drop table nome_regiao_const;
-- drop table nome_instituicao_const;


-- create table nome_regiao_const( 
-- 	nome varchar(16) not null
-- );

-- -- grant select on nome_regiao_const to user;

-- insert into nome_regiao_const
-- values
-- 	('Norte'),
-- 	('Centro'),
-- 	('Lisboa'),
-- 	('Alentejo'),
-- 	('Algarve');



-- create table nome_instituicao_const( 
-- 	nome varchar(16) not null
-- );

-- -- grant select on nome_instituicao_const to user;

-- insert into nome_instituicao_const
-- values
-- 	('farmacia'),
-- 	('laboratorio'),
-- 	('clinica'),
-- 	('hospital');



create table regiao(
--     num_regiao smallint not null unique,
	num_regiao smallint not null unique,
	-- nome char(50) not null check(nome in ('Norte', 'Centro', 'Lisboa', 'Alentejo', 'Algarve')),
	nome varchar(50) not null unique,
	num_habitantes integer not null,
	constraint pk_regiao primary key(num_regiao)
    	-- check (regiao_valida(nome) = 'True')
    -- porque renomear a primary key?
);
-- grant select on regiao to user;

create table concelho(
	-- num_concelho smallint not null,
	num_concelho smallint not null unique,
	-- num_regiao smallint not null, 
	num_regiao smallint not null unique, 
	nome varchar(50) not null unique, 
	-- verificar se o nome do concelho é real
	num_habitantes integer not null,
	constraint fk_concelho_regiao foreign key(num_regiao) references regiao(num_regiao) ON DELETE CASCADE ON UPDATE CASCADE,
	constraint pk_concelho primary key(num_concelho, num_regiao)
);

create table instituicao(
    nome varchar(50) not null,
    -- nome char(50) not null unique,
    tipo varchar(50) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_regiao smallint not null,
    num_concelho smallint not null,
    constraint fk_instituicao_concelho foreign key(num_regiao, num_concelho) references concelho(num_regiao, num_concelho) ON DELETE CASCADE,
    constraint pk_instituicao primary key(nome)
);

create table medico(
    num_cedula smallint not null unique,
    nome varchar(50) not null,
    especialidade varchar(50) not null,
    constraint pk_medico primary key(num_cedula)
);

create table consulta(
    num_cedula smallint not null,
    -- num_cedula smallint not null unique,
    -- num_doente smallint not null unique,
    num_doente smallint not null unique,
    _data date not null,
    -- _data date not null unique check (DATENAME(DW, _data) not in ('Saturday', 'Sunday')),
    nome_instituicao varchar(50) not null,
    constraint fk_consulta_medico foreign key(num_cedula) references medico(num_cedula) ON DELETE CASCADE,
    constraint fk_consulta_instituicao foreign key(nome_instituicao) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_consulta primary key(num_cedula, num_doente, _data)
    -- check (SELECT A.num_doente, A.nome_instituicao, A._data 
    --         FROM consulta AS A 
    --         WHERE num_doente!=A.num_doente OR _data!=A._data OR nome_instituicao!=A.nome_instituicao)
);

create table prescricao(
    num_cedula smallint not null,
    num_doente smallint not null,
    _data date not null,
    substancia varchar(50) not null,
    quant integer not null,
    constraint fk_prescricao_consulta foreign key(num_cedula, num_doente, _data) references consulta(num_cedula, num_doente, _data) ON DELETE CASCADE,
    constraint pk_prescricao primary key(num_cedula, num_doente, _data, substancia)
);

create table analise(
    num_analise smallint not null unique,
    especialidade varchar(50) not null ,
    num_cedula smallint,
    num_doente smallint,
    _data date,
    data_registo date not null, 
    nome varchar(50) not null, 
    quant integer not null, 
    inst varchar(50) not null,
    constraint fk_analise_consulta foreign key(num_cedula, num_doente, _data) references consulta(num_cedula, num_doente, _data) ON DELETE CASCADE,
    constraint fk_analise_instituicao foreign key(inst) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_analise primary key(num_analise)
);

create table venda_farmacia(
    num_venda smallint not null unique,
    data_registo date not null,
    substancia varchar(50) not null,
    quant integer not null,
    preco integer not null,
    inst varchar(50) not null,
    constraint fk_venda_farmacia_instituicao foreign key(inst) references instituicao(nome) ON DELETE CASCADE,
    constraint pk_venda_farmacia primary key(num_venda)
);

create table prescricao_venda(
    num_cedula smallint not null,
    num_doente smallint not null,
    _data date not null,
    substancia varchar(50) not null,
    num_venda smallint not null,
    constraint fk_prescricao_venda_venda_farmacia foreign key(num_venda) references venda_farmacia(num_venda) ON DELETE CASCADE,
    constraint fk_prescricao_venda_prescricao foreign key(num_cedula, num_doente, _data, substancia) references prescricao(num_cedula, num_doente, _data, substancia) ON DELETE CASCADE,
    constraint pk_prescricao_venda primary key(num_cedula, num_doente, _data, substancia, num_venda)
);



/* FUNCTIONS */
/* 
create function regiao_valida(nome_regiao varchar(50))
	returns varchar(5)
as
$$
begin
	if exists (SELECT A.nome_regiao FROM nome_regiao_const AS A WHERE nome_regiao=A.nome_regiao) then
		return 'True'
	return 'False'
end
$$ language plpgsql; */