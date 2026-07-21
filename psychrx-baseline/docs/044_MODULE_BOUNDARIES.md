# 044 - Module Boundaries

## 1. Objetivo

Este documento define oficialmente os limites entre os módulos do PsychRx.

Seu objetivo é impedir mistura de responsabilidades entre domínio, conhecimento, evidência, raciocínio, segurança, aplicação, interface, auditoria e testes.

Este documento não implementa software, não define código, não cria APIs e não escolhe tecnologia. Ele estabelece fronteiras arquiteturais para orientar futuras implementações.

## 2. Princípio Central

Cada módulo deve possuir responsabilidade própria, dados sob sua guarda conceitual, dependências explícitas e comunicação controlada.

Nenhum módulo deve acessar outro por conveniência se isso violar as camadas oficiais, a rastreabilidade ou a separação entre conhecimento científico, raciocínio clínico e interface.

Regra central:

```text
Módulos colaboram por contratos.
Módulos não invadem responsabilidades.
```

## 3. Módulos Oficiais

Os módulos arquiteturais oficiais são:

- Domain Module;
- Knowledge Module;
- Evidence Module;
- Reasoning Module;
- Safety Module;
- Application Module;
- Interface Module;
- Audit Module;
- Testing Module.

Esses módulos podem ser organizados futuramente em pastas, pacotes, serviços ou componentes, mas seus limites conceituais devem permanecer os mesmos.

## 4. Domain Module

### Responsabilidades

O Domain Module define os conceitos centrais do PsychRx:

- `Patient`;
- `ClinicalSnapshot`;
- `Symptom`;
- `Syndrome`;
- `DiagnosticHypothesis`;
- `TherapeuticObjective`;
- `TherapeuticRestriction`;
- `TherapeuticStrategy`;
- `PsychopharmacologicalAgent`;
- `ClinicalResponse`;
- `MonitoringPlan`;
- `SafetyAlert`;
- `ClinicalExplanation`;
- eventos e invariantes de domínio.

### Dependências Permitidas

- Documentos oficiais;
- linguagem ubíqua;
- contratos conceituais estáveis.

### Dependências Proibidas

- Application Module;
- Interface Module;
- dashboards;
- infraestrutura;
- banco de dados;
- conhecimento científico hardcoded;
- regras executáveis de decisão.

### Interfaces Conceituais

O Domain Module expõe conceitos, invariantes e eventos. Ele não expõe telas, fluxos de aplicação ou persistência.

### Comunicação

Outros módulos podem usar conceitos do domínio, mas o domínio não deve conhecer quem o utiliza.

### Isolamento

O Domain Module deve permanecer independente. Qualquer dependência do domínio para aplicação ou interface viola a arquitetura.

### Propriedade dos Dados

O Domain Module é proprietário conceitual dos significados clínicos centrais, não da persistência física dos dados.

## 5. Knowledge Module

### Responsabilidades

O Knowledge Module organiza conhecimento clínico-científico estruturado:

- ontologias;
- taxonomias;
- relações psicofarmacológicas;
- efeitos adversos;
- interações;
- contraindicações;
- requisitos de monitorização;
- conhecimento reutilizável.

### Dependências Permitidas

- Domain Module;
- Evidence Module;
- documentos de governança científica.

### Dependências Proibidas

- Interface Module;
- Application Module como fonte de regra;
- dashboards;
- casos de uso;
- dados individuais de pacientes;
- lógica executável de decisão.

### Interfaces Conceituais

O Knowledge Module disponibiliza conhecimento estruturado e versionado para Reasoning e Safety.

### Comunicação

Comunica-se com Evidence para lastro científico e com Reasoning/Safety como fonte estruturada de conhecimento.

### Isolamento

Conhecimento não deve conter algoritmo. Deve informar raciocínio, não executá-lo.

### Propriedade dos Dados

É proprietário do conhecimento estruturado derivado de fontes, mas não das fontes em si nem dos dados clínicos individuais.

## 6. Evidence Module

### Responsabilidades

O Evidence Module organiza fontes científicas e rastreabilidade:

- `EvidenceSource`;
- tipo de evidência;
- qualidade da evidência;
- força da recomendação;
- status;
- conflitos;
- data de revisão;
- aplicabilidade clínica;
- versionamento.

### Dependências Permitidas

- Documentos de governança científica.

### Dependências Proibidas

- Interface Module;
- Application Module;
- dashboards;
- decisões individuais;
- regras terapêuticas sem curadoria.

### Interfaces Conceituais

Expõe metadados científicos, status, conflitos e aplicabilidade.

### Comunicação

Sustenta Knowledge, Safety e Reasoning com evidência rastreável.

### Isolamento

Evidence não decide conduta. Evidence sustenta ou limita afirmações.

### Propriedade dos Dados

É proprietário das fontes, metadados científicos, versões e registros de conflito.

## 7. Reasoning Module

### Responsabilidades

O Reasoning Module organiza o raciocínio clínico:

- Clinical Operating Mind;
- Question Engine;
- Diagnostic Reasoning;
- Therapeutic Objective Engine;
- Strategy Generation;
- Strategy Comparison;
- gerenciamento de incerteza;
- raciocínio longitudinal;
- integração entre contexto, conhecimento e evidência.

### Dependências Permitidas

- Domain Module;
- Knowledge Module;
- Evidence Module;
- Safety Module.

### Dependências Proibidas

- Interface Module;
- dashboard;
- banco de dados;
- detalhes de aplicação;
- evidência hardcoded;
- prescrição automática.

### Interfaces Conceituais

Expõe raciocínios, hipóteses, objetivos, comparações e explicações em formato conceitual.

### Comunicação

Recebe contexto do Application Module, consulta Knowledge/Evidence/Safety por contratos e devolve raciocínio explicável.

### Isolamento

Reasoning não deve acessar interface diretamente. Também não deve ultrapassar Safety.

### Propriedade dos Dados

É proprietário do raciocínio produzido, mas não dos dados do paciente, fontes científicas ou apresentação visual.

## 8. Safety Module

### Responsabilidades

O Safety Module organiza segurança clínica:

- contrato de segurança;
- bloqueios absolutos;
- alertas críticos;
- alertas moderados;
- contraindicações;
- interações;
- dados ausentes críticos;
- necessidade de encaminhamento;
- necessidade de monitorização.

### Dependências Permitidas

- Domain Module;
- Knowledge Module;
- Evidence Module.

### Dependências Proibidas

- Interface Module;
- dashboard;
- preferências visuais;
- Application como fonte de regra;
- regras sem fonte.

### Interfaces Conceituais

Expõe alertas, bloqueios, restrições e justificativas de segurança.

### Comunicação

Deve ser consultado antes de Strategy Generation e Strategy Comparison.

### Isolamento

Safety não pode ser ignorado por Reasoning, Application ou Interface.

### Propriedade dos Dados

É proprietário conceitual dos alertas e restrições de segurança, mas deve rastrear fontes em Evidence.

## 9. Application Module

### Responsabilidades

O Application Module orquestra casos de uso futuros.

Ele coordena:

- entrada de dados;
- validação de completude;
- chamada aos módulos corretos;
- sequência de raciocínio;
- registro de auditoria;
- retorno de resultados para interfaces.

### Dependências Permitidas

- Domain Module;
- Knowledge Module;
- Evidence Module;
- Reasoning Module;
- Safety Module;
- Audit Module.

### Dependências Proibidas

- Interface como fonte de regra;
- evidência hardcoded;
- regra clínica primária;
- decisão clínica final;
- prescrição.

### Interfaces Conceituais

Expõe contratos de caso de uso, não lógica clínica primária.

### Comunicação

Recebe solicitações da Interface, coordena módulos internos e devolve saídas rastreáveis.

### Isolamento

Application orquestra. Application não inventa conhecimento, não decide conduta e não sobrescreve Safety.

### Propriedade dos Dados

É proprietário dos fluxos de uso e estados operacionais de coordenação, não do significado clínico dos dados.

## 10. Interface Module

### Responsabilidades

O Interface Module coleta informações e apresenta resultados.

Pode:

- receber dados do usuário;
- exibir Clinical Snapshot;
- exibir SafetyAlert;
- exibir ClinicalExplanation;
- exibir fontes;
- exibir incertezas;
- permitir revisão médica.

### Dependências Permitidas

- Application Module.

### Dependências Proibidas

- Domain Module diretamente para decidir lógica;
- Knowledge Module;
- Evidence Module;
- Reasoning Module;
- Safety Module;
- Audit Module como fonte de decisão;
- qualquer regra clínica.

### Interfaces Conceituais

Interface consome contratos fornecidos pela Application.

### Comunicação

Comunica-se com Application. Não comunica diretamente com motores clínicos.

### Isolamento

Interface não decide lógica clínica, não interpreta evidência e não altera severidade de alertas.

### Propriedade dos Dados

É proprietária apenas da representação visual ou textual da informação, não do significado clínico nem da decisão.

## 11. Audit Module

### Responsabilidades

O Audit Module registra rastreabilidade:

- Clinical Snapshot usado;
- dados de entrada relevantes;
- hipóteses;
- objetivos;
- restrições;
- alertas;
- evidências;
- versões;
- raciocínio;
- explicação;
- saída apresentada;
- contexto de execução.

### Dependências Permitidas

- Domain Module;
- Application Module;
- Reasoning Module;
- Safety Module;
- Evidence Module.

### Dependências Proibidas

- Interface como fonte de verdade;
- dashboard;
- decisão clínica;
- alteração de resultado.

### Interfaces Conceituais

Expõe trilhas de auditoria e reconstrução de eventos.

### Comunicação

Recebe eventos e registros dos demais módulos por meio de contratos definidos.

### Isolamento

Audit registra. Audit não decide.

### Propriedade dos Dados

É proprietário dos registros de auditoria, trilhas de rastreabilidade e versões usadas em cada análise.

## 12. Testing Module

### Responsabilidades

O Testing Module valida se os demais módulos respeitam seus contratos.

Deve cobrir:

- domínio;
- contratos;
- regressão;
- segurança clínica;
- explicabilidade;
- rastreabilidade;
- integração;
- não-regressão.

### Dependências Permitidas

- Todos os módulos como alvo de validação.

### Dependências Proibidas

- criação de regra clínica nova;
- conhecimento sem fonte;
- dados reais identificáveis sem política específica;
- interface como fonte de verdade clínica.

### Interfaces Conceituais

Expõe critérios de validação e cenários simulados.

### Comunicação

Valida contratos, fronteiras e comportamento esperado sem assumir propriedade do domínio.

### Isolamento

Testes não criam comportamento oficial. Testes verificam comportamento documentado.

### Propriedade dos Dados

É proprietário de cenários simulados, fixtures conceituais e critérios de teste.

## 13. Comunicação entre Módulos

A comunicação deve seguir contratos explícitos.

Regras:

- Interface comunica-se com Application;
- Application coordena os demais módulos;
- Reasoning consulta Safety antes de comparar estratégias;
- Safety consulta Knowledge e Evidence;
- Knowledge se apoia em Evidence;
- Evidence não depende de Application ou Interface;
- Audit observa eventos, não governa decisões;
- Domain permanece independente.

Comunicação proibida:

- Interface -> Reasoning direto;
- Interface -> Safety direto;
- Interface -> Evidence direto;
- Reasoning -> Interface;
- Domain -> Application;
- Domain -> Interface;
- Knowledge -> Interface;
- Evidence -> Interface.

## 14. Propriedade dos Dados

Cada dado deve possuir proprietário conceitual.

| Tipo de dado | Proprietário conceitual |
|---|---|
| Significado clínico central | Domain Module |
| Conhecimento estruturado | Knowledge Module |
| Fonte científica e metadados | Evidence Module |
| Raciocínio produzido | Reasoning Module |
| Alertas e bloqueios | Safety Module |
| Fluxo de caso de uso | Application Module |
| Apresentação | Interface Module |
| Trilha de auditoria | Audit Module |
| Cenários de validação | Testing Module |

Nenhum módulo deve modificar dado cujo significado pertence a outro módulo.

## 15. Isolamento Arquitetural

O isolamento protege o PsychRx contra acoplamento indevido.

Sinais de violação:

- interface decidindo conduta;
- reasoning acessando dashboard;
- evidence dependendo de application;
- knowledge contendo regra executável;
- motores contendo evidência hardcoded;
- safety sendo ignorado;
- audit alterando resultado;
- testes criando regra clínica;
- domain conhecendo infraestrutura.

Qualquer violação deve bloquear Pull Request ou missão.

## 16. Critério de Aceite Futuro

Uma mudança futura respeita os limites de módulo se:

- altera apenas o módulo responsável;
- usa dependências permitidas;
- não cria comunicação proibida;
- preserva propriedade dos dados;
- mantém rastreabilidade;
- preserva explicabilidade;
- não mistura conhecimento com algoritmo;
- não coloca lógica clínica na interface;
- não altera estrutura sem ADR quando aplicável;
- possui testes proporcionais ao risco.

## 17. Declaração Final

Os limites de módulo existem para proteger a arquitetura clínica do PsychRx.

Cada módulo deve saber o que possui, o que pode consultar, o que não pode decidir e como deve se comunicar. Quando essas fronteiras são respeitadas, o sistema permanece explicável, rastreável, testável e clinicamente seguro.

No PsychRx, modularidade não é organização estética. É uma condição de segurança clínica e governança arquitetural.
