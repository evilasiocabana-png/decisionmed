# ADR 0004 - Localhost App Shell

## ID da Decisao

ADR-0004

## Data

2026-06-30

## Status

Aceita

## Contexto

O projeto precisava de um app funcional em localhost sem iniciar implementacao clinica completa, sem escolher framework e sem violar a separacao entre interface e raciocinio clinico.

## Decisao

Criar um app local read-only usando apenas a biblioteca padrao do Python para servir arquivos estaticos e um endpoint JSON de estado.

## Alternativas Consideradas

- Criar app com framework web.
- Criar app Streamlit.
- Criar apenas arquivo HTML sem servidor.
- Criar servidor local com biblioteca padrao.

A ultima alternativa foi escolhida para reduzir dependencia tecnica e evitar decisao prematura de framework.

## Impacto

- cria `application/app_service.py`;
- cria `application/app_view_model.py`;
- cria `interfaces/web/`;
- cria `scripts/run_localhost.py`;
- adiciona testes de contrato.

## Riscos

- o app e uma casca inicial e ainda nao executa motores clinicos;
- futuras telas devem continuar passando pela camada application;
- qualquer comportamento clinico futuro exigira contratos, fontes e testes.

## Documentos Afetados

- `docs/LOCALHOST_APP.md`
- `application/`
- `interfaces/web/`
- `tests/application/`
- `tests/interfaces/`

## Criterios de Revisao Futura

Revisar esta decisao quando:

- um framework web for proposto;
- houver API clinica real;
- houver autenticacao;
- houver persistencia;
- motores clinicos forem implementados.

## Declaracao Final

O Localhost App Shell entrega uma interface funcional e segura para visualizar o PsychRx sem criar prescritor, motor clinico ou dependencia de framework.
