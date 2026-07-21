# 031 - Knowledge Representation Model

## 1. Objetivo

Definir oficialmente como o conhecimento clinico do PsychRx sera representado de modo computacional, sem implementar software, escolher tecnologia, criar banco de dados ou escrever algoritmos.

Este documento estabelece a ponte entre a Biblioteca Cientifica, os grafos conceituais e a futura engenharia de software.

## 2. Missao

A missao do Knowledge Representation Model e transformar conhecimento cientifico em unidades estruturadas, rastreaveis, versionaveis e reutilizaveis, mantendo separacao entre conteudo clinico e logica de execucao.

## 3. Representacao Conceitual

O conhecimento deve ser representado como unidades conceituais independentes, cada uma com identidade, fonte, escopo, status, versao, relacoes e limites de aplicabilidade.

Uma unidade de conhecimento nao deve ser confundida com codigo. Ela descreve significado clinico e cientifico, nao comportamento executavel.

## 4. Granularidade

A granularidade deve permitir revisar, atualizar e rastrear conhecimento sem reescrever todo o sistema.

Unidades muito grandes dificultam versionamento. Unidades muito pequenas perdem contexto clinico. A granularidade adequada e aquela que preserva:

- significado clinico;
- fonte rastreavel;
- relacao com outros objetos;
- impacto sobre seguranca, explicabilidade e decisao;
- capacidade de atualizacao isolada.

## 5. Objetos de Conhecimento

Objetos de conhecimento sao representacoes estruturadas de conceitos clinicos e cientificos.

Eles podem representar fontes, evidencias, restricoes, interacoes, objetivos, monitorizacao, regras conceituais, estrategias e explicacoes.

Cada objeto deve declarar o que representa, qual sua fonte, onde se aplica, quais limites possui e quais outros objetos dependem dele.

## 6. Relacionamentos

Conhecimento clinico deve ser representado por relacoes explicitas.

Exemplos de relacoes:

- sustenta;
- contraindica;
- modifica;
- exige monitorizacao;
- entra em conflito com;
- deriva de;
- aplica-se a;
- depende de;
- substitui;
- deprecia.

Relacionamentos devem ser clinicamente interpretaveis e auditaveis.

## 7. Metadados

Todo objeto de conhecimento deve conter metadados minimos:

- identificacao;
- nome oficial;
- tipo;
- fonte;
- ano;
- tipo de evidencia;
- qualidade da evidencia;
- status;
- versao;
- data de revisao;
- aplicabilidade;
- conflitos conhecidos;
- responsavel por validacao.

Metadados incompletos impedem uso oficial.

## 8. Reutilizacao

O modelo deve permitir que o mesmo conhecimento seja reutilizado em varios contextos sem duplicacao.

Uma evidencia pode sustentar uma restricao, uma explicacao, uma estrategia e uma necessidade de monitorizacao, desde que cada uso seja rastreavel e contextualizado.

## 9. Extensibilidade

O modelo deve permitir novos objetos e relacoes sem quebrar a arquitetura.

Extensibilidade exige:

- nomenclatura oficial;
- aderencia a Ontologia;
- governanca cientifica;
- versionamento;
- rastreabilidade;
- validacao antes de uso.

## 10. Separacao entre Conhecimento e Execucao

O conhecimento computacional descreve conteudo estruturado. A logica de execucao futura apenas interpreta esse conhecimento.

Motores clinicos nao devem conter evidencia hardcoded. Evidencias nao devem conter algoritmo executavel.

## 11. Limites

Este modelo nao define classes, tabelas, APIs, linguagem, framework, banco de dados ou mecanismos de inferencia.

Ele define como o conhecimento deve ser pensado para que futura implementacao seja coerente, rastreavel e segura.

## 12. Declaracao Final

O Knowledge Representation Model e a base computacional do conhecimento clinico do PsychRx.

No PsychRx, conhecimento so se torna utilizavel quando pode ser representado, rastreado, versionado, validado e explicado sem se confundir com codigo.
