# Introdução

Desenvolvimento de uma plataforma digital - ODISSEIA - para recolha, gestão e armazenamento de dados clínicos. Esta plataforma permite realizar análises sobre os dados, com aplicações de produção de estatísticas e de data-mining.

# Índice
- [Introdução](#introdução)
- [Parte 1](#parte-1)
    - [Descrição do Domínio](#descrição-do-domínio)
    - [Trabalho a desenvolver](#trabalho-a-desenvolver)
    - [Relatório](#relatório)

# Parte 1

Propor um modelo Entidade-Associação com as correspondestes Restrições de Integridade adequado ao domínio apresentado

## Descrição do Domínio

Dados acumulados percebidos como **observações** - caracterizadas por:
- identificador de observação
- o "número" do Cartão de Cidadão do doente
- data de registo na base de dados (sempre a mesma ou posterior até 3 dias à de observação)
- nome da grandeza observada
- data de observação
- valor (sempre numéricos!)

Exemplo:

    <435, 00098765 4 ZB4, 2020-10-10,"colesterol total — mg/dL”, 2020-10-10, 220>

Uma observação pode ser o resultado de uma:
- **medição** - pode ser:
    - clínica (**consulta**) - decorre sempre numa dada instituição de cuidados de saúde (nome, morada) e com um médico (cédula profissional, nome, especialidade)
        > Numa consulta nem sempre é registada uma **observação** (pode ser apenas para estender uma prescrição) e também podem ser feitas múltiplas observações numa consulta
    - laboratorial/exame médico (**análise**) - tem sempre uma especialidade, decorre também sempre numa unidade de saúde, de acordo com um protocolo (nº, descrição, data de homologação pela entidade reguladora da saúde), e são feitas por um técnico (nome, especialidade, nº diploma) ou por um médico.
        > É obrigatório que cada técnico tenha um diploma de uma escola de formação, sendo os nº de diploma atribuídos pelas escolas (nome, morada)

> Apenas os médicos podem dar consultas e os médicos de uma especialidade não podem fazer análises de outra especialidade que não a sua

- **intervenção** - pode ser:
    - **cirúrgica**
    - **farmacêutica** (administração de um medicamento) - sempre feita no contexto de uma consulta e regista duas datas de intervenção (definição de um período temporal)

## Trabalho a desenvolver

1. Desenhar um **modelo Entidade-Associação**
2. Identificar as situações incoerentes no domínio do problema, mas permitidas no modelo E-A apresentado e definir um conjunto de **Restrições de Integridade** de forma a proibir as situações incoerentes

## Relatório

### Avaliação

- 16 valores - modelo Entidade-Associação
- 4 valores - Restrições de Integridade 

### Formato

- folha de rosto:
    - “Projeto de Bases de Dados - Parte 1"
    - nome e número dos alunos
    - percentagem relativa de contribuição e esforço em horas de cada elemento
    - número do grupo
    - turno
    - nome do docente de laboratório
- máximo de 2 páginas
- entregue em duas versões:
    - digital, em formato pdf, com o nome `entrega-01-GG.pdf`, onde `GG` é o número do grupo - entregar no Fénix
    - papel - entregar ao docente no laboratório seguinte

