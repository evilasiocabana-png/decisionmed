# DM-027 — API de formulários em modo somente referência

## Objetivo

Conectar releases externas do catálogo governado ao shell local e expor os
formulários vinculados às etapas do workflow sem receber valores clínicos.

## Contrato

- `GET /api/form-schemas/{specialty_key}/{step_key}` retorna metadados do schema,
  campo, objeto de conhecimento e fontes rastreáveis.
- Schema ausente ou catálogo não carregado retorna `404` e não cria fallback.
- O catálogo é injetável no servidor e validado integralmente antes da abertura.
- A execução local descobre `DecisionMEd-Knowledge` como repositório irmão quando
  ele existe; `--knowledge-root` permite caminho explícito.
- A interface apresenta campos `draft` apenas como referência, sem controles de
  entrada e sem envio de dados ao servidor.

## Segurança e privacidade

Toda resposta declara `clinical_execution_allowed: false`. A página não mantém
anotações livres nem aceita conteúdo de paciente. O único `POST` continua sendo
o avanço estrutural de sessão por chave de etapa.

## Reversão

Reverter o commit desta missão remove a API, a visualização e a carga opcional do
catálogo, preservando o loader e o catálogo externo.
