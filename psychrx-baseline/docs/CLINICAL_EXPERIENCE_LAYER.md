# Clinical Experience Layer

## Objetivo

Definir oficialmente a Clinical Experience Layer como camada arquitetural do PsychRx.

## Funcao

Transformar o raciocinio do PsychRx em uma experiencia rapida, silenciosa e util durante a consulta.

Ela nao decide conduta.

Ela nao prescreve.

Ela organiza a consulta.

## Estrutura Oficial

```text
clinical_experience/
├── consultation_room/
├── clinical_card_stack/
├── guided_anamnesis/
├── live_question_panel/
├── symptom_capture/
├── strategy_panel/
├── risk_panel/
├── monitoring_timeline/
├── evidence_summary/
└── patient_friendly_mode/
```

## Relacao Com Interfaces

```text
interfaces/
├── desktop_dashboard/
├── tablet_view/
└── mobile_view/
```

As interfaces apresentam a experiencia clinica. Elas nao definem regra clinica.

## Componentes

### Consultation Room

Tela principal da consulta. Mostra paciente, sintomas atuais, hipoteses, tratamento atual, riscos, estrategias, plano e monitorizacao.

### Guided Anamnesis

Sugere perguntas objetivas para o medico durante a fala do paciente. As perguntas reduzem incerteza, mas nao diagnosticam automaticamente.

### Live Question Panel

Painel de perguntas importantes no momento. Deve conter poucas perguntas de alta relevancia.

### Symptom Capture

Captura rapida de sintomas, intensidade, padrao e necessidade de investigacao.

### Clinical Card Stack

Organiza informacoes clinicas em cards legiveis e rastreaveis.

### Strategy Panel

Mostra estrategias conceituais possiveis, como manter, ajustar, substituir, associar, retirar gradualmente ou monitorar antes de alterar.

Nao mostra prescricao automatica.

### Risk Panel

Mantem riscos sempre visiveis: suicidio, interacoes, QT, gestacao, sedacao, risco metabolico e outros limites.

### Monitoring Timeline

Organiza o plano longitudinal: hoje, duas semanas, seis semanas, tres meses e outros marcos definidos pelo medico.

### Evidence Summary

Resume evidencias com fonte, qualidade, conflito, aplicabilidade e versao.

### Patient Friendly Mode

Traduz objetivos e monitorizacao para linguagem acessivel ao paciente, sem orientar automedicacao.

## Fluxo Ideal Durante a Consulta

```text
Paciente fala
-> Medico escuta
-> PsychRx sugere perguntas objetivas
-> Medico confirma sintomas
-> PsychRx atualiza Clinical Snapshot
-> PsychRx mostra riscos
-> PsychRx organiza estrategias possiveis
-> Medico decide
-> PsychRx organiza plano e monitorizacao
```

## Dependencias Permitidas

```text
Clinical Experience -> Application
Interface -> Clinical Experience
```

## Dependencias Proibidas

```text
Clinical Experience -> Knowledge direto para sugerir estrategia
Clinical Experience -> Evidence direto para gerar conclusao
Clinical Experience -> Reasoning direto para contornar Application
Clinical Experience -> Safety direto para alterar alerta
Clinical Experience -> decisao clinica final
```

## Limites

- nao prescreve;
- nao escolhe estrategia;
- nao substitui julgamento medico;
- nao oculta riscos;
- nao cria regra terapeutica;
- nao usa evidencia sem rastreabilidade;
- nao transforma interface em motor clinico.

## Declaracao Final

A Clinical Experience Layer torna o PsychRx utilizavel em consulta real, mantendo o paciente no centro, o medico como decisor final e a seguranca clinica como primeira camada.
