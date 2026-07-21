# 137 Case API

## Objetivo

Definir conceitualmente a API de casos clinicos.

## Responsabilidades

- receber dados de caso;
- expor estado do caso;
- preservar historico;
- associar caso a paciente, snapshot, hipoteses e objetivos.

## Regras

- caso nao e prescricao;
- caso deve manter rastreabilidade;
- atualizacoes devem ser auditaveis;
- dados incompletos devem gerar incerteza.

## Declaracao Final

A Case API organiza casos para raciocinio clinico rastreavel sem decidir conduta.
