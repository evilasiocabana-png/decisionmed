# ADR DM-002 — Resolução segura de SpecialtyPack

## Status

Aceito em 2026-07-21.

## Contexto

A DM-001 criou o `SpecialtyPack` como manifesto imutável de composição e
registrou Psiquiatria em estado `reference_only`. O passo seguinte precisa
resolver as capacidades exigidas pelo pacote sem importar conhecimento clínico,
executar motores ou criar um caminho implícito de ativação.

A arquitetura herdada do PsychRx exige contratos explícitos, prioridade da
segurança, rastreabilidade e interrupção do fluxo quando dependências estiverem
ausentes. A ADR DM-001 também exige revisão antes de qualquer forma de
carregamento ou ativação.

## Decisão

Criar `SpecialtyPackResolver` como componente de composição da aplicação. O
resolver recebe descritores versionados de capacidades e produz somente um
`SpecialtyLoadResult` auditável.

Estados permitidos nesta missão:

- `blocked`: falta capacidade obrigatória ou o pacote foi retirado;
- `reference_only`: composição completa, sem autorização clínica;
- `ready_for_validation`: manifesto marcado como ativo, mas ainda dependente de
  um gate clínico futuro.

Nenhum estado da DM-002 permite execução clínica. A propriedade
`clinical_execution_allowed` permanece sempre falsa.

Os bindings iniciais apontam para componentes estruturais do baseline do
PsychRx como descritores. Eles não importam nem executam o código do baseline.

## Alternativas consideradas

### Importar diretamente os motores do PsychRx

Rejeitada porque criaria acoplamento prematuro e poderia contornar contratos de
aplicação, segurança e evidência.

### Tratar presença do pacote como ativação

Rejeitada porque registro e disponibilidade técnica não equivalem a validação
clínica ou autorização de uso.

### Resolver descritores e manter gate fechado

Aceita porque torna dependências e falhas visíveis sem introduzir comportamento
clínico.

## Consequências

- Psiquiatria pode ser carregada e inspecionada pelo núcleo de composição;
- capacidades ausentes produzem bloqueios explícitos;
- cada resultado possui `trace_id` derivado do namespace de auditoria;
- nenhum motor, interface, banco ou conhecimento científico é acionado;
- uma missão futura será necessária para validar adapters reais.

## Riscos e mitigações

- **Binding confundido com implementação:** o objeto contém apenas identificador
  e versão.
- **Ativação acidental:** não existe resultado com execução permitida.
- **Dependência silenciosa:** capacidades ausentes são enumeradas no resultado.
- **Colisão de providers:** bindings duplicados são rejeitados.

## Rollback

Reverter os cinco arquivos da DM-002. A DM-001 e o baseline permanecem
funcionais e não exigem migração.

## Critérios de revisão

Revisar esta ADR antes de criar adapters executáveis, importar módulos do
baseline, integrar interface ou permitir qualquer execução clínica.
