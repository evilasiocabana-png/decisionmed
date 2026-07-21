# Motor Profile Enrichment Analysis

## Objetivo

Definir como respostas explicativas ricas, como o exemplo da Quetiapina por faixa de dose, podem ser incorporadas ao Motor Farmacologico do PsychRx sem alterar as tabelas originais e sem transformar informacao nao validada em conhecimento oficial.

## Diagnostico Atual

A Tabela Motor atual responde bem a pergunta:

> Qual opcao farmacologica combina melhor com o perfil clinico desejado?

Ela ja possui, para cada item:

- medicamento;
- classe;
- alvos terapeuticos;
- pontuacoes por eixo clinico;
- cautelas;
- contextos preferenciais;
- fonte/tabela original;
- status.

Exemplo ja existente para Quetiapina:

- Classe: Antipsicotico atipico.
- Alvos: sono, psicose, bipolaridade, ansiedade.
- Sono: 5.
- Ansiedade: 3.
- Estabilizacao do humor: 4.
- Psicose: 4.
- Cautelas: sedacao, metabolico, hipotensao.
- Fonte local: Tabela 5.

## Lacuna Identificada

O motor ainda nao representa bem a pergunta:

> Por que esse medicamento muda de utilidade conforme a dose?

O exemplo da Quetiapina contem informacao de outro tipo:

- faixa de dose;
- efeito predominante por faixa;
- mecanismo/alvo farmacologico por faixa;
- impacto em sono, ansiedade, humor, energia, cognicao e sedacao;
- cautelas proporcionais;
- texto explicativo para o medico.

Essa informacao nao deve sobrescrever a matriz atual. Ela deve entrar como uma camada adicional.

## Camada Proposta

Criar uma camada futura chamada:

```text
Medication Explanation Profile
```

Responsabilidade:

- explicar o perfil farmacologico do candidato;
- detalhar efeitos por faixa quando houver dado validado;
- indicar o que ja e conhecido;
- marcar lacunas como `PENDENTE_PESQUISAR`;
- nunca alterar as 8 tabelas originais.

## Aplicacao Para Todos os Medicamentos

A logica nao deve ser exclusiva da Quetiapina.

Todos os medicamentos presentes em `pharmacological_decision_matrix.csv` devem ter pelo menos uma linha no backlog de enriquecimento. Essa linha deve separar:

- o que a Tabela Motor ja possui;
- o que ainda precisa de pesquisa especifica;
- o que ainda nao pode ser usado na resposta final do app.

Quetiapina permanece com tres linhas porque o exemplo informado pelo usuario trouxe uma hipotese por faixa de dose. As demais medicacoes ficam com uma linha geral marcada como `PENDENTE_PESQUISAR` para faixa de dose, efeito dominante e mecanismo ate que exista fonte revisavel.

## Estrutura Recomendada

Campos minimos:

- medication_id
- medication_name
- drug_class
- dose_band
- dominant_effect
- pharmacological_target
- receptor_or_mechanism
- anxiety_score
- sleep_score
- mood_score
- energy_score
- cognition_score
- sedation_risk
- weight_gain_risk
- extrapyramidal_risk
- explanation_for_motor
- current_source_status
- source_required
- source_reference
- integration_status

## Fonte por Campo

A partir desta fase, cada campo informativo deve possuir uma coluna de fonte correspondente.

Exemplos:

```text
pharmacological_target
pharmacological_target_source

sedation_risk
sedation_risk_source

receptor_or_mechanism
receptor_or_mechanism_source
```

Regra:

- se o valor veio da Tabela Motor ou das tabelas locais, a fonte usa `TM(...)`;
- se o valor veio de DailyMed/FDA, a fonte usa `DM`;
- se o valor ainda nao possui fonte revisavel, valor e/ou fonte permanecem `PENDENTE_PESQUISAR`;
- o app pode mostrar a resposta limpa, mas deve conseguir exibir a legenda da fonte abaixo do bloco de estrategia.

As abreviacoes oficiais ficam em:

```text
knowledge_base/decision_support_engine/tables/medication_source_legend.csv
```

## Regra de Governanca

Qualquer informacao que nao esteja explicitamente nas tabelas ou em fonte validada deve ser registrada como:

```text
PENDENTE_PESQUISAR
```

As fontes oficiais e o uso permitido por campo estao definidos em:

```text
docs/decision_support_engine/MOTOR_RESEARCH_SOURCE_POLICY.md
```

Exemplo:

```text
Quetiapina 25-100 mg/dia -> PENDENTE_PESQUISAR
Quetiapina 150-300 mg/dia -> PENDENTE_PESQUISAR
Quetiapina 300-800 mg/dia -> PENDENTE_PESQUISAR
Norquetiapina -> PENDENTE_PESQUISAR
```

## Como Isso Entra no Motor

Fluxo proposto:

```text
Tabela Motor
  -> ranking e candidato principal

Medication Explanation Profile
  -> explicacao farmacologica do candidato

Resposta do app
  -> decisao pratica
  -> estrategia
  -> faixa alvo
  -> justificativa
  -> perfil explicativo
```

## Exemplo de Uso Futuro

Quando o motor sugerir Quetiapina:

1. A Tabela Motor continua dizendo por que Quetiapina apareceu no ranking.
2. A nova camada explica o perfil por dose, se validado.
3. Se o perfil ainda nao estiver validado, o app mostra:

```text
Perfil por dose: pendente de pesquisa especifica.
```

Quando o motor sugerir outro medicamento:

1. A Tabela Motor informa classe, alvos, pontuacoes e cautelas ja cadastradas.
2. A nova camada mostra as lacunas de explicacao farmacologica.
3. O que nao estiver validado permanece como `PENDENTE_PESQUISAR`.

## Pontos Que Nao Devem Ser Alterados

- Nao alterar `pharmacological_decision_matrix.csv`.
- Nao alterar as 8 planilhas originais.
- Nao substituir dados ja revisados.
- Nao inferir mecanismo sem fonte.
- Nao transformar exemplo nao validado em regra do motor.

## Estado Atual do Backlog

A tabela criada em:

```text
knowledge_base/decision_support_engine/tables/medication_explanation_profile_backlog.csv
```

contem todos os medicamentos da Tabela Motor.

Ela e apenas backlog de enriquecimento, nao fonte ativa do app.

## Proxima Missao Recomendada

Pesquisar medicamento por medicamento, priorizando candidatos que aparecem com maior frequencia no ranking do app, e substituir `PENDENTE_PESQUISAR` apenas quando houver fonte, secao e trecho revisavel.
