# MISSÃO — MATRIZ FARMACOLÓGICA V2 COMPLETA NO APP

## Objetivo

Evoluir a matriz atual de 46 medicamentos para uma **Versão 2 ampliada da psiquiatria**, mantendo integralmente o padrão de informação já existente para os 46 fármacos e entregando tudo **funcionando no aplicativo**, não apenas em documentação.

A V2 deve adicionar os principais grupos ainda ausentes, especialmente benzodiazepínicos, hipnóticos, TDAH, dependência química, antipsicóticos modernos e fármacos para demência.

## Regra de preservação

Não remover nem degradar os 46 medicamentos já existentes.

Todos os novos medicamentos devem possuir, no mínimo, exatamente as mesmas três camadas que já existem para os 46:

1. **Dose — efeito**
2. **Uso por doença/contexto clínico**
3. **Fonte/referência rastreável**

Além disso, devem participar do ranking, do Clinical Phenotype Filter e do Disease Use Filter conforme seu papel terapêutico.

---

# 1. Medicamentos a adicionar na V2

## A. Benzodiazepínicos

1. Alprazolam
2. Bromazepam
3. Clobazam
4. Clonazepam
5. Diazepam
6. Lorazepam
7. Midazolam
8. Oxazepam
9. Temazepam

## B. Hipnóticos não benzodiazepínicos

10. Zolpidem
11. Zopiclona
12. Eszopiclona

## C. Ansiolítico não benzodiazepínico

13. Buspirona

## D. TDAH

14. Metilfenidato de liberação imediata
15. Metilfenidato de liberação prolongada
16. Lisdexanfetamina
17. Atomoxetina
18. Guanfacina XR
19. Clonidina

## E. Antipsicóticos modernos e relevantes

20. Paliperidona
21. Ziprasidona
22. Cariprazina
23. Brexpiprazol
24. Asenapina
25. Amissulprida
26. Sulpirida

## F. Dependência química

27. Acamprosato
28. Dissulfiram
29. Naloxona
30. Buprenorfina
31. Metadona

## G. Cognição/demência

32. Donepezila
33. Rivastigmina
34. Galantamina
35. Memantina

## H. Agitação e urgência psiquiátrica

36. Prometazina
37. Droperidol

Total esperado da V2: **83 registros principais** contando os 46 atuais + 37 novos.

Observação: formulações diferentes podem compartilhar entidade farmacológica central, mas devem preservar diferenças de liberação, indicação, dose e segurança quando isso muda a conduta. Não duplicar mecanismo como se fosse outro princípio ativo.

---

# 2. Estrutura obrigatória para cada novo medicamento

Cada registro deve conter:

## 2.1 Identidade

- nome canônico;
- aliases e nomes de formulação;
- classe;
- subclasse;
- via(s) contemplada(s);
- formulação;
- liberação imediata/prolongada quando aplicável.

## 2.2 Dose — efeito

Registrar faixas clinicamente relevantes sem inventar mudança receptorial onde ela não existe.

Cada faixa deve conter:

- dose mínima;
- dose máxima;
- unidade;
- frequência;
- papel clínico da faixa;
- efeito predominante;
- mecanismo relacionado;
- se a fronteira é rígida ou didática;
- força da evidência;
- alertas específicos;
- fonte da dose;
- fonte do mecanismo.

Tipos permitidos:

- `RECEPTOR_SHIFT`
- `CLINICAL_EFFECT_SHIFT`
- `INDICATION_SHIFT`
- `EXPOSURE_ONLY`
- `SERUM_LEVEL_GUIDED`
- `INSUFFICIENT_EVIDENCE`

Não afirmar que uma dose “muda o mecanismo” sem fonte primária ou farmacodinâmica específica.

## 2.3 Uso por doença/contexto

Para cada medicamento, mapear de forma explícita:

- doença ou síndrome;
- fase clínica;
- papel terapêutico;
- status regulatório;
- nível de evidência;
- elegibilidade para ranking;
- situação de bloqueio;
- observações clínicas.

Papéis obrigatórios:

- `TRATAMENTO_PRINCIPAL`
- `POTENCIALIZACAO`
- `ADJUVANTE`
- `MANUTENCAO`
- `RESGATE`
- `CURTO_PRAZO`
- `OFF_LABEL_COM_EVIDENCIA`
- `EVIDENCIA_LIMITADA`
- `RESTRITO`
- `NAO_RECOMENDADO`

## 2.4 Segurança

Incluir pelo menos:

- sedação;
- risco de dependência;
- tolerância;
- síndrome de retirada;
- risco respiratório;
- interação com álcool/opioides;
- risco de queda;
- risco cognitivo;
- QT quando aplicável;
- metabolismo/interações relevantes;
- ajuste renal/hepático quando necessário;
- gestação/lactação quando crítico;
- risco de abuso/desvio;
- necessidade de monitorização especial.

## 2.5 Fontes

Cada afirmação deve apontar para a fonte correspondente.

Prioridade:

1. bula profissional Anvisa;
2. FDA Prescribing Information / DailyMed;
3. EMA/SmPC;
4. diretrizes oficiais e consensos reconhecidos;
5. estudos primários de farmacodinâmica, ocupação receptorial ou farmacocinética;
6. Stahl, Goodman & Gilman, Maudsley e BNF como apoio secundário.

Cada fonte precisa informar o que sustenta:

- dose;
- indicação;
- mecanismo;
- segurança;
- monitorização;
- status regulatório.

Não usar apenas referências genéricas sem ligação com a afirmação.

---

# 3. Regras clínicas por grupo

## 3.1 Benzodiazepínicos

O motor deve diferenciar:

- ansiedade aguda;
- crise de pânico;
- abstinência alcoólica;
- catatonia;
- agitação;
- insônia de curto prazo;
- convulsão;
- pré-procedimento/urgência.

Regras obrigatórias:

- nunca tratá-los como terapia crônica preferencial sem sinalização;
- marcar risco de dependência, tolerância, abstinência e prejuízo cognitivo;
- bloquear ou alertar fortemente associação com opioides, álcool e outros depressores;
- diferenciar meia-vida curta, intermediária e longa;
- incluir equivalência benzodiazepínica apenas se houver fonte robusta e deixar claro que é aproximada;
- Lorazepam deve ser reconhecido em catatonia;
- Diazepam/lorazepam devem ser reconhecidos em abstinência alcoólica conforme contexto;
- Midazolam deve ficar restrito a urgência/procedimento, conforme via e ambiente;
- Clobazam deve ser tratado principalmente pelo papel anticonvulsivante quando aplicável.

## 3.2 Hipnóticos Z

- uso de curto prazo;
- risco de dependência, amnésia e comportamentos complexos do sono;
- não tratar efeito sedativo como indicação universal;
- diferenciar insônia inicial e manutenção quando sustentado por fonte.

## 3.3 TDAH

O motor deve distinguir:

- primeira linha;
- segunda linha;
- estimulante versus não estimulante;
- adulto versus pediátrico;
- curta versus longa duração;
- risco cardiovascular;
- psicose/mania ativa;
- uso de substâncias;
- ansiedade e tiques;
- necessidade de monitorização de pressão, frequência, peso e sono.

Metilfenidato IR e de liberação prolongada devem compartilhar entidade central, mas manter diferenças farmacocinéticas e operacionais.

## 3.4 Dependência química

- Naltrexona já existente deve ser integrada aos novos agentes;
- Acamprosato: manutenção de abstinência alcoólica;
- Dissulfiram: uso restrito, supervisionado e com contraindicações claras;
- Naloxona: reversão de overdose, não tratamento de manutenção;
- Buprenorfina e metadona: transtorno por uso de opioides, com regras de ambiente, indução e segurança;
- bloquear naltrexona se houver uso atual de opioide sem período de abstinência apropriado;
- diferenciar manutenção, resgate e prevenção de recaída.

## 3.5 Antipsicóticos modernos

Para cada novo antipsicótico, mapear:

- esquizofrenia;
- mania;
- depressão bipolar;
- manutenção;
- potencialização antidepressiva quando aplicável;
- perfil metabólico;
- prolactina;
- acatisia/EPS;
- QT;
- sedação;
- exigência de alimento quando aplicável;
- formulações de longa ação, quando já contempladas na base.

## 3.6 Demência

- separar doença de Alzheimer, demência com corpos de Lewy, demência vascular e outras;
- diferenciar tratamento cognitivo de controle comportamental;
- incluir riscos de bradicardia, síncope, perda de peso e efeitos gastrointestinais dos inibidores de acetilcolinesterase;
- incluir ajuste renal da memantina;
- não sugerir antipsicóticos como tratamento cognitivo.

## 3.7 Urgência/agitação

Prometazina e droperidol devem ser claramente limitadas por contexto, via, monitorização e risco.

Não permitir que medicamentos de urgência apareçam em ranking ambulatorial comum sem contexto explícito.

---

# 4. Integração com o motor

A V2 deve funcionar no fluxo real:

```text
Clinical Phenotype Filter
        ↓
Disease Use Filter, quando houver diagnóstico
        ↓
Filtro de segurança
        ↓
Filtro de papel terapêutico
        ↓
Ranking
        ↓
Dose — efeito + Uso por doença + Fonte
```

## Regras de elegibilidade

- `NAO_RECOMENDADO` → excluir;
- `RESTRITO` → excluir salvo contexto explícito compatível;
- `RESGATE` → somente em urgência/resgate;
- `CURTO_PRAZO` → sinalização obrigatória;
- `POTENCIALIZACAO` → não aparecer como substituto simples;
- `MANUTENCAO` → não priorizar para fase aguda sem indicação;
- `OFF_LABEL_COM_EVIDENCIA` → permitir com sinalização e menor prioridade;
- `TRATAMENTO_PRINCIPAL` → elegibilidade principal.

O motor deve funcionar também sem diagnóstico fechado, usando o fenótipo clínico, mas sem apresentar a escolha como diagnóstico confirmado.

---

# 5. Interface

Manter os quatro quadros e adaptar para a V2:

1. **Decisão do motor**
2. **Justificativa clínica**
3. **Estratégia/medicamento e papel terapêutico**
4. **Objetivo clínico, dose — efeito, uso por doença e fontes**

Para benzodiazepínicos, hipnóticos, opioides e fármacos de urgência, mostrar alertas de alto impacto em posição visível.

Não exibir mensagens internas como “pendente pesquisar” ou “faixa não cadastrada”. Quando não houver dado validado, usar:

- `Informação ainda não validada para uso decisório`;
- excluir do ranking automático até validação.

---

# 6. Testes obrigatórios

Preservar todos os testes atuais e adicionar testes para:

- contagem total esperada da V2;
- presença das três camadas para todos os novos medicamentos;
- nenhum novo medicamento sem fonte;
- benzodiazepínico não sugerido como manutenção crônica preferencial;
- bloqueio de benzodiazepínico + opioide/álcool;
- lorazepam reconhecido em catatonia;
- diazepam/lorazepam em abstinência alcoólica;
- midazolam restrito a urgência/procedimento;
- estimulantes bloqueados ou rebaixados em mania/psicose ativa;
- naloxona classificada como resgate;
- naltrexona bloqueada diante de uso atual de opioide incompatível;
- donepezila/rivastigmina/galantamina/memantina não confundidas com antipsicóticos;
- antipsicóticos modernos participando corretamente do ranking por doença e fase;
- medicamentos de urgência não aparecendo em contexto ambulatorial inadequado;
- interface exibindo fonte correspondente;
- nenhum dos 46 registros anteriores perdido.

Rodar:

```bash
python -m unittest discover -s tests -t .
```

Todos os testes devem passar.

---

# 7. Entregáveis

1. Base farmacológica V2 implementada.
2. Integração real com os filtros e ranking.
3. Interface atualizada e funcionando.
4. Fontes rastreáveis para todos os novos registros.
5. Testes automatizados.
6. Relatório em:

```text
docs/decision_support_engine/MATRIZ_FARMACOLOGICA_V2_IMPLEMENTATION_REPORT.md
```

O relatório deve informar:

- lista final de medicamentos;
- total de registros de Dose — efeito;
- total de registros de Uso por doença/contexto;
- total de fontes;
- arquivos alterados;
- regras de bloqueio implementadas;
- exemplos de funcionamento no app;
- testes executados e resultado;
- lacunas que permaneceram sem evidência suficiente.

---

# 8. Critério de conclusão

A missão só está concluída quando:

- os novos medicamentos estiverem persistidos na base;
- aparecerem no aplicativo quando clinicamente elegíveis;
- forem excluídos quando incompatíveis;
- exibirem Dose — efeito;
- exibirem Uso por doença/contexto;
- exibirem fonte rastreável;
- participarem dos filtros clínicos;
- os testes passarem;
- houver commit e push do resultado.

Não encerrar a missão apenas com planilha, documentação ou dados sem integração funcional.