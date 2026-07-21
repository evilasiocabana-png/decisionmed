# 033 - Clinical Relationship Model

## 1. Objetivo

Definir como os objetos de conhecimento clinico do PsychRx se relacionam entre si, sem implementar banco de dados, grafo tecnico, API ou algoritmo.

## 2. Missao

A missao do Clinical Relationship Model e tornar explicitas as dependencias, composicoes, agregacoes, cardinalidades e relacoes semanticas que sustentam o conhecimento computacional do PsychRx.

## 3. Dependencias

Dependencia significa que um objeto precisa de outro para ter significado, validade ou aplicabilidade.

Exemplos:

- TherapeuticStrategy depende de TherapeuticObjective.
- ClinicalRule depende de Evidence ou Guideline.
- Contraindication depende de fonte e contexto de aplicabilidade.
- MonitoringRecommendation depende de risco, agente ou condicao.

Dependencias devem ser explicitas para evitar conhecimento solto.

## 4. Cardinalidade

Cardinalidade define quantos objetos podem se relacionar.

Exemplos conceituais:

- uma Evidence pode sustentar varias ClinicalRules;
- uma Guideline pode conter varias Recommendations de fonte;
- uma Contraindication pode afetar varias TherapeuticStrategies;
- uma TherapeuticStrategy pode depender de multiplas evidencias;
- um ClinicalSnapshot pode ativar multiplas restricoes.

Cardinalidade nao deve ser definida como estrutura de banco, mas como relacao de significado.

## 5. Composicao

Composicao ocorre quando um objeto e parte essencial de outro.

Exemplo: uma recomendacao de fonte pode ser composta por populacao, intervencao, comparador, desfecho, qualidade da evidencia e forca da recomendacao.

Se a parte essencial for removida, o objeto perde validade clinica.

## 6. Agregacao

Agregacao ocorre quando objetos independentes sao reunidos para formar uma leitura clinica maior.

Exemplo: Evidence, Contraindication e DrugInteraction podem ser agregados para explicar o risco de uma TherapeuticStrategy.

Agregacao nao elimina autonomia dos objetos.

## 7. Heranca Semantica

Heranca semantica significa que um conceito mais especifico herda significado de um conceito mais geral.

Exemplos:

- DrugInteraction e um tipo de TherapeuticRestriction.
- Contraindication e um tipo de Constraint.
- MonitoringRecommendation e um tipo de conhecimento de acompanhamento.

Heranca semantica nao e heranca de classe. E relacao conceitual.

## 8. Relacionamentos Semanticos

Relacionamentos oficiais podem incluir:

- sustenta;
- contradiz;
- limita;
- bloqueia;
- exige;
- modifica;
- monitora;
- explica;
- deriva de;
- substitui;
- deprecia;
- entra em conflito com.

Cada relacao deve ter significado clinico claro.

## 9. Relacao com Grafos

O Clinical Relationship Model oferece base para Knowledge Graph, Constraint Graph, Evidence Graph e Decision Graph.

Ele define a semantica das relacoes, nao a tecnologia que as armazenara.

## 10. Limites

Este documento nao define Neo4j, SQL, modelo de classes, schema tecnico ou algoritmo de travessia.

## 11. Declaracao Final

O Clinical Relationship Model garante que conhecimento no PsychRx nao exista isolado.

No PsychRx, significado clinico surge das relacoes rastreaveis entre objetos, evidencias, restricoes, objetivos, estrategias e explicacoes.
