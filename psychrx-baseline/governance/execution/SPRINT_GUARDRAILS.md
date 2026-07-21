# Sprint Guardrails

## 1. Proposito

Este documento define regras obrigatorias para evitar retrabalho, regressoes e crescimento desorganizado no PsychRx.

Ele deve funcionar como barreira contra caos arquitetural. Toda sprint, missao do Codex, Pull Request ou decisao estrutural deve respeitar estes guardrails.

## 2. Regra Central

O PsychRx deve evoluir por passos pequenos, rastreaveis e arquiteturalmente coerentes.

Nenhuma entrega deve crescer alem do escopo necessario. Nenhuma pressa operacional justifica misturar dominio, conhecimento, evidencia, raciocinio, seguranca, aplicacao, interface e auditoria.

## 3. Regras Obrigatorias

### 1. Uma missao por vez

Cada missao deve ter um unico objetivo principal.

Nao misturar documentacao, arquitetura, implementacao, teste e interface na mesma missao sem necessidade explicita.

### 2. Escopo pequeno

Toda missao deve alterar o menor numero possivel de arquivos.

Escopo pequeno reduz risco, facilita revisao, permite rollback e evita efeitos colaterais.

### 3. Nenhuma entidade nova sem Ontologia

Qualquer nova entidade clinica deve atualizar ou referenciar a Ontologia oficial.

Entidade clinica criada fora da Ontologia gera ambiguidade, duplicacao e retrabalho.

### 4. Nenhum motor novo sem documento arquitetural

Antes de criar qualquer motor clinico, deve existir documento arquitetural definindo:

- responsabilidade;
- limites;
- entradas e saidas conceituais;
- relacao com seguranca;
- relacao com evidencia;
- explicabilidade;
- rastreabilidade;
- testes esperados.

### 5. Nenhuma regra clinica sem fonte

Toda regra clinica deve possuir evidencia rastreavel.

Sem fonte, a regra nao pode entrar como conhecimento oficial.

### 6. Nenhuma recomendacao sem explicacao

Toda recomendacao, comparacao ou sugestao clinica deve possuir `ClinicalExplanation`.

Explicacao deve incluir dados usados, incertezas, fontes, riscos, objetivos e limites.

### 7. Nenhuma estrategia sem avaliacao de seguranca

Nenhuma `TherapeuticStrategy` pode ser apresentada sem avaliacao previa de seguranca clinica.

Seguranca vem antes de estrategia.

### 8. Nenhuma alteracao estrutural sem ADR

Toda mudanca estrutural relevante deve possuir ADR correspondente.

Inclui:

- nova pasta oficial;
- nova camada;
- mudanca de dependencia;
- mudanca de responsabilidade;
- excecao arquitetural;
- reorganizacao relevante.

### 9. Nenhum codigo sem teste

Qualquer codigo futuro deve vir acompanhado de teste proporcional ao risco.

Motores clinicos exigem, no minimo:

- testes unitarios;
- testes de contrato;
- cenarios clinicos simulados;
- testes de seguranca;
- testes de rastreabilidade da evidencia.

### 10. Nenhuma interface decidindo logica clinica

Interface coleta e apresenta. Interface nao decide.

A Interface Layer nao pode:

- escolher conduta;
- interpretar evidencia;
- reduzir severidade de alerta;
- criar recomendacao;
- aplicar regra clinica;
- ocultar risco;
- substituir raciocinio, seguranca ou aplicacao.

## 4. Sinais de Alerta de Retrabalho Futuro

Os sinais abaixo indicam risco alto de retrabalho, regressao ou caos arquitetural.

### Duplicacao de conceitos

Ocorre quando o mesmo conceito aparece em mais de um lugar com definicoes diferentes.

Exemplo: estabilidade definida de forma diferente em documentos distintos.

### Nomes diferentes para mesma entidade

Ocorre quando sinonimos nao autorizados passam a circular.

Exemplo: usar `Drug` em um lugar e `PsychopharmacologicalAgent` em outro.

### Logica clinica em multiplos lugares

Ocorre quando a mesma regra clinica aparece em Safety, Reasoning, Application e Interface ao mesmo tempo.

Isso dificulta auditoria e aumenta risco de contradicao.

### Conhecimento hardcoded

Ocorre quando evidencia, contraindicação, interacao ou regra terapeutica fica embutida em motor, aplicacao ou interface.

Conhecimento deve estar em Knowledge/Evidence, com fonte e versao.

### Dependencia circular

Ocorre quando camadas passam a depender umas das outras em ciclo.

Exemplo: Application depende de Interface e Interface depende de Application para definir regra.

Dependencia circular enfraquece fronteiras e dificulta testes.

### Testes frageis

Ocorre quando testes verificam detalhes superficiais, mas nao protegem comportamento clinico, contratos, seguranca, rastreabilidade ou explicabilidade.

Teste fragil cria falsa seguranca.

### Ausencia de rastreabilidade

Ocorre quando uma saida nao pode ser ligada a:

- ClinicalSnapshot;
- dados usados;
- evidencia;
- versao;
- regra;
- alerta;
- justificativa.

Ausencia de rastreabilidade bloqueia maturidade clinica.

### Pressa para criar interface antes dos motores

Interface antes dos motores pode empurrar decisao clinica para a camada errada.

Antes de interface madura, o projeto precisa de:

- dominio claro;
- conhecimento estruturado;
- evidencia rastreavel;
- safety definido;
- reasoning definido;
- contratos de aplicacao;
- testes.

## 5. Checklist de Sprint

Antes de iniciar uma sprint:

- existe uma missao clara?
- o escopo e pequeno?
- os arquivos permitidos estao definidos?
- os arquivos proibidos estao definidos?
- ha risco de nova entidade clinica?
- ha necessidade de atualizar Ontologia?
- ha regra clinica nova?
- ha fonte cientifica rastreavel?
- ha mudanca estrutural?
- ha ADR correspondente?
- ha impacto em testes?
- ha impacto em rastreabilidade?

Antes de concluir uma sprint:

- nenhuma regra obrigatoria foi violada?
- nenhum arquivo fora do escopo foi alterado?
- nenhuma dependencia proibida foi criada?
- nenhuma explicabilidade foi removida?
- nenhuma rastreabilidade foi perdida?
- testes foram executados ou justificados?
- rollback e possivel?
- documentacao foi atualizada?

## 6. Criterio de Bloqueio

Uma sprint ou missao deve ser bloqueada se:

- criar entidade clinica sem Ontologia;
- criar motor sem arquitetura;
- criar regra clinica sem fonte;
- criar recomendacao sem explicacao;
- criar estrategia sem seguranca;
- alterar estrutura sem ADR;
- criar codigo sem teste;
- permitir interface decidir logica clinica;
- introduzir dependencia circular;
- remover rastreabilidade;
- misturar conhecimento com algoritmo.

## 7. Relacao com Documentos Oficiais

Estes guardrails devem ser usados junto com:

- `docs/CODEX_DEFINITION_OF_DONE.md`;
- `docs/CODEX_MISSION_TEMPLATE.md`;
- `docs/LAYER_DEPENDENCY_RULES.md`;
- `docs/ARCHITECTURE_REPOSITORY_STRUCTURE.md`;
- `docs/CLINICAL_SAFETY_CONTRACT.md`;
- `docs/EVIDENCE_TRACEABILITY_POLICY.md`;
- `docs/TESTING_POLICY.md`;
- `docs/NAMING_CONVENTIONS.md`;
- `docs/adr/0001_GOVERNANCA_ARQUITETURAL.md`.

## 8. Declaracao Final

Os Sprint Guardrails existem para manter o PsychRx pequeno o suficiente para ser revisavel e rigoroso o suficiente para ser confiavel.

O projeto deve crescer por decisoes explicitas, fontes rastreaveis, camadas separadas, testes proporcionais e explicabilidade preservada. Qualquer sprint que acelere sacrificando essas fronteiras cria divida arquitetural e risco clinico.
