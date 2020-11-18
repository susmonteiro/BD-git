import openpyxl, random
outSql = open("fill.sql", "w")

# Regioes
allNumR = [1, 2, 3, 4, 5]
outSql.write("-- Regioes\n")
outSql.write("insert into regiao values ('1', 'Norte', 3573000);\n")
outSql.write("insert into regiao values ('2', 'Centro', 2217000);\n")
outSql.write("insert into regiao values ('3', 'Lisboa', 4457358);\n")
outSql.write("insert into regiao values ('4', 'Alentejo', 234284);\n")
outSql.write("insert into regiao values ('5', 'Algarve', 438864);\n")

# Concelhos
outSql.write("\n-- Concelhos\n")
wb = openpyxl.load_workbook('concelhos.xlsx', data_only=True)
allNumC = []
allNumCedula = []
allNumDoente = []
for sName in wb.sheetnames:
    sheet = wb.get_sheet_by_name(sName)
    nRegiao = wb.sheetnames.index(sName)
    # [NomeConcelho, NumConcelho]
    if sName == "Folha1":
        continue
    for l in range(1, sheet.max_row+1):
        cell = "D" + str(l) 
        nomeC = sheet[cell].value.title()
        cell = "E" + str(l) 
        numC = sheet[cell].value
        allNumC.append(numC)

        # insert into concelho values (numC, numReg, nomeC, numHab)
        outSql.write("insert into concelho values (" + \
            str(numC) + ", " + str(nRegiao) + ", '" + str(nomeC).strip() + "', " + str(random.randint(10000, 1000000)) + ");\n")
wb.close()

# Instituicoes
outSql.write("\n-- Instituicoes\n")
instFile = open("inst.txt", "r")
allInstTypes = ['farmacia', 'laboratorio', 'clinica', 'hospital']
while instFile:
    line  = instFile.readline()
    if line == "":
        break
    # insert into instituicao values (nome, tipo, num_regiao, num_concelho)
    outSql.write("insert into instituicao values ('" + line[:-1] + "', " + \
        random.choice(allInstTypes) + ", " +  str(random.choice(allNumR)) + ", '" + str(random.choice(allNumC)) + "');\n")
        
instFile.close()


# Medico
outSql.write("\n-- Medicos\n")
namesFile = open("names.txt", "r")
nameLines = namesFile.readlines()
especialidadeFile = open("especialidades.txt", "r")
especialidadeLines = especialidadeFile.readlines()
for i in range(150):
    num_cedula = str(random.randint(1000, 9999))
    allNumCedula.append(num_cedula)
    outSql.write("insert into medico values (" + num_cedula + ", '" + random.choice(nameLines)[:-1] + "', '" + random.choice(especialidadeLines)[:-1] + "');\n")
    

# Consulta - num_cedula, num_doente, data, nome_instituicao
outSql.write("\n-- Consulta\n")
instFile = open("inst.txt", "r")
instLines = instFile.readlines()
for i in range(1000):
    num_doente = str(random.randint(1000, 9999))
    allNumDoente.append(num_doente)
    data = "2020-" + str(random.randint(1,13)) + "-" + str(random.randint(1,31))
    outSql.write("insert into medico values (" + str(random.choice(allNumCedula)) + ", " + num_doente + ", '" + data + "', '" + random.choice(instLines)[:-1] + "');\n")







instFile.close()
namesFile.close()
especialidadeFile.close()


outSql.close()
