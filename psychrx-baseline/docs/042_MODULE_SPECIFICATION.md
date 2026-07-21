# 042 - Module Specification

## 1. Objetivo

Definir os modulos oficiais do software futuro do PsychRx em nivel de engenharia conceitual, sem escrever codigo ou escolher tecnologia.

Este documento nao implementa software, nao cria codigo, nao define classes, nao cria pacotes e nao escolhe framework.

## 2. Missao

Transformar a arquitetura em modulos com responsabilidades, limites, dependencias, comunicacao e isolamento claramente definidos.

## 3. Modulos Oficiais

Modulos principais:

- domain;
- knowledge;
- evidence;
- reasoning;
- safety;
- application;
- interfaces;
- audit;
- tests;
- documentation.

## 4. Responsabilidades

`domain` representa conceitos centrais e invariantes.

`knowledge` representa objetos de conhecimento computacional.

`evidence` governa fontes, qualidade, conflitos e rastreabilidade cientifica.

`reasoning` coordena motores clinicos conceituais.

`safety` concentra avaliacao de riscos, bloqueios e alertas.

`application` orquestra casos de uso futuros sem conter conhecimento clinico hardcoded.

`interfaces` apresenta dados e recebe entradas sem decidir logica clinica.

`audit` preserva rastreabilidade, versoes e trilhas de decisao.

`tests` valida contratos, dominio, seguranca, evidencias e regressao.

## 5. Limites

Cada modulo deve ter fronteira clara.

Knowledge nao deve executar regra clinica. Reasoning nao deve conter evidencia hardcoded. Interface nao deve decidir conduta. Domain nao deve depender de application ou interface.

## 6. Dependencias Permitidas

Dependencias devem seguir as regras de camada:

- application pode coordenar domain, reasoning, safety, evidence, knowledge e audit;
- reasoning pode usar contratos de domain, knowledge, evidence e safety;
- safety pode usar domain, knowledge e evidence;
- interfaces dependem de application;
- audit recebe eventos e trilhas, sem comandar raciocinio.

## 7. Dependencias Proibidas

Proibido:

- domain depender de application;
- domain depender de interface;
- reasoning acessar dashboard diretamente;
- motores conterem evidencia hardcoded;
- knowledge conter regra executavel;
- interface decidir conduta clinica;
- dependencia circular entre modulos.

## 8. Comunicacao

Comunicacao entre modulos deve ocorrer por contratos conceituais definidos, com entradas, saidas, erros e invariantes.

## 9. Isolamento

O isolamento deve permitir testar cada modulo sem carregar toda a aplicacao futura.

Mudancas em fontes cientificas nao devem exigir alteracao em interface. Mudancas em interface nao devem alterar raciocinio clinico.

## 10. Limites do Documento

Este documento nao cria estrutura de pastas, classes, pacotes ou bibliotecas.

## 11. Declaracao Final

Module Specification define o mapa modular do PsychRx.

No PsychRx, cada modulo deve proteger sua responsabilidade para impedir mistura entre dominio, conhecimento, evidencia, raciocinio, seguranca e interface.
