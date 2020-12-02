## Dúvidas:
- podemos usar o data type serial? 
> sim, mas nao e' suposto usarmos neste caso
- uniques redundantes
> nao usar
- é boa prática guardar, por exemplo, os tipos de região numa tabela de constantes?
> para as duas tabelas iniciais e' suposto ignorarmos as restricoes, portanto nao
- no lab 1 (bank.sql) porque fazer constraint para chaves, sendo que o nome não é utilizado?
> nao fazer (nao e' necessario)

- é suposto o populate é suposto não haver erros quando carregamos para a base de dados? 
- na query 2, como identificamos o doente e a regiao? num_cedula e num_regiao ou nome_medico e nome_regiao


- podemos editar (dar updade) de chaves primarias? como por exemplo o nome de uma instituicao
> não

- é suposto usar apenas a chave primaria de forma a obter, por exemplo, a analise a eliminar ou a editar?
> sim

- devemos usar o on delete/update cascade ou e' preferivel fazer a mao?

- caso a quantidade de venda seja superior a quantidade da prescricao para uma dada substancia e' suposto considerarmos que o doente nao tem prescricao?

## ToDo:
# Relatorio:
- explicar que substraímos a quantidade comprada à da prescricao quando é feita uma venda 
- explicar que quando a quantidade de venda é superior à da prescricao, então consideramos que o doente não tem prescricao