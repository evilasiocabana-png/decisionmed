# ADR 0005 - Clinical Experience Layer

## ID da Decisao

ADR-0005

## Data

2026-06-30

## Status

Aceita

## Contexto

O PsychRx precisa ser utilizavel durante uma consulta real. A arquitetura ja descrevia dominio, conhecimento, evidencia, raciocinio, seguranca, aplicacao e interface, mas faltava uma camada oficial para transformar o raciocinio em experiencia de consulta rapida, silenciosa e centrada no paciente.

## Decisao

Criar oficialmente a `Clinical Experience Layer`:

```text
clinical_experience/
```

Componentes oficiais:

- `consultation_room/`
- `clinical_card_stack/`
- `guided_anamnesis/`
- `live_question_panel/`
- `symptom_capture/`
- `strategy_panel/`
- `risk_panel/`
- `monitoring_timeline/`
- `evidence_summary/`
- `patient_friendly_mode/`

Tambem criar superficies conceituais de interface:

- `interfaces/desktop_dashboard/`
- `interfaces/tablet_view/`
- `interfaces/mobile_view/`

## Alternativas Consideradas

1. Colocar experiencia clinica dentro de `interfaces/`.
2. Colocar experiencia clinica dentro de `application/`.
3. Criar `clinical_experience/` como camada propria.

A terceira alternativa foi escolhida porque a experiencia de consulta possui responsabilidade propria: organizar a consulta sem decidir conduta.

## Justificativa

Separar a Clinical Experience Layer impede que interface, aplicacao e raciocinio se misturem. A camada pode definir Consultation Room, Guided Anamnesis, Live Question Panel, Clinical Card Stack, Risk Panel, Strategy Panel e Patient Friendly Mode sem transformar componentes visuais em motores clinicos.

## Impacto

- adiciona nova camada oficial ao repositorio;
- torna UX clinica parte da arquitetura;
- reforca que experiencia organiza a consulta, mas nao prescreve;
- cria fronteira entre aplicacao e interfaces visuais.

## Riscos

- a camada ser confundida com UI final;
- perguntas sugeridas virarem diagnostico automatico;
- Strategy Panel parecer prescricao;
- Risk Panel ser ocultado por conveniencia visual.

## Mitigacoes

- dependencia permitida apenas por contratos da `application/`;
- proibicao explicita de prescricao;
- Risk Panel sempre precede Strategy Panel;
- medico permanece decisor final;
- rastreabilidade e explicabilidade permanecem obrigatorias.

## Documentos Afetados

- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`
- `docs/LAYER_DEPENDENCY_RULES.md`
- `docs/LOCALHOST_APP.md`
- `clinical_experience/README.md`
- `interfaces/desktop_dashboard/README.md`
- `interfaces/tablet_view/README.md`
- `interfaces/mobile_view/README.md`

## Criterios de Revisao Futura

Revisar quando:

- a UX clinica for implementada de forma interativa;
- Guided Anamnesis ganhar comportamento computacional;
- Strategy Panel passar a consumir motores reais;
- Patient Friendly Mode usar IA assistiva;
- houver autenticacao, persistencia ou dados reais.

## Declaracao Final

A Clinical Experience Layer torna o PsychRx utilizavel em consulta real sem deslocar o paciente do centro, sem substituir o medico e sem transformar a interface em prescritor.
