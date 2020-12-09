insert into instituicao values('testQ', 'farmacia', 3, 1106);
insert into instituicao values('testH', 'hospital', 3, 1107);
insert into medico values (8989, 'nome', 'especialidade');

insert into consulta values (8989, 901, '2020-01-9', 'testQ');
insert into consulta values (8989, 902, '2020-01-9', 'testH');
insert into consulta values (8989, 903, '2020-01-9', 'testQ');
insert into consulta values (8989, 904, '2020-01-9', 'testQ');
insert into consulta values (8989, 905, '2020-01-9', 'testQ');
insert into consulta values (8989, 906, '2020-01-9', 'testQ');
insert into consulta values (8989, 907, '2020-01-16', 'testQ');
insert into consulta values (8989, 908, '2020-01-16', 'testQ');
insert into consulta values (8989, 909, '2020-01-16', 'testH');
insert into consulta values (8989, 910, '2020-01-17', 'testQ');
insert into consulta values (8989, 911, '2020-02-06', 'testQ');
insert into consulta values (8989, 912, '2020-02-06', 'testQ');
insert into consulta values (8989, 913, '2019-02-06', 'testH');
insert into consulta values (8989, 914, '2019-02-06', 'testQ');
insert into consulta values (8989, 915, '2019-02-06', 'testQ');
insert into consulta values (8989, 916, '2019-02-06', 'testQ');



insert into prescricao values (8989, 901, '2020-01-9', 'Aspirina', 9);
insert into prescricao values (8989, 902, '2020-01-9', 'Aspirina', 9);
insert into prescricao values (8989, 903, '2020-01-9', 'Alirocumabe', 9);
insert into prescricao values (8989, 904, '2020-01-9', 'Alirocumabe', 9);
insert into prescricao values (8989, 905, '2020-01-9', 'Alirocumabe', 9);
insert into prescricao values (8989, 906, '2020-01-9', 'Alirocumabe', 9);
insert into prescricao values (8989, 907, '2020-01-16', 'Alirocumabe', 9);
insert into prescricao values (8989, 908, '2020-01-16', 'Alirocumabe', 9);
insert into prescricao values (8989, 909, '2020-01-16', 'Alirocumabe', 9);
insert into prescricao values (8989, 910, '2020-01-17', 'Alirocumabe', 9);
insert into prescricao values (8989, 911, '2020-02-06', 'Alirocumabe', 9);
insert into prescricao values (8989, 912, '2020-02-06', 'Alirocumabe', 9);
insert into prescricao values (8989, 913, '2019-02-06', 'Alirocumabe', 9);
insert into prescricao values (8989, 914, '2019-02-06', 'Alirocumabe', 9);
insert into prescricao values (8989, 915, '2019-02-06', 'Alirocumabe', 9);
insert into prescricao values (8989, 916, '2019-02-06', 'Aspirina', 9);


insert into venda_farmacia values (801, '2020-01-9', 'Aspirina', 3, 23, 'testQ');
insert into venda_farmacia values (802, '2020-01-9', 'Aspirina', 3, 23, 'testH');
insert into venda_farmacia values (803, '2020-01-9', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (804, '2020-01-9', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (805, '2020-01-9', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (806, '2020-01-9', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (807, '2020-01-16', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (808, '2020-01-16', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (809, '2020-01-16', 'Alirocumabe', 3, 23, 'testH');
insert into venda_farmacia values (810, '2020-01-17', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (811, '2020-02-06', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (812, '2020-02-06', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (813, '2019-02-06', 'Alirocumabe', 3, 23, 'testH');
insert into venda_farmacia values (814, '2019-02-06', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (815, '2019-02-06', 'Alirocumabe', 3, 23, 'testQ');
insert into venda_farmacia values (816, '2019-02-06', 'Aspirina', 3, 23, 'testQ');


insert into prescricao_venda values (8989, 901, '2012001-9', 'Aspirina', 801);
insert into prescricao_venda values (8989, 902, '2020-01-9', 'Aspirina', 802);
insert into prescricao_venda values (8989, 903, '2020-01-9', 'Alirocumabe', 803);
insert into prescricao_venda values (8989, 904, '2020-01-9', 'Alirocumabe', 804);
insert into prescricao_venda values (8989, 905, '2020-01-9', 'Alirocumabe', 805);
insert into prescricao_venda values (8989, 906, '2020-01-9', 'Alirocumabe', 806);
insert into prescricao_venda values (8989, 907, '2020-01-16', 'Alirocumabe', 807);
insert into prescricao_venda values (8989, 908, '2020-01-16', 'Alirocumabe', 808);
insert into prescricao_venda values (8989, 909, '2020-01-16', 'Alirocumabe', 809);
insert into prescricao_venda values (8989, 910, '2020-01-17', 'Alirocumabe', 810);
insert into prescricao_venda values (8989, 911, '2020-02-06', 'Alirocumabe', 811);
insert into prescricao_venda values (8989, 912, '2020-02-06', 'Alirocumabe', 812);
insert into prescricao_venda values (8989, 913, '2019-02-06', 'Alirocumabe', 813);
insert into prescricao_venda values (8989, 914, '2019-02-06', 'Alirocumabe', 814);
insert into prescricao_venda values (8989, 915, '2019-02-06', 'Alirocumabe', 815);
insert into prescricao_venda values (8989, 916, '2019-02-06', 'Aspirina', 816);
