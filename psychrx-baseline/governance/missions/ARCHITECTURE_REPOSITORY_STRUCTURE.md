# Architecture Repository Structure

## 1. Proposito

Este documento define a estrutura oficial do repositorio PsychRx antes de qualquer implementacao.

Seu objetivo e separar responsabilidades arquiteturais para impedir que logica clinica, evidencia cientifica, interfaces, auditoria e aplicacao fiquem misturadas.

Esta estrutura nao cria codigo clinico, motores, recomendacoes ou implementacao. Ela define onde cada tipo de conhecimento, regra, contrato conceitual e responsabilidade deve existir.

## 2. Principio Central

O repositorio deve preservar fronteiras claras:

- `docs/` documenta;
- `domain/` modela o dominio;
- `knowledge/` organiza conhecimento clinico-cientifico estruturado;
- `reasoning/` organiza raciocinio clinico conceitual;
- `safety/` organiza seguranca clinica;
- `evidence/` organiza fontes, evidencias e rastreabilidade cientifica;
- `application/` orquestra casos de uso futuros;
- `interfaces/` expõe entradas e saidas futuras;
- `audit/` registra rastreabilidade e governanca operacional;
- `tests/` valida comportamento esperado, limites e seguranca.

Nenhuma camada deve absorver responsabilidades de outra.

## 3. Estrutura Oficial

```text
docs/
domain/
knowledge/
reasoning/
safety/
evidence/
application/
interfaces/
audit/
tests/
```

## 4. docs/

### Finalidade

Guardar documentacao oficial do projeto, incluindo arquitetura, principios clinicos, modelos conceituais, governanca, limites, glossario e decisoes.

### Pode existir

- documentos arquiteturais;
- manifestos;
- principios clinicos;
- modelos conceituais;
- definicoes de dominio;
- politicas de governanca;
- registros de decisoes;
- mapas conceituais;
- documentacao de seguranca, evidencia e rastreabilidade.

### Nao pode existir

- codigo de aplicacao;
- codigo clinico executavel;
- motores;
- regras clinicas implementadas;
- componentes de interface;
- dados sensiveis de pacientes;
- fontes cientificas brutas sem curadoria.

### Dependencias permitidas

- Pode referenciar todas as demais pastas conceitualmente.
- Pode documentar contratos e responsabilidades.

### Dependencias proibidas

- Nao pode depender de implementacao.
- Nao pode ser fonte unica de regras clinicas executaveis.
- Nao pode conter logica operacional escondida em texto para ser executada diretamente.

## 5. domain/

### Finalidade

Representar o modelo central do dominio do PsychRx: entidades, value objects, aggregates, eventos de dominio e linguagem ubíqua.

### Pode existir

- modelos conceituais de paciente;
- sintomas;
- hipoteses diagnosticas;
- objetivos terapeuticos;
- estrategias conceituais;
- psicofarmacos como objetos do dominio;
- resposta clinica;
- estabilizacao;
- eventos de dominio;
- invariantes do dominio.

### Nao pode existir

- fontes cientificas completas;
- revisoes de literatura;
- regras de seguranca implementadas;
- componentes de interface;
- orquestracao de casos de uso;
- persistencia concreta;
- chamadas externas;
- recomendacoes automaticas.

### Dependencias permitidas

- Pode depender de conceitos documentados em `docs/`.
- Pode referenciar tipos conceituais de `knowledge/` e `evidence/` sem incorporar seu conteudo.

### Dependencias proibidas

- Nao pode depender de `interfaces/`.
- Nao pode depender de `application/`.
- Nao pode depender de infraestrutura futura.
- Nao pode conter evidencia cientifica embutida.
- Nao pode conter logica de apresentacao.

## 6. knowledge/

### Finalidade

Organizar conhecimento clinico-cientifico estruturado usado pelo PsychRx, separado de codigo, interface e orquestracao.

### Pode existir

- taxonomias;
- ontologias;
- mapas de psicofarmacos;
- classes farmacologicas;
- mecanismos;
- efeitos adversos estruturados;
- interacoes estruturadas;
- contraindicações estruturadas;
- requisitos de monitorizacao;
- conhecimento versionado derivado de fontes.

### Nao pode existir

- codigo de motor clinico;
- decisoes para pacientes individuais;
- interfaces;
- casos de uso de aplicacao;
- logs;
- dados identificaveis de pacientes;
- recomendacoes finais sem contexto clinico.

### Dependencias permitidas

- Pode depender de `evidence/` para fontes e lastro cientifico.
- Pode seguir modelos definidos em `domain/`.
- Pode ser documentado por `docs/`.

### Dependencias proibidas

- Nao pode depender de `interfaces/`.
- Nao pode depender de `application/`.
- Nao pode conter regras de decisao individual.
- Nao pode misturar fonte cientifica bruta com interpretacao clinica sem versionamento.

## 7. reasoning/

### Finalidade

Organizar o raciocinio clinico conceitual do PsychRx: Clinical Operating Mind, Decision Graph, Knowledge Graph, Evidence Graph, Constraint Graph e fluxos de pensamento clinico.

### Pode existir

- modelos de raciocinio;
- mapas de decisao conceitual;
- criterios de comparacao;
- tratamento de incerteza;
- raciocinio longitudinal;
- relacao entre sintomas, hipoteses, objetivos, riscos e estabilidade;
- explicabilidade conceitual.

### Nao pode existir

- algoritmos executaveis;
- recomendacoes automaticas;
- prescricoes;
- codigo de motor;
- componentes de UI;
- fontes cientificas completas;
- dados de pacientes.

### Dependencias permitidas

- Pode depender de `domain/` para conceitos do dominio.
- Pode consultar conceitualmente `knowledge/`, `safety/` e `evidence/`.
- Pode ser documentado em `docs/`.

### Dependencias proibidas

- Nao pode depender de `interfaces/`.
- Nao pode depender de detalhes de `application/`.
- Nao pode embutir evidencia cientifica sem referencia ao `evidence/`.
- Nao pode transformar raciocinio em prescricao automatica.

## 8. safety/

### Finalidade

Organizar principios, limites, alertas, restricoes e criterios de seguranca clinica.

### Pode existir

- regras conceituais de seguranca;
- criterios de alerta;
- classes de risco;
- contraindicações como limites;
- interacoes relevantes para seguranca;
- politicas de bloqueio conceitual;
- criterios de dados ausentes criticos;
- criterios de cautela;
- relacao com monitorizacao.

### Nao pode existir

- codigo de recomendacao;
- prescricao automatica;
- UI;
- fontes cientificas sem rastreabilidade;
- orquestracao de aplicacao;
- dados reais de pacientes;
- decisoes clinicas finais.

### Dependencias permitidas

- Pode depender de `domain/` para conceitos.
- Deve depender de `evidence/` para justificativa cientifica quando aplicavel.
- Pode consumir conhecimento estruturado de `knowledge/`.
- Pode orientar `reasoning/`.

### Dependencias proibidas

- Nao pode depender de `interfaces/`.
- Nao pode depender de preferencias de apresentacao.
- Nao pode conter evidencia sem fonte.
- Nao pode ser enfraquecido por logica de conveniencia da aplicacao.

## 9. evidence/

### Finalidade

Organizar fontes cientificas, hierarquia de evidencias, versionamento, rastreabilidade, conflitos e governanca cientifica.

### Pode existir

- diretrizes;
- revisoes sistematicas;
- meta-analises;
- ensaios clinicos;
- livros-texto referenciados;
- consensos;
- regulamentacoes;
- matriz de qualidade da evidencia;
- registros de conflito entre fontes;
- versoes de evidencia;
- notas de curadoria.

### Nao pode existir

- codigo clinico;
- interface;
- dados de pacientes;
- recomendacoes individuais;
- regras executaveis;
- conhecimento sem fonte;
- conclusoes sem nivel de evidencia.

### Dependencias permitidas

- Pode referenciar `docs/` para politicas de governanca.
- Pode sustentar `knowledge/`, `safety/` e `reasoning/`.

### Dependencias proibidas

- Nao pode depender de `interfaces/`.
- Nao pode depender de `application/`.
- Nao pode ser alterado por necessidades de UI.
- Nao pode conter decisao clinica individual.

## 10. application/

### Finalidade

Organizar a orquestracao futura dos casos de uso do PsychRx, sem conter conhecimento cientifico, regras clinicas primarias ou interface.

### Pode existir

- casos de uso futuros;
- fluxos de aplicacao;
- coordenacao entre dominio, raciocinio, seguranca, evidencia e auditoria;
- contratos conceituais de entrada e saida;
- politicas de sequenciamento;
- validacoes de completude nao clinicas.

### Nao pode existir

- conhecimento cientifico embutido;
- evidencia primaria;
- regras clinicas primarias;
- componentes visuais;
- prescricao automatica;
- logica de UI;
- dados sensiveis persistidos diretamente.

### Dependencias permitidas

- Pode depender de `domain/`.
- Pode coordenar `reasoning/`, `safety/`, `knowledge/`, `evidence/` e `audit/`.
- Pode fornecer contratos para `interfaces/`.

### Dependencias proibidas

- Nao pode ser dependencia de `domain/`.
- Nao pode alterar regras de `safety/`.
- Nao pode modificar evidencia em `evidence/`.
- Nao pode decidir conteudo cientifico.

## 11. interfaces/

### Finalidade

Organizar fronteiras futuras de interacao do sistema com usuarios, sistemas externos ou superfícies de entrada e saida.

### Pode existir

- contratos de apresentacao;
- formatos de entrada;
- formatos de saida;
- prototipos conceituais de interface;
- textos de apoio ao usuario;
- mapeamento de campos para casos de uso;
- adaptadores futuros sem logica clinica.

### Nao pode existir

- regras clinicas;
- evidencia cientifica;
- motores;
- decisoes clinicas;
- prescricao automatica;
- conhecimento farmacologico;
- logica de seguranca primaria.

### Dependencias permitidas

- Pode depender de `application/` para contratos.
- Pode apresentar resultados vindos de `reasoning/`, `safety/` e `evidence/` por meio de `application/`.

### Dependencias proibidas

- Nao pode acessar diretamente `evidence/` para decidir conteudo.
- Nao pode acessar diretamente `knowledge/` para gerar recomendacao.
- Nao pode conter atalhos de decisao clinica.
- Nao pode alterar significado clinico para conveniencia visual.

## 12. audit/

### Finalidade

Organizar rastreabilidade, trilhas de decisao, versionamento operacional, registros de explicabilidade e reconstrucao de analises.

### Pode existir

- modelos de auditoria;
- registros conceituais de eventos;
- trilhas de versao;
- matriz de rastreabilidade;
- criterios de reconstrucao de analise;
- relacao entre decisao, evidencia, snapshot e usuario;
- politicas de imutabilidade conceitual.

### Nao pode existir

- regras clinicas primarias;
- evidencia cientifica como fonte principal;
- interface;
- prescricoes;
- dados sensiveis desnecessarios;
- motores de decisao.

### Dependencias permitidas

- Pode receber eventos conceituais de `application/`, `reasoning/`, `safety/` e `evidence/`.
- Pode referenciar `domain/` para identidade de eventos.
- Pode ser documentado por `docs/`.

### Dependencias proibidas

- Nao pode governar decisao clinica.
- Nao pode substituir `evidence/`.
- Nao pode alterar saidas clinicas.
- Nao pode depender de `interfaces/` para definir verdade auditavel.

## 13. tests/

### Finalidade

Organizar validacoes futuras de comportamento esperado, seguranca, rastreabilidade, explicabilidade e limites do sistema.

### Pode existir

- casos de teste conceituais;
- cenarios de seguranca;
- testes de consistencia documental;
- testes de rastreabilidade;
- testes de limites de recomendacao;
- testes de conflitos de evidencia;
- testes de separacao entre camadas;
- fixtures anonimas ou sinteticas quando necessario no futuro.

### Nao pode existir

- dados reais identificaveis de pacientes;
- conhecimento cientifico sem fonte;
- regras clinicas novas;
- implementacao de motores;
- interface como fonte de verdade;
- recomendacoes clinicas finais.

### Dependencias permitidas

- Pode validar contratos de todas as pastas.
- Pode referenciar `docs/` como criterio de aceitacao.
- Pode testar se `application/`, `interfaces/`, `reasoning/`, `safety/`, `knowledge/` e `evidence/` respeitam fronteiras.

### Dependencias proibidas

- Nao pode criar comportamento clinico que nao exista no dominio ou na documentacao.
- Nao pode substituir governanca cientifica.
- Nao pode conter dados clinicos reais sem politica especifica.
- Nao pode acoplar testes a detalhes de interface como regra clinica.

## 14. Matriz de Dependencias Permitidas

```text
docs        -> pode referenciar todos conceitualmente
domain      -> docs
knowledge   -> docs, domain, evidence
reasoning   -> docs, domain, knowledge, safety, evidence
safety      -> docs, domain, knowledge, evidence
evidence    -> docs
application -> domain, reasoning, safety, knowledge, evidence, audit
interfaces  -> application
audit       -> docs, domain, application, reasoning, safety, evidence
tests       -> todas as pastas como alvo de validacao
```

## 15. Dependencias Proibidas Criticas

- `domain/` nao depende de `application/` ou `interfaces/`.
- `knowledge/` nao depende de `application/` ou `interfaces/`.
- `evidence/` nao depende de `application/` ou `interfaces/`.
- `safety/` nao depende de `interfaces/`.
- `interfaces/` nao contem regra clinica.
- `application/` nao contem evidencia cientifica embutida.
- `reasoning/` nao prescreve.
- `audit/` nao decide.
- `tests/` nao cria regra clinica nova.

## 16. Criterio de Aceite Arquitetural

Uma alteracao futura no repositorio so deve ser aceita se respeitar estas perguntas:

- A logica clinica esta separada da interface?
- A evidencia cientifica esta separada da aplicacao?
- A seguranca clinica possui fonte e fronteira propria?
- O dominio nao depende de tecnologia ou UI?
- A interface apenas apresenta e coleta, sem decidir?
- A aplicacao coordena, mas nao inventa conhecimento clinico?
- A auditoria consegue reconstruir o caminho da decisao?
- Os testes validam regras existentes, sem criar regras novas?

Se qualquer resposta for negativa, a alteracao viola a estrutura oficial do repositorio.

## 17. Declaracao Final

A estrutura oficial do repositorio PsychRx existe para proteger o projeto contra mistura de responsabilidades. Conhecimento cientifico, raciocinio clinico, seguranca, dominio, aplicacao, interface e auditoria devem permanecer separados, conectados por dependencias explicitas e rastreaveis.

Essa separacao e uma exigencia clinica, nao apenas tecnica. Ela impede que evidencia vire interface, que interface vire decisao, que aplicacao vire prescritor e que logica clinica perca rastreabilidade.

## 18. Adendo - Clinical Experience Layer

ADR relacionada: `docs/adr/0005_CLINICAL_EXPERIENCE_LAYER.md`.

A estrutura oficial do repositorio passa a incluir:

```text
clinical_experience/
adapters/
infrastructure/
clinical_kernel/
reasoning/
safety/
interfaces/desktop_dashboard/
interfaces/tablet_view/
interfaces/mobile_view/
```

### clinical_experience/

Finalidade: transformar o raciocinio do PsychRx em uma experiencia de consulta rapida, silenciosa, responsiva e util.

Pode existir:

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

Nao pode existir:

- prescricao automatica;
- decisao clinica final;
- regra terapeutica primaria;
- evidencia cientifica hardcoded;
- motores clinicos;
- bypass da Safety Layer;
- acesso direto a dados sensiveis sem contrato de aplicacao.

Dependencias permitidas:

- `application/`
- `docs/`

Dependencias proibidas:

- `knowledge/` direto para sugerir estrategia;
- `evidence/` direto para gerar conclusao;
- `reasoning/` direto para contornar aplicacao;
- `safety/` direto para alterar alerta;
- `interfaces/` como fonte de verdade.

### adapters/

Finalidade: guardar adaptadores externos futuros sem regra clinica primaria.

Nao pode conter prescricao, evidencia hardcoded ou decisao assistencial.

### infrastructure/

Finalidade: guardar infraestrutura tecnica futura.

Nao pode conter dominio, conhecimento cientifico, regra clinica ou decisao de conduta.

### clinical_kernel/

Finalidade: guardar o nucleo computacional futuro do raciocinio clinico.

Ainda nao implementa motores, regras terapeuticas ou recomendacoes.

### reasoning/

Finalidade: organizar raciocinio clinico estruturado.

Nao depende de interface e nao prescreve.

### safety/

Finalidade: organizar seguranca clinica.

Seguranca precede estrategias e nao pode ser contornada pela interface.
