fd = open('loop.sql', "w")

n_doente = 54321
for i in range(98):
    query = "insert into consulta values (12345, %s, '2020-12-01', 'Hospital Beatriz Ângelo');\n"
    n_doente += 1
    fd.write(query%n_doente)