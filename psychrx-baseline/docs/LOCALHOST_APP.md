# PsychRx Localhost App

## Objetivo

Entregar um app local funcional para visualizar a arquitetura clinica do PsychRx em modo read-only.

## Como Executar

```text
python scripts\run_localhost.py --host 127.0.0.1 --port 8765
```

URL:

```text
http://127.0.0.1:8765
```

## Arquitetura

```text
interfaces/web
-> application/PsychRxAppService
-> application/PsychRxAppViewModel
```

A interface depende apenas da camada `application`.

## Limites

O app:

- nao prescreve;
- nao recomenda dose;
- nao cria estrategia terapeutica;
- nao executa motor clinico;
- nao usa IA;
- nao acessa banco de dados;
- nao contem dados reais de pacientes.

## Funcionalidades

- status do produto;
- contrato de seguranca clinica;
- Consultation MVP read-only com regioes Patient Context, Clinical Inquiry, Safety and Strategy, Monitoring and Explanation;
- Patient Header Card;
- Current Medication Card;
- Clinical Snapshot planejado;
- Clinical Investigation Panel demonstrativo read-only com perguntas estaticas priorizadas;
- Objectives Widget read-only com objetivos conceituais sem calculo dinamico;
- Risk Widget read-only com categorias conceituais de risco sem calculo real;
- Strategy Widget bloqueado com texto explicito de indisponibilidade terapeutica;
- Monitoring Widget read-only;
- Investigation Workflow, Clinical Compass, Missing Information Widget, Consultation Progress Widget e Dynamic Question States;
- Clinical Widget Framework, Widget Registry, Widget State Model e Widget Visibility Rules;
- Consultation, Clinical, Medication, Symptom e Response Timelines;
- fluxo conceitual de raciocinio;
- trilhas enterprise;
- paineis conceituais do dashboard medico.
- Clinical Experience Layer com seus componentes oficiais.

## Testes

Validar com:

```text
python -m unittest discover -s tests -t .
```

## Declaracao Final

O app localhost e uma superficie read-only de apresentacao da arquitetura do PsychRx, nao uma ferramenta assistencial prescritiva.
