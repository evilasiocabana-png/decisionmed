# 012 - Decision Graph

## 1. Objetivo

Este documento define oficialmente o grafo de decisão clínica do PsychRx.

O Decision Graph representa a arquitetura conceitual dos caminhos de raciocínio clínico que conectam o estado atual do paciente a hipóteses, objetivos, restrições, estratégias, riscos, evidências, monitorização e estabilização.

Este documento não implementa algoritmos, não define software, não cria APIs, não descreve banco de dados e não automatiza decisões clínicas.

## 2. Conceito Geral

O Decision Graph organiza decisões clínicas como uma rede de nós, caminhos, bifurcações, critérios, restrições e impactos.

Ele não é um fluxograma de software. É uma representação conceitual de como o raciocínio clínico deve ser estruturado antes que qualquer `TherapeuticStrategy` seja comparada ou apresentada.

O Decision Graph deve impedir saltos diretos entre sintoma e estratégia. Toda decisão deve atravessar contexto clínico, segurança, objetivos, restrições, evidências e explicabilidade.

## 3. Nós Clínicos

Nós clínicos são pontos de organização do raciocínio.

### Nó de Clinical Snapshot

Representa o estado clínico atual do paciente.

Inclui sintomas, síndromes, hipóteses, objetivos, restrições, riscos, dados ausentes e incertezas.

### Nó de Sintoma

Representa manifestação clínica relevante.

Pode conduzir a síndromes, hipóteses, objetivos, monitorização ou alerta de segurança.

### Nó de Síndrome

Representa agrupamento clínico de sintomas.

Pode sustentar hipóteses, indicar riscos ou orientar objetivos terapêuticos.

### Nó de Hipótese Diagnóstica

Representa hipótese em avaliação.

Deve possuir nível de confiança, critérios favoráveis, critérios contrários e incertezas.

### Nó de Objetivo Terapêutico

Representa o alvo clínico que orienta a decisão.

Nenhuma estratégia deve existir sem este nó.

### Nó de Restrição

Representa limite clínico, farmacológico, contextual ou individual.

Pode modificar, reduzir ou bloquear caminhos.

### Nó de Segurança

Representa avaliação de risco obrigatória.

Deve preceder qualquer caminho estratégico.

### Nó de Evidência

Representa sustentação científica, qualidade, aplicabilidade, conflito e força da recomendação.

### Nó de Estratégia

Representa caminho terapêutico conceitual comparável.

Não representa prescrição.

### Nó de Monitorização

Representa acompanhamento necessário para avaliar resposta, risco, tolerabilidade e estabilidade.

### Nó de Estabilização

Representa o destino final do raciocínio: maior estabilidade clínica do paciente.

## 4. Caminhos

Caminhos são sequências clínicas possíveis entre nós.

Um caminho típico pode seguir:

```text
Clinical Snapshot
  -> Sintomas
  -> Síndromes
  -> Hipóteses
  -> Objetivos
  -> Restrições
  -> Segurança
  -> Evidências
  -> Estratégias
  -> Monitorização
  -> Estabilização
```

Esse caminho não é algoritmo. Ele é uma ordem conceitual de segurança e coerência clínica.

Caminhos podem retornar a nós anteriores quando surgem dados novos, incertezas, riscos ou deterioração clínica.

## 5. Bifurcações

Bifurcações são pontos em que o raciocínio clínico pode seguir por mais de um caminho.

Exemplos:

- dados suficientes versus dados insuficientes;
- risco baixo versus risco crítico;
- hipótese provável versus hipótese incerta;
- objetivo de eficácia versus objetivo de segurança;
- melhora sintomática versus piora funcional;
- estratégia possível versus estratégia bloqueada;
- evidência convergente versus evidência conflitante;
- estabilidade parcial versus deterioração.

Toda bifurcação deve explicitar:

- pergunta clínica;
- caminhos possíveis;
- critérios que diferenciam os caminhos;
- riscos de cada caminho;
- incertezas;
- necessidade de decisão médica.

## 6. Critérios

Critérios são elementos usados para orientar passagem entre nós ou bifurcações.

Critérios principais:

- gravidade sintomática;
- risco suicida ou comportamental;
- presença de delirium, intoxicação ou abstinência;
- comorbidades;
- contraindicações;
- interações;
- efeitos adversos prévios;
- funcionalidade;
- qualidade de vida;
- adesão;
- preferência do paciente;
- qualidade da evidência;
- aplicabilidade da evidência;
- disponibilidade de monitorização;
- reversibilidade da decisão;
- impacto sobre estabilização.

Critérios devem ser explícitos. Critérios ocultos reduzem explicabilidade.

## 7. Restrições

Restrições limitam caminhos.

Podem ser:

- absolutas;
- relativas;
- contextuais;
- temporárias;
- dependentes de evidência;
- dependentes de monitorização;
- dependentes de preferência do paciente.

Restrições podem produzir:

- bloqueio de caminho;
- alerta crítico;
- alerta moderado;
- necessidade de encaminhamento;
- necessidade de monitorização;
- redução da força da comparação;
- retorno para coleta de dados;
- revisão de objetivo.

Nenhuma restrição relevante deve ser ignorada para preservar um caminho estratégico desejado.

## 8. Pontos Críticos

Pontos críticos são nós ou bifurcações em que erro de raciocínio pode gerar risco clínico relevante.

Pontos críticos incluem:

- risco suicida;
- risco de agressividade;
- delirium;
- intoxicação;
- abstinência;
- gestação;
- lactação;
- insuficiência renal;
- insuficiência hepática;
- doença cardiovascular;
- QT prolongado;
- epilepsia;
- interação medicamentosa grave;
- alergia;
- reação adversa grave prévia;
- evidência conflitante;
- estratégia sem monitorização possível;
- deterioração clínica.

Pontos críticos devem ter prioridade sobre conveniência, preferência de interface ou desejo de gerar estratégia.

## 9. Reversibilidade

Reversibilidade representa a capacidade de revisar, desfazer ou corrigir um caminho clínico com menor custo ou risco.

Caminhos mais reversíveis incluem:

- coletar dados adicionais;
- revisar hipótese;
- redefinir objetivo;
- intensificar monitorização;
- reconhecer incerteza;
- adiar comparação estratégica;
- registrar alerta para revisão médica.

Decisões reversíveis ainda exigem justificativa. Reversibilidade não elimina responsabilidade clínica.

## 10. Irreversibilidade

Irreversibilidade representa caminhos que podem gerar consequências difíceis de reverter, risco elevado ou perda de segurança.

Caminhos pouco reversíveis ou de alto impacto incluem:

- ignorar risco suicida ou agressivo;
- avançar com estratégia diante de contraindicação grave;
- desconsiderar interação de alto risco;
- interpretar delirium como transtorno psiquiátrico primário sem avaliação;
- propor caminho sem monitorização possível;
- tratar evidência fraca como recomendação forte;
- ignorar reação adversa grave prévia;
- reduzir explicabilidade;
- remover rastreabilidade.

Quanto menor a reversibilidade, maior deve ser a exigência de segurança, evidência, explicação e decisão médica documentada.

## 11. Propagação de Impacto

Propagação de impacto descreve como uma mudança em um nó altera outros nós do grafo.

Exemplos:

- novo sintoma pode alterar síndrome, hipótese e objetivo;
- nova hipótese pode alterar objetivos e restrições;
- nova restrição pode bloquear estratégia;
- novo SafetyAlert pode exigir monitorização ou encaminhamento;
- nova evidência pode alterar força da comparação;
- efeito adverso pode alterar resposta, tolerabilidade e estabilidade;
- recaída pode alterar objetivo, estratégia e monitorização;
- deterioração clínica pode interromper caminho estratégico e priorizar segurança.

O Decision Graph deve tornar esses impactos visíveis para evitar decisões isoladas.

## 12. Relação com Outros Grafos

O Decision Graph depende conceitualmente de:

- `Knowledge Graph`, para entender relações clínicas;
- `Constraint Graph`, para limites e restrições;
- `Evidence Graph`, para sustentação científica;
- `Clinical Snapshot`, para estado atual;
- `Clinical Safety Contract`, para pontos críticos;
- `Motor de Estabilização`, para avaliar destino final.

O Decision Graph não substitui esses documentos. Ele organiza como suas informações entram em caminhos de decisão.

## 13. Limites

O Decision Graph:

- não prescreve;
- não decide pelo médico;
- não implementa algoritmo;
- não escolhe psicofármaco;
- não substitui avaliação clínica;
- não elimina incerteza;
- não transforma caminho possível em conduta obrigatória;
- não deve ocultar bifurcações, restrições ou impactos.

Sua função é organizar o raciocínio clínico de forma explicável e segura.

## 14. Declaração Final

O Decision Graph do PsychRx é a arquitetura conceitual dos caminhos de decisão clínica.

Ele organiza nós, caminhos, bifurcações, critérios, restrições, pontos críticos, reversibilidade, irreversibilidade e propagação de impacto para garantir que nenhuma estratégia seja considerada fora do contexto do paciente, da segurança, da evidência e da estabilização.

No PsychRx, decidir não é saltar para uma conduta. Decidir é atravessar um caminho clínico rastreável, explicável e sempre subordinado ao julgamento médico.
