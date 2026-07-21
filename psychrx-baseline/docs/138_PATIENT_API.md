# 138 Patient API

## Objetivo

Definir conceitualmente a API de paciente.

## Responsabilidades

- expor dados autorizados do paciente;
- preservar identidade e privacidade;
- conectar paciente a snapshots e timelines;
- evitar duplicidade de identidade clinica.

## Regras

- paciente e centro do dominio;
- dados sensiveis exigem seguranca;
- API nao deve expor informacao alem do necessario;
- historico clinico deve ser rastreavel.

## Declaracao Final

A Patient API existe para organizar contexto clinico do paciente, nao para automatizar decisoes terapeuticas.
