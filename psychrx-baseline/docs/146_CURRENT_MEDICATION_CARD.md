# 146 - Current Medication Card

## 1. Objetivo

Definir o Current Medication Card como componente conceitual da consulta no PsychRx.

Este card organiza o tratamento atual do paciente de forma clara, rastreavel e segura, sem transformar medicacao vigente em prescricao automatica e sem sugerir alteracao terapeutica.

## 2. Missao

O Current Medication Card deve permitir ao medico visualizar rapidamente:

- quais medicamentos o paciente usa atualmente;
- quais informacoes do tratamento atual estao completas;
- quais informacoes ainda precisam ser confirmadas;
- quais itens exigem atencao de seguranca futura;
- como o tratamento atual se relaciona com o Clinical Snapshot.

O card organiza informacao.

O card nao recomenda.

O card nao prescreve.

O card nao altera conduta.

## 3. Posicao no Consultation Layout

O Current Medication Card pertence a:

```text
REGIAO 1 - Patient Context
```

Ele deve aparecer depois do Patient Header Card e antes de qualquer Strategy Card.

Ordem conceitual:

```text
Patient Header Card
-> Current Medication Card
-> Clinical Snapshot Card
-> Live Question Panel
-> Risk Panel
-> Strategy Card
```

## 4. Responsabilidades

O Current Medication Card deve:

- representar tratamento atual;
- separar medicacao vigente de estrategia futura;
- destacar dados incompletos;
- apoiar identificacao futura de interacoes, efeitos adversos e adesao;
- preservar rastreabilidade;
- lembrar que qualquer mudanca pertence ao medico.

## 5. Informacoes Permitidas

O card pode conter, conceitualmente:

- nome oficial do agente psicofarmacologico, quando disponivel;
- dose informada;
- frequencia informada;
- tempo de uso;
- indicacao relatada ou objetivo associado;
- adesao relatada;
- efeitos adversos relatados;
- uso recente, suspenso ou irregular;
- informacoes ausentes;
- necessidade de confirmacao pelo medico.

## 6. Informacoes Proibidas

O card nao deve conter:

- recomendacao de iniciar medicamento;
- recomendacao de suspender medicamento;
- recomendacao de ajustar dose;
- substituicao sugerida;
- combinacao sugerida;
- calculo automatico de conduta;
- equivalencia terapeutica sem fonte futura;
- alerta conclusivo sem avaliacao de seguranca.

## 7. Separacao Entre Tratamento Atual e Estrategia

O Current Medication Card descreve o que existe.

O Strategy Card descrevera alternativas futuras.

```text
Current Medication Card = estado atual
Strategy Card = possibilidades revisaveis
Medical Decision = decisao do medico
```

Essa separacao impede que a interface transforme historico de medicacao em prescricao.

## 8. Relacao com Safety

O card pode sinalizar que existem dados necessarios para avaliacao de seguranca.

Exemplos conceituais permitidos:

```text
Dose status: not confirmed
Adherence status: unknown
Adverse effects: requires review
Interaction review: pending
```

Exemplos proibidos:

```text
Increase dose
Switch medication
Safe to combine
Continue automatically
```

A avaliacao de risco pertence ao Risk Panel e ao Safety First Engine futuro.

## 9. Relacao com Clinical Snapshot

O Current Medication Card alimenta contexto para o Clinical Snapshot, mas nao substitui o snapshot.

Relacao:

```text
Current Medication Card
-> tratamento atual informado

Clinical Snapshot Card
-> estado clinico dinamico integrado
```

## 10. Relacao com Monitorizacao

O card pode indicar que monitorizacao futura sera necessaria, mas nao define plano completo.

Exemplo conceitual:

```text
Monitoring need: pending clinical review
```

O plano pertence ao Monitoring Card.

## 11. Estados Conceituais

O card pode possuir estados:

```text
No medication reported
Medication list incomplete
Medication list reported
Dose incomplete
Adherence unknown
Adverse effects reported
Requires safety review
```

Esses estados sao informativos e nao decidem conduta.

## 12. Exemplo Textual

Exemplo sem dados reais:

```text
Current Medication
Agent: PsychopharmacologicalAgent-001
Dose: informed, not validated
Frequency: informed
Duration: unknown
Adherence: requires review
Adverse effects: requires review
Safety review: pending
```

Este exemplo e estrutural. Ele nao representa caso clinico real e nao deve ser usado como recomendacao.

## 13. Dependencias

Depende de:

- `144_CONSULTATION_LAYOUT.md`;
- `145_PATIENT_HEADER_CARD.md`;
- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`;
- `PROJECT_GLOSSARY.md`;
- `PROJECT_DEPENDENCIES.md`;
- `adr/0005_CLINICAL_EXPERIENCE_LAYER.md`;
- `adr/0009_CLINICAL_EXPERIENCE_PRECEDES_DASHBOARD.md`.

## 14. O Que Nao Pertence ao Current Medication Card

Nao pertence a este card:

- decisao terapeutica;
- recomendacao de ajuste;
- estrategia de troca;
- comparacao de estrategias;
- calculo de dose;
- avaliacao completa de interacao;
- plano de monitorizacao completo;
- instrucao direta ao paciente.

## 15. Criterios de Aceite

O Current Medication Card esta aceito quando:

- organiza tratamento atual sem prescrever;
- separa medicacao vigente de estrategia futura;
- identifica informacoes ausentes;
- preserva privacidade e rastreabilidade;
- nao interpreta risco de forma conclusiva;
- nao gera recomendacao terapeutica;
- prepara o Live Question Panel como proximo componente;
- preserva o medico como decisor final.

## Declaracao Final

O Current Medication Card organiza o tratamento atual como contexto clinico da consulta, sem transformar medicamento vigente em prescricao, sem sugerir mudanca terapeutica e sem substituir a avaliacao medica.
