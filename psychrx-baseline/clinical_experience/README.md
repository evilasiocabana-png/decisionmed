# Clinical Experience Layer

## Finalidade

A Clinical Experience Layer transforma o raciocinio do PsychRx em uma experiencia rapida, silenciosa e util durante a consulta.

Ela organiza a consulta. Ela nao decide conduta.

Ela nao prescreve.

## Responsabilidades

- estruturar a experiencia da consulta;
- apresentar perguntas relevantes;
- organizar sintomas;
- tornar riscos sempre visiveis;
- apresentar estrategias como alternativas revisaveis;
- apoiar monitorizacao longitudinal;
- traduzir explicacoes para linguagem adequada ao paciente.

## Nao Pode

- prescrever;
- escolher estrategia pelo medico;
- criar regra terapeutica;
- acessar evidencia diretamente para decidir;
- substituir Safety First;
- ocultar riscos;
- transformar UI em motor clinico.

## Subcomponentes

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

## Dependencias

Pode depender de contratos da `application/`.

Nao deve depender diretamente de `domain/`, `knowledge/`, `evidence/`, `reasoning/` ou `safety/` para decidir comportamento clinico.

## Declaracao Final

A Clinical Experience Layer existe para tornar o PsychRx utilizavel em consulta real sem retirar o paciente do centro e sem retirar a decisao do medico.
