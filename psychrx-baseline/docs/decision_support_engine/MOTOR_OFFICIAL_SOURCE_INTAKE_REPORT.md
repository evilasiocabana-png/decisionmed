# Motor Official Source Intake Report

## Objetivo

Registrar locators oficiais de fonte regulatoria para alimentar a pesquisa do Motor Farmacologico sem extrair ou validar conteudo clinico automaticamente.

## Fonte consultada

- DailyMed/FDA REST API: https://dailymed.nlm.nih.gov/dailymed/services/
- DailyMed public label pages: https://dailymed.nlm.nih.gov/dailymed/

## Resultado

- Medicamentos pesquisados: 83
- Fonte DailyMed/FDA localizada: 76
- Nao localizado em DailyMed/FDA nesta etapa: 7

## Limite

Esta etapa registra fonte oficial localizada. Ela nao transforma nenhum campo em recomendacao, nao extrai mecanismo, nao define dose para paciente e nao libera runtime clinico.

## Pendentes fora de DailyMed/FDA

- Agomelatina -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Bromazepam -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Dosulepina -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Levomepromazina -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Maprotilina -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Mianserina -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.
- Zopiclona -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.

## Proximo passo

Executar extracao campo a campo apenas quando houver fonte, secao, trecho revisavel e revisao editorial/cientifica.
