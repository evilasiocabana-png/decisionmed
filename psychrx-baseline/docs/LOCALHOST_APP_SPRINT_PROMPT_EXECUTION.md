# Localhost App Sprint Prompt Execution

## Nome do Sprint

Sprint Técnico - Localhost App Shell

## Missão Executada

```text
===========================================================
MISSAO LOCALHOST-001 — LOCALHOST_APP_SHELL
Sprint Técnico — Localhost App Shell
Projeto: PsychRx
===========================================================

Voce esta trabalhando no projeto PsychRx.

Leia obrigatoriamente todos os documentos anteriores antes de iniciar.

Objetivo

Criar um app local funcional em localhost para apresentar o PsychRx em modo read-only.

Conteudo obrigatorio

- app em localhost funcional;
- interface dependente apenas da camada application;
- ViewModel unico para a UI;
- status de seguranca clinica visivel;
- fluxo conceitual de raciocinio;
- trilhas enterprise;
- dashboard medico conceitual;
- testes automatizados;
- ADR correspondente;
- documentacao de execucao.

Restricoes

- Nao criar prescritor.
- Nao criar motor clinico.
- Nao criar regra terapeutica.
- Nao criar IA.
- Nao criar banco de dados.
- Nao criar dados reais de paciente.
- Nao fazer interface decidir conduta clinica.
- Nao misturar conhecimento cientifico com algoritmo.
- Nao introduzir framework antes de decisao arquitetural.

Criterios de aceite

- app abre em localhost;
- endpoint de health responde;
- endpoint de estado retorna JSON;
- UI renderiza PsychRx;
- testes passam;
- ADR criado;
- documentacao criada;
- seguranca read-only preservada;
- pronto para revisao CTO.
```

## Arquivos Criados ou Atualizados

- `application/__init__.py`
- `application/app_service.py`
- `application/app_view_model.py`
- `interfaces/__init__.py`
- `interfaces/web/__init__.py`
- `interfaces/web/server.py`
- `interfaces/web/static/index.html`
- `interfaces/web/static/styles.css`
- `interfaces/web/static/app.js`
- `scripts/run_localhost.py`
- `tests/application/__init__.py`
- `tests/application/test_app_service.py`
- `tests/interfaces/__init__.py`
- `tests/interfaces/test_web_app.py`
- `docs/LOCALHOST_APP.md`
- `docs/adr/0004_LOCALHOST_APP_SHELL.md`

## Arquivos Ja Existentes Validados

- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/CODEX_DEFINITION_OF_DONE.md`
- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/ROADMAP_ENTERPRISE.md`
- `docs/ROADMAP_RECONCILIATION_REPORT.md`

## Validacoes Executadas

```text
python -m unittest discover -s tests -t .
```

Resultado:

```text
Ran 25 tests
OK
```

Validacao manual por HTTP:

```text
http://127.0.0.1:8765/health
http://127.0.0.1:8765/
http://127.0.0.1:8765/api/app-state
```

Resultado:

- `/health`: 200 OK
- `/`: 200 OK
- `/api/app-state`: 200 OK

## Inconsistencias ou Bloqueios Restantes

- O app e uma casca read-only inicial e ainda nao executa motores clinicos.
- Nao ha autenticacao, persistencia, API clinica real ou IA.
- Alguns documentos antigos `.md` seguem com conteudo binario de Word, conforme registrado no relatorio de reconciliacao.
- Nao ha repositorio Git inicializado na pasta local.

## Declaracao Final

O PsychRx possui agora um app localhost funcional, read-only, testado e rastreavel, sem criar prescricao, motor clinico, IA ou regra terapeutica.

## Adendo - Clinical Experience Layer

A missao foi estendida para refletir a nova camada oficial `clinical_experience/`.

Arquivos principais adicionados:

- `clinical_experience/README.md`
- `clinical_experience/consultation_room/README.md`
- `clinical_experience/clinical_card_stack/README.md`
- `clinical_experience/guided_anamnesis/README.md`
- `clinical_experience/live_question_panel/README.md`
- `clinical_experience/symptom_capture/README.md`
- `clinical_experience/strategy_panel/README.md`
- `clinical_experience/risk_panel/README.md`
- `clinical_experience/monitoring_timeline/README.md`
- `clinical_experience/evidence_summary/README.md`
- `clinical_experience/patient_friendly_mode/README.md`
- `docs/CLINICAL_EXPERIENCE_LAYER.md`
- `docs/adr/0005_CLINICAL_EXPERIENCE_LAYER.md`

Validacoes adicionais:

```text
python -m unittest discover -s tests -t .
```

Resultado:

```text
Ran 30 tests
OK
```

O app localhost passou a exibir a Clinical Experience Layer em `/api/app-state` e na pagina principal.
