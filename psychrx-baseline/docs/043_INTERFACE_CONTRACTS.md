# 043 - Interface Contracts

## 1. Objetivo

Definir os contratos conceituais entre modulos do PsychRx, sem implementar APIs, DTOs, schemas, classes ou endpoints.

## 2. Missao

Garantir que modulos se comuniquem por acordos explicitos de entrada, saida, invariantes e erros, reduzindo acoplamento e regressao.

## 3. Contrato Conceitual

Um contrato conceitual define:

- operacao;
- responsabilidade;
- entrada esperada;
- saida esperada;
- invariantes;
- erros possiveis;
- rastreabilidade;
- limites.

## 4. Operacoes

Operacoes futuras devem representar intencoes clinicas e arquiteturais, nao detalhes de tecnologia.

Exemplos conceituais:

- construir Clinical Snapshot;
- validar entrada clinica;
- avaliar seguranca;
- gerar perguntas;
- formar hipoteses;
- definir objetivos;
- gerar estrategias candidatas;
- comparar estrategias;
- produzir explicacao;
- registrar auditoria.

## 5. Entradas

Toda entrada deve declarar:

- origem;
- obrigatoriedade;
- formato conceitual;
- validade;
- contexto clinico;
- nivel de confianca quando aplicavel;
- sensibilidade de seguranca;
- fonte quando for conhecimento.

## 6. Saidas

Toda saida deve declarar:

- conteudo;
- status;
- justificativa;
- incertezas;
- evidencias;
- alertas;
- bloqueios;
- trilha de rastreabilidade.

## 7. Invariantes

Invariantes obrigatorias:

- nenhuma estrategia sem objetivo;
- nenhuma comparacao sem seguranca;
- nenhuma explicacao sem rastreabilidade;
- nenhuma regra clinica sem fonte;
- nenhuma interface decidindo logica clinica;
- nenhum motor acessando dashboard diretamente.

## 8. Erros Possiveis

Categorias:

- entrada invalida;
- dado obrigatorio ausente;
- risco nao avaliado;
- evidencia ausente;
- conflito de evidencia;
- violacao de nomenclatura;
- violacao de dependencia;
- falha de rastreabilidade;
- saida nao explicavel.

## 9. Limites

Este documento nao define protocolo HTTP, GraphQL, REST, arquivos, objetos de linguagem ou banco de dados.

## 10. Declaracao Final

Interface Contracts impedem que modulos conversem por improviso.

No PsychRx, contratos conceituais sao a primeira defesa contra regressao arquitetural.
