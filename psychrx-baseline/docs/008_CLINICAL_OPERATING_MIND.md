# 008 - Clinical Operating Mind

## 1. Objetivo

O Clinical Operating Mind define oficialmente a arquitetura conceitual do raciocinio clinico do PsychRx.

Ele representa o "cerebro clinico" do sistema: a forma como o PsychRx organiza dados, formula perguntas, estrutura hipoteses, identifica objetivos, reconhece restricoes, prioriza seguranca, avalia evidencias, compara estrategias, explica conclusoes e acompanha o paciente ao longo do tempo.

Este documento nao descreve implementacao, codigo, algoritmos, APIs, banco de dados ou classes. Ele descreve como o sistema organiza o julgamento clinico para apoiar o medico sem substitui-lo.

## 2. Missao

A missao do Clinical Operating Mind e transformar informacoes clinicas dispersas em raciocinio organizado, seguro, explicavel e rastreavel.

O Clinical Operating Mind deve:

- colocar o paciente no centro;
- organizar o estado clinico atual;
- formular perguntas clinicas relevantes;
- sustentar hipoteses diagnosticas sem transforma-las em certezas indevidas;
- definir objetivos terapeuticos antes de estrategias;
- identificar restricoes e riscos;
- aplicar seguranca clinica antes de qualquer comparacao;
- integrar conhecimento cientifico, evidencia e contexto individual;
- comparar estrategias sem prescrever;
- explicar o raciocinio;
- acompanhar resposta, estabilidade, recaida, recorrencia e remissao ao longo do tempo.

## 3. Responsabilidades

O Clinical Operating Mind e responsavel por organizar o julgamento clinico do PsychRx.

Suas responsabilidades sao:

- distinguir dados informados, inferencias, hipoteses, evidencias e decisoes;
- identificar dados ausentes clinicamente relevantes;
- reconhecer incertezas;
- preservar a diferenca entre estrategia terapeutica e prescricao;
- impedir estrategia sem objetivo terapeutico;
- impedir comparacao estrategica sem avaliacao de seguranca;
- impedir recomendacao sem explicacao;
- impedir informacao clinica sem fonte quando depender de conhecimento cientifico;
- conectar cada saida a evidencias, riscos e contexto;
- sustentar rastreabilidade;
- manter o medico como decisor final.

## 4. Principios Operacionais

O Clinical Operating Mind deve operar segundo os seguintes principios:

- paciente antes da estrategia;
- raciocinio antes da conclusao;
- seguranca antes da eficacia;
- objetivo antes da estrategia;
- evidencia antes da afirmacao;
- explicacao antes da recomendacao;
- rastreabilidade antes de maturidade;
- incerteza declarada antes de certeza falsa;
- monitorizacao antes de estabilidade sustentada;
- medico sempre como decisor final.

Comparar nao e prescrever. Sugerir nao e decidir. Explicar nao e substituir julgamento medico.

## 5. Fluxo Geral de Funcionamento

O Clinical Operating Mind organiza o raciocinio em uma sequencia clinica.

Primeiro, o sistema constroi ou atualiza o `Clinical Snapshot`, representando o estado clinico atual do paciente.

Depois, o `Question Engine` organiza as perguntas clinicas que precisam ser respondidas: o que esta acontecendo, o que falta saber, qual risco existe, qual objetivo e prioritario e quais caminhos sao seguros o suficiente para comparacao.

Em seguida, o `Diagnostic Reasoning` estrutura hipoteses diagnosticas e diferenciais com nivel de confianca, criterios favoraveis, criterios contrarios e incertezas.

O `Therapeutic Objective Engine` define os objetivos terapeuticos que orientam qualquer discussao estrategica.

O `Constraint Engine` identifica restricoes, contraindicações, interacoes, comorbidades, preferencias e fatores individuais que limitam ou modificam estrategias.

O `Safety First Engine` avalia riscos clinicos obrigatorios antes de permitir qualquer comparacao terapeutica.

Somente depois disso, `Strategy Generation` pode organizar possibilidades conceituais de estrategia, e `Strategy Comparison` pode comparar alternativas em termos de beneficios, riscos, restricoes, evidencias, monitorizacao e estabilidade.

O `Evidence Evaluation` avalia qualidade, aplicabilidade, conflitos e forca das evidencias.

O `Clinical Explanation` transforma o raciocinio em justificativa compreensivel, rastreavel e revisavel.

O `Monitoring Engine` define o que precisa ser acompanhado, e o `Longitudinal Follow-up` compara a trajetoria do paciente ao longo do tempo.

## 6. Componentes Internos

### Clinical Snapshot

Representa o estado clinico atual do paciente em um momento especifico.

Inclui sintomas, funcionalidade, qualidade de vida, medicamentos em uso, historico relevante, riscos, dados ausentes, hipoteses, objetivos ativos e alertas de seguranca.

O Clinical Snapshot e o ponto de partida do raciocinio.

### Question Engine

Organiza as perguntas clinicas que orientam o raciocinio.

Ele ajuda a explicitar:

- o que precisa ser esclarecido;
- quais dados faltam;
- quais riscos precisam ser avaliados;
- quais hipoteses sao plausiveis;
- quais objetivos sao prioritarios;
- quais decisoes ainda nao podem ser tomadas.

### Diagnostic Reasoning

Organiza hipoteses diagnosticas e sindromicas.

Deve diferenciar:

- sintomas;
- sindromes;
- hipoteses diagnosticas;
- diagnosticos diferenciais;
- nivel de confianca;
- incertezas.

Diagnostic Reasoning nao fecha diagnostico automaticamente.

### Therapeutic Objective Engine

Define objetivos terapeuticos antes de qualquer estrategia.

Pode organizar objetivos como:

- reducao de sintomas;
- reducao de risco;
- melhora funcional;
- melhora de qualidade de vida;
- tolerabilidade;
- adesao;
- prevencao de recaida;
- estabilidade sustentada.

Nenhuma estrategia deve existir sem objetivo terapeutico.

### Constraint Engine

Identifica restricoes clinicas, farmacologicas, contextuais e individuais.

Inclui:

- contraindicações;
- interacoes;
- comorbidades;
- alergias;
- reacoes adversas previas;
- preferencias do paciente;
- fatores individuais;
- dados ausentes criticos.

### Safety First Engine

Aplica o contrato de seguranca clinica antes de qualquer estrategia.

Deve considerar risco de suicidio, agressividade, delirium, intoxicacao, abstinencia, gestacao, lactacao, insuficiencia renal, insuficiencia hepatica, doenca cardiovascular, QT prolongado, epilepsia, interacoes, alergias e reacoes adversas graves previas.

Se a seguranca nao estiver avaliada, a comparacao estrategica deve ser limitada ou bloqueada.

### Strategy Generation

Organiza possibilidades conceituais de estrategia terapeutica.

Nao prescreve, nao escolhe conduta e nao define tratamento final.

Sua funcao e formular caminhos possiveis para comparacao, sempre subordinados a objetivos, restricoes, seguranca e evidencia.

### Strategy Comparison

Compara estrategias possiveis.

Deve considerar:

- objetivo terapeutico;
- beneficio esperado;
- risco;
- restricoes;
- qualidade da evidencia;
- aplicabilidade ao paciente;
- tolerabilidade;
- monitorizacao;
- impacto sobre estabilidade.

Strategy Comparison nao substitui decisao medica.

### Evidence Evaluation

Avalia a evidencia que sustenta afirmacoes, alertas e comparacoes.

Deve considerar:

- fonte;
- ano;
- tipo de evidencia;
- qualidade;
- forca da recomendacao;
- conflitos conhecidos;
- aplicabilidade clinica;
- status;
- data de revisao.

Nenhuma regra terapeutica deve entrar sem evidencia rastreavel.

### Clinical Explanation

Gera a explicacao clinica da saida.

Deve conectar:

- dados do paciente;
- Clinical Snapshot;
- hipoteses;
- objetivos;
- restricoes;
- riscos;
- evidencias;
- incertezas;
- limites;
- papel do medico.

Clinical Explanation e parte obrigatoria do raciocinio, nao texto decorativo.

### Monitoring Engine

Define o que deve ser acompanhado para avaliar seguranca, resposta e estabilidade.

Pode envolver sintomas, funcionalidade, qualidade de vida, efeitos adversos, adesao, exames, sinais vitais, risco, resposta clinica e sinais de recaida ou recorrencia.

### Longitudinal Follow-up

Organiza a trajetoria do paciente ao longo do tempo.

Compara snapshots, respostas, eventos adversos, alteracoes funcionais, estabilidade parcial, estabilidade sustentada, remissao, recaida e recorrencia.

Impede que o sistema confunda melhora pontual com estabilidade clinica.

## 7. Relação entre os componentes

Os componentes do Clinical Operating Mind se relacionam como uma cadeia de raciocinio clinico.

O `Clinical Snapshot` fornece o estado atual. O `Question Engine` transforma esse estado em perguntas. O `Diagnostic Reasoning` organiza hipoteses. O `Therapeutic Objective Engine` define direcao. O `Constraint Engine` identifica limites. O `Safety First Engine` decide se ha seguranca minima para seguir.

Depois disso, `Strategy Generation` organiza caminhos possiveis, `Strategy Comparison` compara alternativas e `Evidence Evaluation` qualifica a base cientifica. O `Clinical Explanation` torna o caminho compreensivel e rastreavel. O `Monitoring Engine` define acompanhamento. O `Longitudinal Follow-up` reavalia tudo conforme a trajetoria muda.

Nenhum componente deve agir isoladamente como decisor clinico final.

## 8. Gerenciamento de Incerteza

O Clinical Operating Mind deve tratar incerteza como parte normal do raciocinio clinico.

Incertezas podem vir de:

- dados ausentes;
- informacoes contraditorias;
- sintomas inespecificos;
- baixa confianca diagnostica;
- evidencia limitada;
- conflito entre fontes;
- contexto clinico incompleto;
- resposta ambigua;
- adesao incerta;
- causalidade incerta de efeito adverso.

O sistema deve:

- nomear a incerteza;
- reduzir a forca da conclusao;
- evitar recomendacao forte;
- sugerir necessidade de dados adicionais;
- manter alternativas abertas;
- reforcar monitorizacao;
- preservar julgamento medico.

Ocultar incerteza e falha clinica.

## 9. Processo Longitudinal

O PsychRx deve raciocinar no tempo.

O processo longitudinal compara estados sucessivos do paciente para avaliar:

- resposta clinica;
- tolerabilidade;
- funcionalidade;
- qualidade de vida;
- adesao;
- eventos adversos;
- risco;
- remissao;
- recaida;
- recorrencia;
- estabilidade parcial;
- estabilidade sustentada.

Cada novo Clinical Snapshot deve ser interpretado em relacao aos anteriores.

O Clinical Operating Mind deve reconhecer que psicofarmacologia nao se decide apenas pelo estado atual, mas pela trajetoria.

## 10. Relação com os demais documentos

Este documento se relaciona com:

- documentos fundadores 000 a 006: preservam os principios clinicos e arquiteturais obrigatorios;
- `007_MOTOR_DE_ESTABILIZACAO.md`: define estabilidade como objetivo final do raciocinio;
- `009_CLINICAL_SNAPSHOT.md`: define o ponto de partida dinamico do raciocinio;
- `010_BIBLIOTECA_CIENTIFICA.md`: organiza as fontes cientificas;
- `011_KNOWLEDGE_GRAPH.md`: define relacoes entre conceitos clinicos;
- `012_DECISION_GRAPH.md`: define caminhos de decisao;
- `013_CONSTRAINT_GRAPH.md`: define restricoes clinicas;
- `014_EVIDENCE_GRAPH.md`: define sustentacao cientifica das decisoes;
- `CLINICAL_SAFETY_CONTRACT.md`: define barreiras obrigatorias de seguranca;
- `EVIDENCE_TRACEABILITY_POLICY.md`: define rastreabilidade cientifica obrigatoria;
- `NAMING_CONVENTIONS.md`: padroniza termos usados neste documento.

## 11. Limitações

O Clinical Operating Mind possui limites claros:

- nao implementa software;
- nao define APIs;
- nao define banco de dados;
- nao usa pseudocodigo;
- nao define classes;
- nao prescreve;
- nao substitui avaliacao medica;
- nao fecha diagnostico automaticamente;
- nao elimina incerteza;
- nao transforma evidencia populacional em decisao individual automatica;
- nao decide conduta final.

Seu papel e organizar o raciocinio clinico de forma segura, explicavel e rastreavel.

## 12. Declaração Final

O Clinical Operating Mind e a especificacao oficial do funcionamento conceitual do cerebro do PsychRx.

Ele organiza o julgamento clinico em torno do paciente, estrutura perguntas, hipoteses, objetivos, restricoes, seguranca, evidencia, estrategia, explicacao, monitorizacao e acompanhamento longitudinal.

No PsychRx, pensar clinicamente significa raciocinar antes de sugerir, proteger antes de comparar, explicar antes de concluir e manter o medico como decisor final.
