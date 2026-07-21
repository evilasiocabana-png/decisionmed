# 030 - Clinical Reasoning Architecture

## 1. Definicao

Este documento consolida a arquitetura do raciocinio clinico do PsychRx.

Ele integra motores conceituais, grafos, Biblioteca Cientifica, seguranca, explicabilidade, monitorizacao e raciocinio longitudinal em um fluxo unico, sem definir implementacao tecnica.

## 2. Objetivo

O objetivo e especificar como o PsychRx organiza o raciocinio clinico de ponta a ponta antes da modelagem do dominio e antes de qualquer software.

## 3. Missao

A missao da Clinical Reasoning Architecture e consolidar os motores conceituais em um fluxo clinico unico, coerente, rastreavel, explicavel e seguro.

Ela deve servir como gate arquitetural antes da modelagem do dominio.

## 4. Entradas Conceituais

As entradas conceituais desta arquitetura incluem:

- Clinical Snapshot;
- contexto clinico;
- perguntas e lacunas;
- hipoteses diagnosticas;
- objetivos terapeuticos;
- restricoes;
- evidencias;
- alertas de seguranca;
- estrategias candidatas;
- dados de monitorizacao;
- dados longitudinais.

## 5. Saidas Conceituais

As saidas conceituais incluem:

- fluxo de raciocinio clinico consolidado;
- responsabilidades dos motores;
- dependencias entre componentes;
- pontos de interrupcao por seguranca;
- requisitos de explicabilidade;
- requisitos de rastreabilidade;
- criterios de revisao arquitetural formal;
- gate para modelagem do dominio.

## 6. Principio Central

O paciente permanece no centro.

O raciocinio vem antes da estrategia. A seguranca vem antes da comparacao. A evidencia vem antes da justificativa. A explicabilidade vem antes da apresentacao. O medico permanece decisor final.

## 7. Integracao dos Motores

Os motores se integram da seguinte forma:

- Clinical Snapshot ancora o estado atual.
- Clinical Context Engine individualiza o raciocinio.
- Question Engine reduz lacunas.
- Diagnostic Reasoning Engine organiza hipoteses.
- Uncertainty Engine explicita limites.
- Therapeutic Objective Engine define alvos.
- Safety First Engine bloqueia ou modifica estrategias.
- Strategy Generation Engine organiza possibilidades.
- Strategy Comparison Engine compara alternativas.
- Explanation Engine justifica o percurso.
- Monitoring Engine acompanha resposta e seguranca.
- Longitudinal Reasoning interpreta a trajetoria.
- Clinical Navigation Engine orienta continuidade.

## 8. Fluxo Completo de Decisao Clinica

```text
Paciente
  -> Clinical Snapshot
  -> Clinical Context Engine
  -> Question Engine
  -> Diagnostic Reasoning Engine
  -> Uncertainty Engine
  -> Therapeutic Objective Engine
  -> Constraint Graph / Safety First Engine
  -> Strategy Generation Engine
  -> Strategy Comparison Engine
  -> Evidence Graph / Biblioteca Cientifica
  -> Explanation Engine
  -> Monitoring Engine
  -> Longitudinal Reasoning
  -> Clinical Navigation Engine
  -> Estabilizacao Clinica
```

O fluxo e iterativo. Novos dados podem retornar o raciocinio a etapas anteriores.

## 9. Interfaces Conceituais

Interfaces conceituais sao pontos de comunicacao entre motores.

Elas nao representam APIs, classes ou banco de dados. Representam contratos de informacao: o que um motor precisa receber e o que deve entregar ao restante do raciocinio.

## 10. Dependencias

Dependencias principais:

- TherapeuticStrategy depende de TherapeuticObjective.
- Comparacao depende de seguranca, restricoes e evidencias.
- Explicacao depende da trilha completa.
- Monitorizacao depende de riscos e objetivos.
- Estabilidade depende de dados longitudinais.
- Qualquer conhecimento clinico depende de fonte rastreavel.

## 11. Responsabilidades de Cada Componente

Cada componente deve ter responsabilidade unica:

- Snapshot representa estado atual.
- Contexto individualiza.
- Perguntas reduzem lacunas.
- Diagnostico organiza hipoteses.
- Incerteza limita conclusoes.
- Objetivos dao direcao.
- Seguranca protege.
- Geracao cria possibilidades.
- Comparacao organiza alternativas.
- Evidencia sustenta.
- Explicacao torna audivel.
- Monitorizacao acompanha.
- Longitudinalidade interpreta trajetoria.
- Navegacao preserva continuidade.

## 12. Separacao entre Conhecimento, Raciocinio e Implementacao

Conhecimento cientifico fica na Biblioteca Cientifica, Evidence Graph e politicas de rastreabilidade.

Raciocinio clinico fica nos motores conceituais.

Implementacao tecnica futura deve respeitar essa separacao e nao hardcodar conhecimento cientifico nos algoritmos.

## 13. Diagrama Textual do Raciocinio

```text
Dados do paciente
  + contexto
  + evidencias
  + restricoes
  + seguranca
  + objetivos
  + incertezas
  = raciocinio clinico explicavel

raciocinio clinico explicavel
  -> alternativas terapeuticas comparaveis
  -> monitorizacao proporcional
  -> acompanhamento longitudinal
  -> estabilizacao clinica como finalidade
```

## 14. Revisao Arquitetural Formal

Antes da modelagem do dominio, deve haver revisao arquitetural formal do Sprint 4.

Essa revisao deve verificar:

- lacunas entre motores;
- responsabilidades duplicadas;
- dependencia circular;
- ausencia de rastreabilidade;
- ausencia de explicabilidade;
- mistura entre conhecimento e algoritmo;
- salto indevido para implementacao;
- falhas no fluxo de seguranca.

## 15. Gate de Qualidade

O Sprint 4 funciona como gate antes da modelagem do dominio.

Nao se deve avancar para entidades, agregados ou especificacoes de implementacao se o fluxo de raciocinio ainda tiver lacunas, duplicidades ou contradicoes.

## 16. Riscos Arquiteturais

Riscos principais:

- motores com responsabilidades sobrepostas;
- Strategy Generation atuando como prescritor;
- Safety First Engine consultado tarde demais;
- Evidence Graph usado como decoracao;
- Explanation Engine tratado como texto final e nao como requisito;
- Clinical Snapshot desatualizado;
- monitorizacao desconectada da estabilidade;
- interface decidindo logica clinica.

## 17. Limites da Arquitetura

Esta arquitetura nao implementa software, nao define tecnologia, nao escolhe linguagem, nao cria banco de dados, nao prescreve e nao substitui decisao medica.

Ela define o modo como o PsychRx deve organizar o raciocinio clinico.

## 18. Declaracao Final

A Clinical Reasoning Architecture consolida o nucleo cognitivo do PsychRx.

No PsychRx, decisao clinica segura nasce da integracao entre paciente, contexto, perguntas, hipoteses, objetivos, restricoes, evidencia, explicacao, monitorizacao e longitudinalidade.

Esta arquitetura e o gate conceitual antes da modelagem do dominio.
