# 136 API Architecture

## Objetivo

Definir a arquitetura conceitual da API Clinica do PsychRx.

## Principios

- API como camada de aplicacao, nao dominio;
- dominio independente da API;
- conhecimento cientifico separado de algoritmo;
- seguranca, auditoria e rastreabilidade obrigatorias;
- nenhuma rota deve prescrever automaticamente.

## Fronteiras

- entrada de casos;
- consulta de pacientes;
- raciocinio clinico;
- estrategias comparaveis;
- monitorizacao;
- auditoria.

## Declaracao Final

A API Architecture define contratos externos futuros sem permitir que a API contorne dominio, safety ou decisao medica.
