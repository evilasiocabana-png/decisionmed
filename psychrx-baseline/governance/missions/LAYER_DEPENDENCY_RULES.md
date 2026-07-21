# Layer Dependency Rules

## 1. Proposito

Este documento define regras rigidas de dependencia entre camadas do PsychRx.

Ele deve funcionar como contrato arquitetural para revisao de Pull Requests. Qualquer alteracao futura que viole estas regras deve ser considerada arquiteturalmente incorreta, mesmo que funcione tecnicamente.

O objetivo e impedir que dominio, conhecimento cientifico, evidencia, raciocinio clinico, seguranca, aplicacao, interface e auditoria sejam misturados.

## 2. Camadas Oficiais

As camadas oficiais do PsychRx sao:

1. Domain Layer
2. Knowledge Layer
3. Evidence Layer
4. Reasoning Layer
5. Safety Layer
6. Application Layer
7. Interface Layer
8. Audit Layer

Cada camada possui responsabilidade propria e dependencias restritas.

## 3. Regra Geral de Dependencia

Dependencias devem apontar para camadas mais fundamentais, nunca para camadas de apresentacao ou orquestracao quando isso comprometer o dominio.

Regra central:

```text
Interface -> Application -> Reasoning/Safety -> Domain/Knowledge/Evidence
Audit observa e registra, mas nao decide.
Domain permanece independente.
```

Nenhuma camada deve atravessar outra para buscar conveniencia.

## 4. Domain Layer

### Pode depender de

- Nenhuma camada operacional.
- Conceitos documentados em `docs/`, apenas como referencia conceitual.

### Nao pode depender de

- Application Layer;
- Interface Layer;
- Reasoning Layer;
- Safety Layer;
- Knowledge Layer como fonte embutida;
- Evidence Layer como biblioteca de fontes;
- Audit Layer.

### Regra de independencia do dominio

O dominio deve ser independente de aplicacao, interface, banco, tecnologia, dashboard, fluxos de usuario e orquestracao.

O Domain Layer define os conceitos centrais do PsychRx, mas nao deve conhecer como eles serao apresentados, persistidos, auditados ou executados.

### Proibicoes explicitas

- `domain` depender de `application`;
- `domain` depender de `interface`;
- entidades de dominio conhecerem dashboard;
- entidades de dominio conhecerem casos de uso;
- entidades de dominio conterem evidencia cientifica hardcoded;
- entidades de dominio decidirem conduta clinica final.

## 5. Knowledge Layer

### Pode depender de

- Domain Layer, para usar linguagem e conceitos do dominio;
- Evidence Layer, para lastro cientifico e fontes;
- `docs/`, para governanca conceitual.

### Nao pode depender de

- Application Layer;
- Interface Layer;
- Audit Layer como fonte de verdade;
- dashboards;
- casos de uso;
- componentes de apresentacao.

### Regra de separacao entre conhecimento e algoritmo

Knowledge Layer organiza conhecimento clinico-cientifico estruturado, mas nao executa decisoes.

Conhecimento nao e algoritmo. Conhecimento informa raciocinio, seguranca e explicabilidade, mas nao deve conter regra executavel, fluxo de decisao ou prescricao automatica.

### Proibicoes explicitas

- `knowledge` conter regra executavel;
- `knowledge` acessar interface;
- `knowledge` decidir conduta clinica;
- `knowledge` conter logica de caso de uso;
- `knowledge` misturar fonte cientifica com comportamento operacional.

## 6. Evidence Layer

### Pode depender de

- `docs/`, para politicas de governanca cientifica.

### Nao pode depender de

- Domain Layer como requisito operacional;
- Application Layer;
- Interface Layer;
- Reasoning Layer;
- Safety Layer;
- Audit Layer como fonte primaria;
- dashboards.

### Responsabilidade

Evidence Layer organiza fontes, hierarquia de evidencias, qualidade, conflitos, versionamento e rastreabilidade cientifica.

Ela sustenta Knowledge, Safety e Reasoning, mas nao deve ser alterada por necessidades de interface ou fluxo de aplicacao.

### Proibicoes explicitas

- evidencia depender de UI;
- evidencia depender de dashboard;
- evidencia ser moldada por caso de uso;
- evidencia conter decisao individual;
- evidencia conter prescricao.

## 7. Reasoning Layer

### Pode depender de

- Domain Layer;
- Knowledge Layer;
- Evidence Layer;
- Safety Layer para limites e bloqueios conceituais;
- `docs/`, para principios de raciocinio.

### Nao pode depender de

- Interface Layer;
- dashboard;
- componentes visuais;
- rotas ou telas;
- armazenamento concreto;
- detalhes de apresentacao.

### Responsabilidade

Reasoning Layer organiza raciocinio clinico: hipoteses, objetivos, comparacoes, incertezas, longitudinalidade, explicabilidade e integracao entre contexto, conhecimento e evidencia.

Reasoning nao prescreve. Reasoning estrutura pensamento.

### Proibicoes explicitas

- `reasoning` acessar dashboard diretamente;
- motores clinicos conterem evidencia hardcoded;
- raciocinio depender de layout de tela;
- raciocinio decidir conduta final;
- raciocinio ignorar Safety Layer;
- raciocinio gerar recomendacao sem justificativa rastreavel.

## 8. Safety Layer

### Pode depender de

- Domain Layer;
- Knowledge Layer;
- Evidence Layer;
- `docs/`, para principios de seguranca clinica.

### Nao pode depender de

- Interface Layer;
- dashboard;
- Application Layer como fonte de regra clinica;
- preferencias de apresentacao;
- Audit Layer para decidir risco.

### Responsabilidade

Safety Layer organiza restricoes, riscos, contraindicações, interacoes, alertas, bloqueios conceituais e criterios de cautela.

Seguranca clinica deve atuar antes de comparacoes estrategicas.

### Proibicoes explicitas

- Safety depender da interface;
- Safety ajustar regra por conveniencia visual;
- Safety conter evidencia sem fonte;
- Safety ser bypassada por Application;
- Safety gerar prescricao automatica.

## 9. Application Layer

### Pode depender de

- Domain Layer;
- Knowledge Layer;
- Evidence Layer;
- Reasoning Layer;
- Safety Layer;
- Audit Layer para registrar eventos;
- `docs/`, para contratos arquiteturais.

### Nao pode depender de

- Interface Layer como fonte de regra;
- dashboard como fonte de verdade;
- componentes visuais para decidir fluxo clinico;
- evidencia hardcoded.

### Responsabilidade

Application Layer orquestra casos de uso futuros. Ela coordena camadas, mas nao cria conhecimento cientifico, nao cria regra clinica primaria e nao decide conduta final.

### Proibicoes explicitas

- Application conter evidencia hardcoded;
- Application sobrescrever Safety;
- Application criar regra clinica sem Domain/Knowledge/Evidence;
- Application tratar Interface como fonte de decisao;
- Application prescrever.

## 10. Interface Layer

### Pode depender de

- Application Layer;
- contratos de saida definidos pela aplicacao;
- `docs/`, para linguagem e limites de apresentacao.

### Nao pode depender de

- Domain Layer diretamente para decidir comportamento clinico;
- Knowledge Layer diretamente;
- Evidence Layer diretamente;
- Reasoning Layer diretamente;
- Safety Layer diretamente;
- Audit Layer como mecanismo de decisao.

### Regra de isolamento da interface

Interface coleta informacoes e apresenta resultados. Interface nao decide conduta clinica, nao interpreta evidencia, nao executa raciocinio clinico e nao altera significado de alertas para conveniencia visual.

### Proibicoes explicitas

- interface decidir conduta clinica;
- interface gerar recomendacao;
- interface acessar evidencia para montar conclusao;
- interface acessar knowledge para sugerir estrategia;
- interface ocultar alerta de seguranca;
- interface transformar cautela em aprovacao;
- interface modificar forca da recomendacao.

## 11. Audit Layer

### Pode depender de

- Domain Layer para identidade conceitual de eventos;
- Application Layer para eventos orquestrados;
- Reasoning Layer para registrar raciocinio;
- Safety Layer para registrar alertas;
- Evidence Layer para registrar versoes de fonte;
- `docs/`, para politicas de rastreabilidade.

### Nao pode depender de

- Interface Layer como fonte de verdade;
- dashboard para definir evento;
- preferencias visuais;
- dados sem necessidade de auditoria.

### Regra de rastreabilidade

Toda decisao, alerta, comparacao ou justificativa clinicamente relevante deve ser reconstruivel.

A rastreabilidade deve registrar:

- Clinical Snapshot usado;
- dados de entrada relevantes;
- hipoteses consideradas;
- objetivos terapeuticos;
- restricoes e alertas;
- evidencias e versoes;
- raciocinio ou comparacao apresentada;
- incertezas;
- saida exibida;
- ator ou contexto de execucao.

Audit registra. Audit nao decide.

### Proibicoes explicitas

- Audit decidir conduta;
- Audit substituir Evidence;
- Audit alterar resultado clinico;
- Audit depender de Interface para definir verdade;
- Audit ocultar versoes usadas.

## 12. Matriz de Dependencias Permitidas

```text
Domain      -> nenhuma camada operacional
Knowledge   -> Domain, Evidence
Evidence    -> nenhuma camada operacional
Reasoning   -> Domain, Knowledge, Evidence, Safety
Safety      -> Domain, Knowledge, Evidence
Application -> Domain, Knowledge, Evidence, Reasoning, Safety, Audit
Interface   -> Application
Audit       -> Domain, Application, Reasoning, Safety, Evidence
```

## 13. Dependencias Proibidas Globais

- Domain -> Application
- Domain -> Interface
- Domain -> Dashboard
- Knowledge -> Interface
- Knowledge -> Application
- Knowledge -> regra executavel
- Evidence -> Interface
- Evidence -> Application
- Reasoning -> Interface
- Reasoning -> Dashboard
- Safety -> Interface
- Interface -> Knowledge
- Interface -> Evidence
- Interface -> Reasoning
- Interface -> Safety
- Interface -> decisao clinica
- Application -> evidencia hardcoded
- Clinical engines -> evidencia hardcoded
- Audit -> decisao clinica

## 14. Regra de Separacao entre Conhecimento e Algoritmo

Conhecimento cientifico deve estar em Knowledge e Evidence.

Raciocinio deve estar em Reasoning.

Seguranca deve estar em Safety.

Orquestracao deve estar em Application.

Apresentacao deve estar em Interface.

Nenhum motor clinico pode conter evidencia hardcoded. Motores podem consultar conhecimento e evidencia por contratos apropriados, mas nao devem carregar conteudo cientifico fixo como parte de sua logica interna.

## 15. Regra de Isolamento da Interface

A Interface Layer nao pode tomar decisoes clinicas.

Ela pode:

- coletar dados;
- apresentar alertas;
- exibir justificativas;
- mostrar fontes;
- indicar incertezas;
- permitir revisao medica.

Ela nao pode:

- decidir conduta;
- alterar conclusao;
- reduzir severidade de alerta;
- criar recomendacao;
- escolher estrategia;
- interpretar evidencia diretamente;
- ocultar informacao clinicamente relevante.

## 16. Regra de Rastreabilidade

Toda saida clinica relevante deve ser rastreavel ate:

- dados do paciente;
- Clinical Snapshot;
- hipoteses;
- objetivos;
- restricoes;
- evidencias;
- versoes;
- raciocinio;
- alertas;
- decisao ou revisao medica.

Se uma saida nao puder ser rastreada, ela nao deve ser aceita.

## 17. Checklist para Pull Requests

Todo Pull Request deve responder:

- Domain continua independente?
- Domain nao depende de Application?
- Domain nao depende de Interface?
- Knowledge esta livre de regra executavel?
- Evidence esta livre de decisao individual?
- Reasoning nao acessa dashboard?
- Motores clinicos nao contem evidencia hardcoded?
- Safety nao depende da interface?
- Application apenas orquestra?
- Interface nao decide conduta clinica?
- Audit registra sem decidir?
- Toda saida clinica relevante e rastreavel?

Se qualquer resposta for negativa, o Pull Request deve ser rejeitado ou reestruturado.

## 18. Declaracao Final

As regras de dependencia entre camadas existem para proteger a integridade clinica e arquitetural do PsychRx.

O dominio deve permanecer independente. O conhecimento deve permanecer separado do algoritmo. A interface deve permanecer isolada da decisao clinica. A evidencia deve ser rastreavel. A auditoria deve reconstruir o caminho da decisao. Qualquer violacao dessas regras enfraquece a seguranca, a explicabilidade e a confiabilidade do sistema.

## 19. Adendo - Clinical Experience Layer

ADR relacionada: `docs/adr/0005_CLINICAL_EXPERIENCE_LAYER.md`.

A Clinical Experience Layer passa a ser uma camada oficial do PsychRx.

```text
Interface -> Clinical Experience -> Application -> Reasoning/Safety -> Domain/Knowledge/Evidence
Audit observa e registra, mas nao decide.
Domain permanece independente.
```

### Responsabilidade

Transformar o raciocinio do PsychRx em uma experiencia rapida, silenciosa e util durante a consulta.

Ela organiza a consulta. Ela nao decide conduta.

### Pode depender de

- Application Layer;
- contratos de saida definidos pela aplicacao;
- `docs/`, para linguagem e limites de experiencia clinica.

### Nao pode depender de

- Domain Layer diretamente para decidir comportamento clinico;
- Knowledge Layer diretamente;
- Evidence Layer diretamente;
- Reasoning Layer diretamente;
- Safety Layer diretamente;
- Interface Layer como fonte de regra clinica.

### Componentes oficiais

- Consultation Room;
- Clinical Card Stack;
- Guided Anamnesis;
- Live Question Panel;
- Symptom Capture;
- Strategy Panel;
- Risk Panel;
- Monitoring Timeline;
- Evidence Summary;
- Patient Friendly Mode.

### Proibicoes explicitas

- Clinical Experience decidir conduta;
- Clinical Experience prescrever;
- Guided Anamnesis virar diagnostico automatico;
- Live Question Panel criar interrogatorio excessivo sem relevancia;
- Strategy Panel escolher estrategia pelo medico;
- Risk Panel ser ocultado por conveniencia visual;
- Patient Friendly Mode orientar automedicacao;
- Clinical Experience acessar evidencia diretamente para gerar conclusao.

### Matriz atualizada

```text
Clinical Experience -> Application
Interface           -> Clinical Experience, Application
```

Esse adendo expande as regras anteriores sem revogar a independencia do dominio, a separacao entre conhecimento e algoritmo, a prioridade da seguranca e a rastreabilidade obrigatoria.
