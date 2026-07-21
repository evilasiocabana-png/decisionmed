# 145 - Patient Header Card

## 1. Objetivo

Definir o Patient Header Card como o primeiro card conceitual da consulta no PsychRx.

Este card identifica o paciente, situa o medico no contexto minimo necessario e ancora a consulta sem reduzir a pessoa a um diagnostico, medicamento ou problema isolado.

## 2. Missao

O Patient Header Card deve responder, de forma rapida e segura:

- quem e o paciente;
- qual e o contexto clinico minimo da consulta;
- qual e o estado de privacidade e identificacao;
- qual e o vinculo longitudinal com a consulta atual;
- quais informacoes essenciais ainda faltam.

O card organiza identidade e contexto.

O card nao diagnostica.

O card nao prescreve.

O card nao decide conduta.

## 3. Posicao no Consultation Layout

O Patient Header Card pertence a:

```text
REGIAO 1 - Patient Context
```

Ele deve aparecer antes de:

- Clinical Snapshot Card;
- Current Medication Card;
- Live Question Panel;
- Risk Panel;
- Strategy Card.

## 4. Responsabilidades

O Patient Header Card deve:

- manter o paciente como primeiro eixo da consulta;
- exibir identificacao clinica minima;
- indicar contexto de atendimento;
- preservar privacidade;
- sinalizar dados essenciais ausentes;
- orientar o medico sem induzir conclusao;
- permitir continuidade longitudinal futura.

## 5. Informacoes Permitidas

O card pode conter, conceitualmente:

- identificador seguro do paciente;
- nome ou iniciais, conforme politica de privacidade futura;
- idade ou faixa etaria;
- genero quando clinicamente relevante e informado;
- data ou momento da consulta;
- tipo de consulta;
- status de dados incompletos;
- marcador de acompanhamento longitudinal;
- avisos de privacidade e confidencialidade.

## 6. Informacoes Proibidas

O card nao deve conter:

- prescricao;
- sugestao terapeutica;
- diagnostico fechado como identidade do paciente;
- julgamento de gravidade sem contexto;
- alerta clinico sem rastreabilidade futura;
- dado sensivel desnecessario;
- informacao que exponha o paciente alem do minimo necessario;
- conteudo para paciente sem supervisao medica.

## 7. Privacidade

O Patient Header Card deve seguir o principio de minimo necessario.

Regras conceituais:

- mostrar apenas dados necessarios para situar a consulta;
- evitar exposicao excessiva em tela;
- permitir modos futuros de visualizacao reduzida;
- separar identificacao administrativa de contexto clinico;
- nunca usar dados reais de paciente em exemplos de documentacao.

## 8. Relacao com Clinical Snapshot

O Patient Header Card nao substitui o Clinical Snapshot.

Relacao:

```text
Patient Header Card
-> identifica e situa

Clinical Snapshot Card
-> representa o estado clinico atual
```

O Header responde "quem e o paciente nesta consulta".

O Snapshot responde "qual e o estado clinico dinamico neste momento".

## 9. Relacao com Safety

O Patient Header Card pode sinalizar que existem dados de seguranca pendentes, mas nao deve interpretar risco.

Exemplo conceitual permitido:

```text
Safety status: incomplete
```

Exemplo conceitual proibido:

```text
Paciente seguro para estrategia X
```

Risco clinico pertence ao Risk Panel e a camada de seguranca.

## 10. Relacao com Strategy

O Patient Header Card nao deve apresentar estrategia terapeutica.

Ele tambem nao deve exibir frases que parecam recomendacao.

Strategy Card so pode aparecer depois de contexto, snapshot, perguntas e risco.

## 11. Estados Conceituais

O card pode ter estados conceituais:

```text
Identificacao completa
Identificacao parcial
Contexto incompleto
Privacidade reduzida
Consulta em andamento
Consulta longitudinal
```

Esses estados organizam a experiencia, mas nao geram decisao clinica.

## 12. Exemplo Textual

Exemplo sem dados reais:

```text
Patient Header
Identifier: PATIENT-001
Age range: adult
Consultation: follow-up
Context status: incomplete
Privacy mode: standard
```

Este exemplo e estrutural. Ele nao representa caso clinico real.

## 13. Dependencias

Depende de:

- `144_CONSULTATION_LAYOUT.md`;
- `PROGRAM_07_CLINICAL_EXPERIENCE_LAYER.md`;
- `PROJECT_GLOSSARY.md`;
- `PROJECT_DEPENDENCIES.md`;
- `adr/0005_CLINICAL_EXPERIENCE_LAYER.md`;
- `adr/0009_CLINICAL_EXPERIENCE_PRECEDES_DASHBOARD.md`.

## 14. O Que Nao Pertence ao Patient Header Card

Nao pertence a este card:

- Clinical Snapshot completo;
- lista de sintomas;
- lista de medicamentos;
- riscos detalhados;
- objetivos terapeuticos;
- estrategias;
- monitorizacao;
- evidencia cientifica;
- decisao medica.

## 15. Criterios de Aceite

O Patient Header Card esta aceito quando:

- identifica o paciente sem reduzir a pessoa ao diagnostico;
- usa apenas contexto clinico minimo;
- preserva privacidade;
- nao exibe prescricao;
- nao exibe estrategia;
- nao interpreta risco;
- nao substitui Clinical Snapshot;
- prepara o Current Medication Card como proximo componente;
- preserva o medico como decisor final.

## Declaracao Final

O Patient Header Card ancora a consulta no paciente, preservando identidade, privacidade e contexto minimo sem transformar a pessoa em diagnostico, sem gerar decisao clinica e sem antecipar estrategia terapeutica.
