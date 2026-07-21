# 147 - Live Clinical Snapshot

## 1. Objetivo

Definir o Live Clinical Snapshot como a representacao dinamica do estado clinico durante a consulta no Clinical Workspace.

Este documento nao implementa software, IA, Clinical Kernel ou algoritmo de raciocinio. Ele define como o Snapshot deve aparecer e se comportar conceitualmente no workspace.

## 2. Missao

O Live Clinical Snapshot deve organizar, em uma area visivel da consulta:

- dados clinicos ja registrados;
- sintomas atuais;
- hipoteses em avaliacao;
- objetivos em construcao;
- restricoes conhecidas;
- riscos pendentes;
- informacoes ausentes;
- incertezas abertas;
- mudancas relevantes durante a consulta.

O Snapshot mostra o estado.

O Snapshot nao conclui diagnostico.

O Snapshot nao prescreve.

O Snapshot nao substitui o medico.

## 3. Posicao no Clinical Workspace

O Live Clinical Snapshot pertence a:

```text
PHASE 01 - Consultation Experience
SPRINT 18 - Consultation Workspace
REGIAO - Patient Context
```

Ordem conceitual:

```text
Patient Header
-> Current Medication
-> Live Clinical Snapshot
-> Live Question Panel
-> Risk Panel
-> Clinical Strategy Card
```

## 4. Responsabilidades

O Live Clinical Snapshot deve:

- consolidar o estado clinico atual da consulta;
- diferenciar dado informado, dado ausente, hipotese e incerteza;
- indicar quando informacoes de seguranca ainda nao foram avaliadas;
- atualizar sua representacao conforme dados forem registrados em missoes futuras;
- preparar o Live Question Panel;
- preservar rastreabilidade futura.

## 5. Informacoes Permitidas

O Snapshot pode conter, conceitualmente:

- sintomas principais;
- intensidade informada;
- curso temporal informado;
- hipoteses em avaliacao;
- dados ausentes;
- objetivos ainda nao confirmados;
- restricoes conhecidas;
- status de seguranca;
- status de incerteza;
- ultima atualizacao.

## 6. Informacoes Proibidas

O Snapshot nao deve conter:

- diagnostico final automatico;
- recomendacao de tratamento;
- prescricao;
- ajuste de dose;
- estrategia desbloqueada sem risco;
- conclusao sem justificativa;
- informacao clinica sem fonte futura;
- orientacao direta ao paciente.

## 7. Estados Conceituais

O Live Clinical Snapshot pode apresentar estados:

```text
Empty
Incomplete
Collecting
Safety pending
Ready for review
Updated
Requires physician review
```

Esses estados sao comunicacionais. Eles nao disparam conduta.

## 8. Atualizacao Durante a Consulta

O termo "Live" significa que a representacao deve acompanhar a consulta.

Nesta fase, isso e uma definicao conceitual.

Futuras implementacoes poderao atualizar o Snapshot quando:

- um sintoma for registrado;
- uma pergunta for respondida;
- um risco for identificado;
- um dado ausente for preenchido;
- uma hipotese for adicionada ou removida;
- uma informacao for marcada como incerta.

## 9. Relacao com Live Question Panel

O Snapshot fornece contexto para perguntas.

O Live Question Panel mostra lacunas que precisam ser preenchidas.

```text
Live Clinical Snapshot
-> mostra estado e lacunas

Live Question Panel
-> transforma lacunas em perguntas relevantes
```

## 10. Relacao com Risk Panel

O Snapshot pode sinalizar seguranca pendente.

O Risk Panel e o local responsavel por destacar riscos.

O Snapshot nao deve liberar Strategy Card.

## 11. Relacao com Clinical Kernel Futuro

O Live Clinical Snapshot sera consumidor futuro do Clinical Kernel.

Ele nao e o Kernel.

Ele nao raciocina sozinho.

Ele nao executa motores.

Ele apenas apresenta estado clinico organizado.

## 12. Exemplo Textual

Exemplo sem dados reais:

```text
Live Clinical Snapshot
Status: incomplete
Symptoms: pending review
Hypotheses: not established
Safety: pending
Missing data: sleep, suicidality, substance use, adherence
Last update: current consultation
```

Este exemplo e estrutural e nao representa caso clinico real.

## 13. Dependencias

Depende de:

- `144_CONSULTATION_LAYOUT.md`;
- `145_PATIENT_HEADER_CARD.md`;
- `146_CURRENT_MEDICATION_CARD.md`;
- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`;
- `adr/0010_CLINICAL_WORKSPACE_PRIORITY.md`;
- `PROJECT_DEPENDENCIES.md`;
- `PROJECT_GLOSSARY.md`.

## 14. Criterios de Aceite

O Live Clinical Snapshot esta aceito quando:

- define Snapshot como representacao dinamica;
- nao implementa software;
- nao cria IA;
- nao cria Clinical Kernel;
- nao decide diagnostico;
- nao prescreve;
- diferencia dados, lacunas, hipoteses e incertezas;
- prepara o Live Question Panel;
- preserva medico como decisor final.

## Declaracao Final

O Live Clinical Snapshot e a superficie dinamica do estado clinico dentro do Clinical Workspace. Ele organiza o que se sabe, o que falta saber e o que ainda exige revisao medica, sem raciocinar sozinho, sem prescrever e sem substituir o Clinical Kernel futuro.
