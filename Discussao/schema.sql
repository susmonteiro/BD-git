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

create table regiao(
    num_regiao smallint not null,
    nome varchar(128) not null unique,
    num_habitantes integer not null,
    primary key(num_regiao)
);

create table concelho(
    num_concelho int not null,
    num_regiao smallint not null,
    nome varchar(128) not null,
    num_habitantes integer not null,
    foreign key(num_regiao) references regiao(num_regiao),
    primary key(num_concelho, num_regiao)
);

create table instituicao(
    nome varchar(128) not null,
    tipo varchar(128) not null check(tipo in ('farmacia', 'laboratorio', 'clinica', 'hospital')),
    num_regiao int not null,
    num_concelho smallint not null,
    foreign key(num_regiao, num_concelho) references concelho(num_regiao, num_concelho),
    primary key(nome)
);

create table medico(
    num_cedula int not null,
    nome varchar(128) not null,
    especialidade varchar(128) not null,
    primary key(num_cedula)
);

create table consulta(
   num_cedula int not null,
   num_doente int not null,
   _data date not null check (EXTRACT(DOW FROM _data) not in (6,7)), -- ('Saturday', 'Sunday')
   nome_instituicao varchar(128) not null,
   foreign key(num_cedula) references medico(num_cedula),
   foreign key(nome_instituicao) references instituicao(nome),
   primary key(num_cedula, num_doente, _data),
   constraint RI_2 unique (num_doente, _data, nome_instituicao)
);

create table prescricao(
   num_cedula int not null,
   num_doente int not null,
   _data date not null,
   substancia varchar(64) not null,
   quant integer not null,
   foreign key(num_cedula, num_doente, _data) references consulta(num_cedula, num_doente, _data),
   primary key(num_cedula, num_doente, _data, substancia)
);

create table analise(
   num_analise smallint not null,
   especialidade varchar(128) not null,
   num_cedula int,
   num_doente int,
   _data date,
   data_registo date not null,
   nome varchar(128) not null,
   quant integer not null,
   inst varchar(128) not null,
   foreign key(num_cedula, num_doente, _data) references consulta(num_cedula, num_doente, _data),
   foreign key(inst) references instituicao(nome),
   primary key(num_analise),
   constraint null_consulta check((num_cedula IS null AND num_doente IS null 
    AND _data IS null) OR (num_cedula IS not null AND num_doente IS not null AND _data IS NOT null))
);

create table venda_farmacia(
   num_venda smallint not null,
   data_registo date not null,
   substancia varchar(64) not null,
   quant integer not null,
   preco integer not null,
   inst varchar(128) not null,
   foreign key(inst) references instituicao(nome),
   primary key(num_venda)
);

create table prescricao_venda(
   num_cedula smallint not null,
   num_doente smallint not null,
   _data date not null,
   substancia varchar(64) not null,
   num_venda smallint not null,
   foreign key(num_venda) references venda_farmacia(num_venda),
   foreign key(num_cedula, num_doente, _data, substancia) references prescricao(num_cedula, num_doente, _data, substancia),
   primary key(num_cedula, num_doente, _data, substancia, num_venda)
);
