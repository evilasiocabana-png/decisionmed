# AUDITORIA — PERFIL POR DOSE E USO POR DOENÇA

## Natureza da missão

Auditoria somente leitura e diagnóstico. **Não implementar, não corrigir e não alterar o comportamento clínico nesta missão.**

## Objetivo

Verificar como o PsychRx está atualmente estruturando, armazenando, processando e exibindo as informações referentes a:

1. faixas terapêuticas;
2. perfil clínico/farmacológico por dose;
3. mecanismo de ação por faixa de dose;
4. uso por doença/indicação;
5. fontes científicas e regulatórias;
6. distinção entre uso aprovado, recomendado por diretriz, potencialização, manutenção, off-label, evidência limitada e não recomendado;
7. rastreabilidade entre dado de origem, regra do motor e texto exibido ao médico.

## Contexto funcional esperado

O motor possui uma planilha com 46 registros de medicamentos, incluindo antidepressivos, antipsicóticos, estabilizadores do humor, anticonvulsivantes e naltrexona.

A tela deverá futuramente ser capaz de responder de forma clara:

- qual é a faixa de dose relevante;
- o que muda clinicamente ou farmacologicamente nessa faixa;
- para qual doença ou fase da doença o medicamento é utilizado;
- qual é o papel terapêutico: principal, adjuvante, potencializador, manutenção ou uso restrito;
- qual fonte sustenta cada afirmação;
- qual é o nível de evidência;
- se a faixa representa uma divisão regulatória, clínica didática, farmacodinâmica comprovada ou apenas maior exposição.

## Medicamentos que devem ser localizados na base atual

1. Agomelatina
2. Amitriptilina
3. Aripiprazol
4. Bupropiona
5. Bupropiona XL
6. Carbamazepina
7. Citalopram
8. Clomipramina
9. Clorpromazina
10. Clozapina
11. Desipramina
12. Desvenlafaxina
13. Divalproato
14. Dosulepina
15. Doxepina
16. Duloxetina
17. Escitalopram
18. Fenitoína
19. Fenobarbital
20. Fluoxetina
21. Fluvoxamina
22. Haloperidol
23. Imipramina
24. Lamotrigina
25. Levomepromazina
26. Lítio
27. Lurasidona
28. Maprotilina
29. Mianserina
30. Mirtazapina
31. Naltrexona
32. Nortriptilina
33. Olanzapina
34. Oxcarbazepina
35. Paroxetina
36. Quetiapina
37. Risperidona
38. Sertralina
39. Tioridazina
40. Topiramato
41. Trazodona
42. Valproato
43. Venlafaxina
44. Venlafaxina XR
45. Vilazodona
46. Vortioxetina

## Perguntas obrigatórias da auditoria

### 1. Fonte de dados

- Em quais arquivos, planilhas, tabelas, bancos ou módulos estão cadastrados os 46 medicamentos?
- Qual é a fonte real usada hoje para faixa terapêutica?
- O texto “TM/Aba 1” representa qual arquivo e qual aba?
- Existem medicamentos duplicados por formulação ou sal, como bupropiona/Bupropiona XL, venlafaxina/Venlafaxina XR e valproato/divalproato?
- Há normalização de nomes, acentos, capitalização, formulação e princípio ativo?

### 2. Modelo de dados atual

Mapear os campos existentes e informar se há suporte real para:

- dose mínima;
- dose máxima;
- unidade;
- formulação;
- via;
- doença/indicação;
- fase da doença;
- papel terapêutico;
- mecanismo;
- efeito clínico dominante;
- perfil por dose;
- nível de evidência;
- fonte;
- status regulatório;
- alerta;
- contraindicação;
- necessidade de nível sérico;
- fronteira rígida ou didática;
- data/versão da referência.

Informar quais campos existem, quais estão ausentes e quais estão sendo simulados por texto livre.

### 3. Uso por doença

Verificar se hoje o sistema distingue corretamente:

- transtorno depressivo maior;
- depressão resistente;
- transtorno bipolar — depressão;
- transtorno bipolar — mania;
- manutenção bipolar;
- esquizofrenia e outros transtornos psicóticos;
- TOC;
- TAG;
- transtorno do pânico;
- ansiedade social;
- TEPT;
- insônia;
- dor neuropática;
- fibromialgia;
- prevenção de enxaqueca;
- epilepsia;
- transtorno por uso de álcool;
- transtorno por uso de opioides;
- tabagismo;
- bulimia nervosa;
- transtorno disfórico pré-menstrual.

Para cada doença presente no sistema, informar se o medicamento é classificado como:

- tratamento principal;
- alternativa;
- potencialização;
- adjuvante;
- manutenção;
- uso aprovado;
- recomendado por diretriz;
- off-label com evidência;
- evidência limitada;
- não recomendado;
- uso restrito/alto risco.

### 4. Perfil por dose

Verificar se o sistema atualmente trata “perfil por dose” como:

- mudança real de mecanismo/receptor;
- mudança de indicação;
- mudança de efeito clínico;
- aumento de exposição;
- faixa de titulação;
- faixa guiada por nível sérico;
- texto descritivo sem estrutura.

Identificar qualquer inferência indevida, principalmente nos casos de:

- quetiapina;
- mirtazapina;
- trazodona;
- venlafaxina;
- doxepina;
- clorpromazina;
- levomepromazina;
- amitriptilina;
- lítio;
- valproato/divalproato;
- carbamazepina;
- lamotrigina;
- fenitoína;
- fenobarbital.

### 5. Fontes e rastreabilidade

- Existe fonte individual ligada a cada faixa de dose?
- A fonte aparece apenas como texto genérico ou possui estrutura própria?
- O sistema diferencia bula regulatória, diretriz, livro-texto, revisão e estudo primário?
- É possível rastrear a recomendação exibida até a linha/célula/registro original?
- Existem referências incompletas, como “TM/Aba 1”, sem obra, edição, ano, página, DOI ou URL institucional?
- Há controle de versão da evidência?
- O motor consegue impedir que uma informação sem validação seja apresentada como fato estabelecido?

### 6. Motor de decisão

Auditar o fluxo completo:

```text
entrada clínica
→ identificação do diagnóstico/quadro
→ seleção de candidatos
→ aplicação de contraindicações e riscos
→ escolha do papel terapêutico
→ definição da faixa de dose
→ explicação do perfil por dose
→ inclusão da fonte
→ apresentação na interface
```

Informar:

- em qual etapa cada decisão é tomada;
- se a doença realmente influencia a faixa apresentada;
- se o motor confunde “faixa por quadro” com “dose inicial” ou “dose máxima”;
- se sugere antipsicótico como substituto direto de antidepressivo sem classificar potencialização ou indicação específica;
- se considera resposta, adesão, tempo de uso, tolerabilidade e dose adequada antes de sugerir troca;
- se existe risco de recomendação clinicamente incoerente por falta de contexto.

### 7. Interface dos quatro quadros

Auditar a implementação atual dos quatro quadros e informar exatamente o que cada um recebe do backend.

Verificar especialmente:

- texto concatenado ou sem espaçamento;
- campos vazios;
- “não cadastrado” apesar de haver faixa registrada;
- contradição entre otimizar e substituir;
- medicamento sugerido sem justificativa;
- fonte interna exibida ao médico sem referência bibliográfica;
- excesso de texto técnico/log interno;
- se “faixa terapêutica”, “perfil por dose”, “uso por doença” e “fonte” estão claramente separados.

### 8. Cobertura dos 46 medicamentos

Gerar uma matriz com uma linha para cada medicamento e as colunas:

| Medicamento | Existe na base | Faixa cadastrada | Uso por doença | Perfil por dose | Fonte estruturada | Status regulatório | Alertas | Problemas encontrados |
|---|---:|---:|---:|---:|---:|---:|---:|---|

Não omitir nenhum dos 46 medicamentos.

### 9. Testes

Localizar e avaliar testes existentes para:

- leitura da planilha;
- normalização de medicamento;
- seleção por doença;
- faixa por indicação;
- perfil por dose;
- exibição da fonte;
- classificação off-label/aprovado;
- nível de evidência;
- duplicidade entre formulações;
- medicamentos guiados por nível sérico;
- renderização dos quatro quadros.

Informar testes ausentes, sem criá-los nesta missão.

## Entregável obrigatório

Criar um relatório de auditoria contendo:

1. resumo executivo;
2. arquitetura atual do fluxo;
3. arquivos e funções envolvidos;
4. modelo de dados atual;
5. matriz completa dos 46 medicamentos;
6. problemas encontrados, classificados em crítico, alto, médio e baixo;
7. divergências clínicas ou farmacológicas;
8. lacunas de fontes e rastreabilidade;
9. cobertura de testes;
10. recomendações de correção em ordem de prioridade;
11. proposta de próxima missão, sem executá-la.

## Regras

- Não alterar código, planilha, banco, interface ou documentação oficial, exceto o próprio relatório de auditoria.
- Não inventar fontes nem completar dados clínicos por memória.
- Não afirmar que uma faixa muda o mecanismo sem localizar suporte explícito.
- Diferenciar claramente dado encontrado, inferência e ausência de evidência.
- Citar caminhos de arquivos, classes, funções, tabelas, colunas e linhas relevantes.
- Registrar o commit e o estado do repositório auditado.

## Local sugerido para o relatório

```text
codex/completed/AUDITORIA_PERFIL_POR_DOSE_E_USO_POR_DOENCA_2026-07-12_RESULTADO.md
```

Caso o fluxo do repositório determine outro local, seguir o protocolo existente e informar onde o relatório foi salvo.
