# DM-017 — Contrato estrutural de ClinicalSnapshot

## Resultado

O Domain Core agora possui um `ClinicalSnapshot` imutável, versionado,
rastreável e independente de interface, persistência ou motor clínico.

O contrato segue o vocabulário oficial do PsychRx e torna explícitas as seções
ausentes. Uma estrutura com todas as seções alcança apenas o estado
`awaiting_human_validation`; ela nunca autoriza execução clínica.

## Privacidade

- o sujeito é representado somente por `SubjectReference` gerado e
  pseudonimizado;
- nome, CPF, e-mail e identificador de prontuário não pertencem ao contrato;
- não existe serialização, API ou persistência desta informação nesta missão;
- a futura entrada de dados permanece bloqueada até haver controles próprios de
  autenticação, privacidade e retenção.

## Limites clínicos

`ClinicalObservation` aceita apenas valores primitivos, finitos e limitados. O
significado de cada campo deverá vir de conhecimento validado da especialidade.
Não há diagnóstico, interpretação, prescrição, recomendação ou regra clínica.

## Reversão

Remover `decisionmed/domain/clinical_snapshot.py`, seus exports e testes restaura
o estado anterior sem migração de dados, pois não há armazenamento.
