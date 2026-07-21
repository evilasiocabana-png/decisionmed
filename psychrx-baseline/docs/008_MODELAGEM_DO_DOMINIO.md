# 008 - Modelagem do Dominio

## 1. Visao Geral do Dominio

O dominio do PsychRx e organizado em torno do paciente, do raciocinio clinico e da seguranca psicofarmacologica. O sistema nao existe para prescrever, mas para estruturar informacoes, identificar riscos, comparar possibilidades terapeuticas e explicar o raciocinio ao medico.

A modelagem do dominio deve preservar quatro principios centrais:

- paciente no centro;
- seguranca clinica antes de qualquer estrategia;
- conhecimento cientifico separado das decisoes algoritmicas;
- medico sempre como decisor final.

Em termos de Domain-Driven Design, o PsychRx deve ser compreendido como um conjunto de contextos delimitados que colaboram entre si. Cada contexto possui linguagem, responsabilidades e objetos proprios. A comunicacao entre contextos deve ocorrer por contratos conceituais claros, eventos de dominio e referencias explicitas, evitando que regras clinicas fiquem espalhadas ou duplicadas.

O nucleo do dominio e formado por:

- registro estruturado do paciente;
- avaliacao clinica;
- hipoteses diagnosticas;
- objetivos terapeuticos;
- estrategias terapeuticas;
- psicofarmacos;
- evidencias cientificas;
- seguranca clinica;
- monitorizacao;
- explicabilidade;
- auditoria e rastreabilidade.

## 2. Bounded Contexts

### Paciente

Responsavel pela identidade clinica longitudinal do paciente dentro do sistema. Centraliza dados demograficos minimos, condicoes clinicas relevantes, historico terapeutico, fatores de risco e estado atual.

Justificativa: o paciente e a unidade central do dominio. Todos os demais contextos orbitam em torno dele, mas nao devem possuir diretamente toda a sua estrutura interna.

### Avaliacao Clinica

Responsavel por organizar observacoes clinicas, dados de anamnese, problemas ativos, escalas, exames, comorbidades e estado atual do caso.

Justificativa: avaliacao clinica e diferente de paciente. O paciente e longitudinal; a avaliacao e uma leitura contextual em determinado momento.

### Sintomas

Responsavel por registrar sintomas, intensidade, duracao, evolucao, impacto funcional e relacao temporal com tratamentos ou eventos clinicos.

Justificativa: sintomas possuem dinamica propria, podem mudar rapidamente e alimentam hipoteses, objetivos e monitorizacao.

### Hipoteses Diagnosticas

Responsavel por representar hipoteses diagnosticas, diferenciais, nivel de confianca, criterios de suporte, criterios contrarios e incertezas.

Justificativa: o sistema apoia raciocinio antes de estrategia. Hipoteses devem ser explicitadas antes de qualquer comparacao terapeutica.

### Objetivos Terapeuticos

Responsavel por definir o que se pretende acompanhar ou melhorar, como remissao sintomatica, reducao de risco, tolerabilidade, funcionalidade, adesao ou estabilizacao.

Justificativa: nenhuma estrategia deve existir sem objetivo terapeutico explicito.

### Estrategias Terapeuticas

Responsavel por comparar caminhos terapeuticos possiveis em nivel conceitual, sem transformar a comparacao em prescricao automatica.

Justificativa: estrategia nao e prescricao. O contexto deve sustentar comparacao argumentada, riscos, vantagens, limitacoes e justificativas.

### Psicofarmacos

Responsavel por representar medicamentos, classes, mecanismos, perfis farmacologicos, riscos, interacoes, efeitos adversos, contraindicações e requisitos de monitorizacao.

Justificativa: psicofarmacos possuem modelo proprio e devem ser separados da decisao clinica individual.

### Evidencias Cientificas

Responsavel por fontes, diretrizes, estudos, nivel de evidencia, validade, data de revisao e versionamento cientifico.

Justificativa: nenhuma informacao clinicamente relevante deve existir sem fonte. O conhecimento cientifico deve permanecer separado do codigo e das decisoes operacionais.

### Seguranca Clinica

Responsavel por identificar riscos, alertas, contraindicações, interacoes, dados ausentes criticos e situacoes que bloqueiam ou limitam comparacoes.

Justificativa: seguranca clinica e a primeira camada do PsychRx. Nenhuma estrategia deve ser comparada antes de avaliacao de risco.

### Monitorizacao

Responsavel por acompanhar sintomas, efeitos adversos, exames, sinais vitais, escalas, riscos e objetivos terapeuticos ao longo do tempo.

Justificativa: psicofarmacologia exige acompanhamento longitudinal. Monitorizacao conecta avaliacao, estrategia, risco e resposta.

### Explicabilidade

Responsavel por transformar resultados em justificativas rastreaveis: dados usados, regras acionadas, fontes, limites, incertezas e versoes.

Justificativa: nenhuma recomendacao, alerta ou comparacao deve existir sem justificativa compreensivel.

### Auditoria

Responsavel por registrar eventos, entradas, saidas, versoes, fontes, usuarios, decisoes e trilhas de rastreabilidade.

Justificativa: o sistema deve permitir reconstruir qualquer analise realizada.

## 3. Entidades

### Paciente

Responsabilidade: representar a unidade clinica central.

Atributos principais:

- identificador do paciente;
- dados demograficos minimos;
- condicoes clinicas relevantes;
- historico terapeutico;
- fatores de risco;
- avaliacoes clinicas associadas;
- estado clinico atual.

Ciclo de vida: criado quando o paciente entra no sistema; atualizado ao longo do acompanhamento; arquivado quando nao estiver mais ativo, preservando auditoria.

Relacionamentos: possui avaliacoes clinicas, sintomas, hipoteses, objetivos, estrategias, eventos de monitorizacao e registros de auditoria.

### AvaliacaoClinica

Responsabilidade: representar uma leitura clinica estruturada em um momento especifico.

Atributos principais:

- identificador;
- paciente associado;
- data da avaliacao;
- problemas ativos;
- sintomas observados;
- comorbidades;
- exames relevantes;
- medicamentos em uso;
- dados ausentes;
- autor da avaliacao.

Ciclo de vida: criada em cada avaliacao relevante; pode ser complementada; deve preservar versao dos dados usados.

Relacionamentos: pertence a um paciente; referencia sintomas, hipoteses, riscos, objetivos e analises.

### Sintoma

Responsabilidade: representar manifestacao clinica acompanhavel.

Atributos principais:

- nome;
- intensidade;
- duracao;
- inicio;
- curso temporal;
- impacto funcional;
- contexto de aparecimento;
- escala associada, quando houver.

Ciclo de vida: registrado, atualizado, monitorado e eventualmente resolvido ou inativado.

Relacionamentos: pertence a paciente ou avaliacao; pode sustentar hipoteses, objetivos e monitorizacao.

### HipoteseDiagnostica

Responsabilidade: representar uma possibilidade diagnostica em avaliacao.

Atributos principais:

- descricao;
- criterios favoraveis;
- criterios contrarios;
- nivel de confianca;
- diagnosticos diferenciais;
- incertezas;
- fonte ou criterio usado, quando aplicavel.

Ciclo de vida: criada durante avaliacao; revisada conforme novos dados; confirmada, descartada ou mantida como diferencial.

Relacionamentos: depende de avaliacao clinica; orienta objetivos terapeuticos e estrategias comparativas.

### ObjetivoTerapeutico

Responsabilidade: explicitar o alvo clinico da analise.

Atributos principais:

- descricao;
- prioridade;
- indicador de acompanhamento;
- criterio de sucesso;
- prazo clinico esperado;
- riscos associados;
- justificativa.

Ciclo de vida: criado antes de estrategias; revisado conforme resposta, tolerabilidade e mudanca do quadro.

Relacionamentos: pertence ao paciente ou avaliacao; condiciona estrategias e monitorizacao.

### EstrategiaTerapeutica

Responsabilidade: representar uma possibilidade de abordagem, sem equivaler a prescricao.

Atributos principais:

- objetivo associado;
- descricao conceitual;
- beneficios esperados;
- riscos;
- limitacoes;
- justificativa;
- evidencias associadas;
- status de comparacao;
- alertas de seguranca.

Ciclo de vida: criada para comparacao; pode ser descartada, considerada, selecionada pelo medico ou arquivada.

Relacionamentos: depende de objetivo terapeutico, avaliacao de risco e evidencias; pode envolver psicofarmacos ou classes.

### Psicofarmaco

Responsabilidade: representar um medicamento dentro do modelo oficial do PsychRx.

Atributos principais:

- nome;
- classe;
- mecanismos principais;
- perfil de receptores;
- indicacoes reconhecidas;
- contraindicações;
- interacoes;
- efeitos adversos;
- requisitos de monitorizacao;
- fontes cientificas.

Ciclo de vida: criado no banco de conhecimento; revisado por versao cientifica; nunca alterado como dado isolado sem fonte.

Relacionamentos: pertence ao contexto de psicofarmacos; referencia evidencias, interacoes, riscos e monitorizacao.

### ClasseFarmacologica

Responsabilidade: agrupar psicofarmacos por caracteristicas clinicas e farmacologicas.

Atributos principais:

- nome;
- descricao;
- mecanismos comuns;
- riscos comuns;
- evidencias gerais;
- limitacoes.

Ciclo de vida: mantida no banco de conhecimento e revisada cientificamente.

Relacionamentos: agrega psicofarmacos e referencia evidencias.

### EvidenciaCientifica

Responsabilidade: representar fonte ou unidade de conhecimento cientifico rastreavel.

Atributos principais:

- titulo;
- tipo de fonte;
- autores ou instituicao;
- ano;
- nivel de evidencia;
- resumo do achado;
- validade;
- data de revisao;
- versao;
- conflitos ou limitacoes.

Ciclo de vida: cadastrada, revisada, atualizada, substituida ou depreciada.

Relacionamentos: sustenta psicofarmacos, regras, alertas, estrategias e justificativas.

### RegraClinica

Responsabilidade: representar uma regra declarativa derivada de conhecimento cientifico ou governanca clinica.

Atributos principais:

- descricao;
- condicao de acionamento;
- consequencia;
- nivel de severidade;
- fontes;
- versao;
- status.

Ciclo de vida: criada a partir de evidencia ou decisao de governanca; revisada e versionada.

Relacionamentos: pertence ao banco de conhecimento; acionada por motores clinicos; registrada em auditoria.

### AlertaDeSeguranca

Responsabilidade: representar um risco identificado pelo sistema.

Atributos principais:

- tipo;
- severidade;
- dados que acionaram o alerta;
- justificativa;
- fonte;
- recomendacao de cautela;
- status de revisao.

Ciclo de vida: emitido durante analise; revisado pelo medico; pode ser reconhecido, resolvido ou mantido.

Relacionamentos: depende de paciente, avaliacao, regra clinica, psicofarmaco ou estrategia.

### InteracaoMedicamentosa

Responsabilidade: representar relacao de risco entre substancias, classes ou fatores clinicos.

Atributos principais:

- agentes envolvidos;
- mecanismo;
- severidade;
- efeito esperado;
- evidencia;
- orientacao de cautela;
- requisitos de monitorizacao.

Ciclo de vida: mantida no conhecimento cientifico; acionada quando medicamentos ou fatores relevantes aparecem.

Relacionamentos: referencia psicofarmacos, evidencias e alertas.

### PlanoDeMonitorizacao

Responsabilidade: representar acompanhamento proposto como apoio ao raciocinio, nao como ordem automatica.

Atributos principais:

- objetivo monitorado;
- parametro;
- frequencia conceitual;
- justificativa;
- fonte;
- condicoes de alerta.

Ciclo de vida: criado apos analise de objetivo, risco e estrategia; revisado conforme evolucao.

Relacionamentos: vincula paciente, objetivo, risco, estrategia e evidencias.

### AnaliseClinica

Responsabilidade: consolidar a execucao de raciocinio, seguranca, comparacao e explicabilidade.

Atributos principais:

- paciente;
- avaliacao usada;
- dados de entrada;
- motores acionados;
- resultados;
- alertas;
- justificativas;
- fontes;
- versoes;
- status.

Ciclo de vida: criada a cada solicitacao de analise; torna-se registro historico auditavel.

Relacionamentos: agrega resultados de risco, comparacoes, explicacoes e auditoria.

### Explicacao

Responsabilidade: representar a justificativa estruturada de uma saida do sistema.

Atributos principais:

- conclusao ou alerta explicado;
- dados usados;
- regras acionadas;
- fontes;
- incertezas;
- versoes;
- linguagem para o medico.

Ciclo de vida: gerada junto da analise; preservada para auditoria.

Relacionamentos: pertence a analise clinica; referencia evidencias, regras e dados do paciente.

### RegistroDeAuditoria

Responsabilidade: permitir reconstrucao integral de uma acao ou analise.

Atributos principais:

- evento;
- data e hora;
- usuario ou ator;
- dados de entrada;
- componentes acionados;
- versoes;
- saida gerada;
- referencias cientificas.

Ciclo de vida: criado automaticamente em eventos relevantes; preservado de forma imutavel.

Relacionamentos: referencia paciente, analise, regras, fontes e contexto de execucao.

## 4. Value Objects

### Dose

Representa quantidade medicamentosa de forma estruturada. Deve ser Value Object porque sua identidade nao importa isoladamente; importam valor, unidade, via e contexto.

### Peso

Representa medida corporal. Deve incluir valor, unidade, data e confiabilidade, pois influencia interpretacoes clinicas.

### IMC

Representa indice calculado a partir de peso e altura. Deve ser imutavel em relacao ao momento de calculo.

### Altura

Representa medida corporal necessaria para calculos e avaliacao clinica.

### IntervaloQT

Representa medida eletrocardiografica relevante para risco psicofarmacologico. Deve incluir valor, unidade, metodo e data.

### EscoreClinico

Representa resultado de escala clinica. Deve incluir nome da escala, valor, faixa, data e interpretacao.

### FuncaoRenal

Representa estado renal relevante para risco e farmacocinetica. Pode incluir taxa estimada, categoria, data e fonte do exame.

### FuncaoHepatica

Representa estado hepatico relevante para metabolismo e seguranca. Pode incluir marcadores, categoria, data e interpretacao.

### PressaoArterial

Representa medida vital composta por valores sistolico e diastolico, unidade, posicao e data.

### FrequenciaCardiaca

Representa medida vital relevante para risco, efeitos adversos e monitorizacao.

### NivelDeEvidencia

Representa classificacao da confiabilidade cientifica. Deve ser objeto de valor porque condiciona ranking e explicabilidade.

### SeveridadeDoRisco

Representa grau de risco clinico ou farmacologico. Deve ser consistente em todo o dominio.

### NivelDeConfianca

Representa confianca associada a hipoteses diagnosticas ou inferencias. Evita transformar hipotese em certeza.

### PeriodoClinico

Representa intervalo temporal clinicamente relevante, como inicio, duracao ou janela de observacao.

### Justificativa

Representa argumento estruturado que conecta dados, regra, evidencia e conclusao.

### ReferenciaCientifica

Representa citacao ou fonte especifica usada por uma afirmacao. Deve ser imutavel dentro de uma versao.

## 5. Aggregates

### Aggregate Paciente

Aggregate Root: Paciente.

Inclui:

- dados demograficos minimos;
- fatores de risco;
- historico terapeutico resumido;
- estado clinico atual;
- referencias para avaliacoes e analises.

Responsabilidade: garantir consistencia da identidade clinica longitudinal.

### Aggregate Avaliacao Clinica

Aggregate Root: AvaliacaoClinica.

Inclui:

- sintomas registrados;
- problemas ativos;
- comorbidades registradas;
- dados objetivos;
- lacunas clinicas.

Responsabilidade: preservar a consistencia de uma leitura clinica em determinado momento.

### Aggregate Hipotese Diagnostica

Aggregate Root: HipoteseDiagnostica.

Inclui:

- criterios favoraveis;
- criterios contrarios;
- nivel de confianca;
- diferenciais;
- incertezas.

Responsabilidade: impedir hipoteses sem nivel de confianca e sem base explicita.

### Aggregate Objetivo Terapeutico

Aggregate Root: ObjetivoTerapeutico.

Inclui:

- indicador de acompanhamento;
- criterio de sucesso;
- prioridade;
- justificativa.

Responsabilidade: garantir que estrategias sejam orientadas por objetivos explicitos.

### Aggregate Estrategia Terapeutica

Aggregate Root: EstrategiaTerapeutica.

Inclui:

- objetivo associado;
- comparacoes;
- riscos;
- beneficios;
- limitacoes;
- evidencias;
- justificativas.

Responsabilidade: impedir estrategia sem objetivo, sem analise de risco ou sem justificativa.

### Aggregate Psicofarmaco

Aggregate Root: Psicofarmaco.

Inclui:

- classe;
- perfil farmacologico;
- contraindicações;
- interacoes;
- efeitos adversos;
- fontes.

Responsabilidade: garantir que todo psicofarmaco siga o modelo oficial e tenha fonte cientifica.

### Aggregate Evidencia Cientifica

Aggregate Root: EvidenciaCientifica.

Inclui:

- referencia;
- nivel de evidencia;
- validade;
- versao;
- limitacoes;
- status de revisao.

Responsabilidade: preservar integridade, versionamento e rastreabilidade do conhecimento.

### Aggregate Analise Clinica

Aggregate Root: AnaliseClinica.

Inclui:

- dados de entrada;
- alertas;
- resultados dos motores;
- explicacoes;
- fontes;
- versoes;
- registro de execucao.

Responsabilidade: manter uma analise completa, rastreavel e auditavel.

### Aggregate Auditoria

Aggregate Root: RegistroDeAuditoria.

Inclui:

- evento;
- ator;
- timestamp;
- entrada;
- saida;
- versoes;
- referencias.

Responsabilidade: garantir imutabilidade e reconstrucao historica.

## 6. Servicos de Dominio

### Clinical Reasoning Service

Coordena raciocinio clinico estruturado. Organiza dados do paciente, sintomas, hipoteses, objetivos e limites da analise. Nao prescreve.

### Risk Assessment Service

Avalia riscos clinicos e psicofarmacologicos antes de qualquer estrategia. Pode gerar alertas, bloqueios ou exigencia de dados adicionais.

### Strategy Comparison Service

Compara estrategias terapeuticas em nivel conceitual, considerando objetivo, riscos, beneficios, limitacoes e evidencias. Nao seleciona conduta final pelo medico.

### Drug Interaction Service

Identifica interacoes entre medicamentos, classes, condicoes clinicas e fatores de risco. Deve sempre fornecer mecanismo, severidade e fonte.

### Contraindication Assessment Service

Avalia contraindicações absolutas, relativas ou situacionais com base em dados do paciente e conhecimento cientifico versionado.

### Evidence Ranking Service

Classifica evidencias conforme hierarquia cientifica, validade, atualidade e aplicabilidade ao caso.

### Monitoring Planner

Organiza necessidades de acompanhamento associadas a sintomas, riscos, psicofarmacos, objetivos e estrategias. Nao emite ordem clinica autonoma.

### Explanation Service

Gera explicacoes rastreaveis conectando dados, regras, fontes, motores e conclusoes.

### Traceability Service

Garante que toda saida possua vinculo com entradas, fontes, regras e versoes.

### Clinical Safety Gate Service

Funciona como barreira obrigatoria antes de comparacoes estrategicas. Se houver risco elevado sem resolucao ou dados criticos ausentes, deve impedir saidas estrategicas fortes.

## 7. Repositorios

### Patient Repository

Responsavel por recuperar e persistir aggregates de Paciente, preservando identidade longitudinal e referencias para avaliacoes e analises.

### Clinical Assessment Repository

Responsavel por recuperar avaliacoes clinicas e seus elementos internos.

### Diagnostic Hypothesis Repository

Responsavel por consultar e preservar hipoteses diagnosticas, seus niveis de confianca e historico de revisao.

### Therapeutic Goal Repository

Responsavel por gerenciar objetivos terapeuticos e sua evolucao.

### Therapeutic Strategy Repository

Responsavel por registrar estrategias comparadas, status, justificativas e relacao com objetivos.

### Psychopharmacology Knowledge Repository

Responsavel por consultar psicofarmacos, classes, perfis, interacoes, contraindicações e efeitos adversos.

### Evidence Repository

Responsavel por recuperar evidencias cientificas, fontes, versoes, niveis de evidencia e status de revisao.

### Clinical Rule Repository

Responsavel por recuperar regras clinicas declarativas e suas versoes.

### Clinical Analysis Repository

Responsavel por preservar analises completas, incluindo motores acionados, resultados, explicacoes, fontes e versoes.

### Audit Repository

Responsavel por registrar e recuperar eventos auditaveis de forma imutavel.

## 8. Eventos de Dominio

### PacienteAtualizado

Ocorre quando dados clinicamente relevantes do paciente sao alterados.

### AvaliacaoClinicaRegistrada

Ocorre quando uma nova avaliacao clinica e criada.

### SintomaRegistrado

Ocorre quando um sintoma novo e associado ao paciente ou avaliacao.

### SintomaAtualizado

Ocorre quando intensidade, duracao, impacto ou curso temporal de um sintoma muda.

### HipoteseCriada

Ocorre quando uma hipotese diagnostica e registrada com nivel de confianca.

### HipoteseRevisada

Ocorre quando nova informacao altera confianca, criterios ou status de uma hipotese.

### ObjetivoTerapeuticoDefinido

Ocorre quando um objetivo terapeutico e criado para orientar raciocinio.

### AnaliseDeRiscoExecutada

Ocorre quando o sistema executa avaliacao de seguranca clinica.

### AlertaDeSegurancaEmitido

Ocorre quando uma regra ou motor identifica risco relevante.

### EstrategiaComparada

Ocorre quando uma estrategia e comparada contra objetivos, riscos e evidencias.

### EstrategiaSelecionada

Ocorre quando o medico marca uma estrategia como escolhida ou considerada. O evento registra decisao humana, nao decisao automatica do sistema.

### EvidenciaAtualizada

Ocorre quando uma fonte cientifica e revisada, substituida, depreciada ou adicionada.

### RegraClinicaAtualizada

Ocorre quando uma regra derivada do conhecimento cientifico muda de versao.

### ExplicacaoGerada

Ocorre quando uma analise produz justificativa rastreavel.

### AnaliseAuditada

Ocorre quando uma analise e registrada com entradas, saidas, fontes e versoes.

## 9. Regras de Negocio

- O paciente deve ser o centro de qualquer analise.
- Raciocinio clinico deve preceder comparacao de estrategias.
- Seguranca clinica deve ser executada antes de qualquer saida estrategica.
- Estrategia terapeutica nao pode existir sem objetivo terapeutico.
- Hipotese diagnostica deve possuir nivel de confianca.
- Psicofarmaco deve possuir modelo oficial e fonte cientifica.
- Informacao cientifica deve possuir fonte.
- Recomendacao ou comparacao deve possuir justificativa.
- Risco elevado deve bloquear recomendacoes fortes ou conclusoes estrategicas sem ressalva.
- Dados clinicos ausentes relevantes devem ser explicitados.
- Saida de IA deve ser tratada como apoio explicativo, nao como decisao clinica.
- Decisao final deve permanecer com o medico.
- Toda analise deve ser rastreavel.
- Toda regra clinica deve possuir versao.
- Toda evidencia deve possuir status de revisao.
- Alertas devem informar severidade, origem e justificativa.
- Estrategias devem apresentar beneficios, riscos, limitacoes e incertezas.

## 10. Invariantes

- Nenhuma recomendacao sem evidencia.
- Nenhuma informacao cientifica sem fonte.
- Nenhuma estrategia sem objetivo terapeutico.
- Nenhuma estrategia sem analise de risco.
- Nenhuma hipotese sem nivel de confianca.
- Nenhum psicofarmaco sem modelo oficial.
- Nenhum alerta sem justificativa.
- Nenhuma decisao sem rastreabilidade.
- Nenhuma analise sem versao do conhecimento utilizado.
- Nenhuma saida clinica deve ocultar incerteza relevante.
- Nenhuma comparacao deve ser apresentada como prescricao automatica.
- Nenhum motor clinico deve substituir a decisao medica.
- Nenhuma atualizacao cientifica deve ocorrer sem versionamento.
- Nenhum resultado deve misturar dado do paciente, inferencia e evidencia sem diferenciacao.

## 11. Dependencias Entre Contextos

Os contextos devem se comunicar por referencias, eventos e contratos conceituais, evitando compartilhamento direto de estruturas internas.

Fluxo preferencial de dependencia:

- Paciente fornece identidade e estado longitudinal.
- Avaliacao Clinica consome dados do Paciente e produz leitura contextual.
- Sintomas alimentam Avaliacao Clinica, Hipoteses e Monitorizacao.
- Hipoteses Diagnosticas dependem de Avaliacao Clinica e Sintomas.
- Objetivos Terapeuticos dependem de Hipoteses, Sintomas e Avaliacao.
- Seguranca Clinica consome Paciente, Avaliacao, Psicofarmacos e Evidencias.
- Estrategias Terapeuticas dependem de Objetivos, Seguranca e Evidencias.
- Psicofarmacos dependem de Evidencias Cientificas.
- Explicabilidade consome resultados de todos os contextos, mas nao altera regras.
- Auditoria observa eventos de todos os contextos, mas nao interfere no dominio clinico.

Regras de desacoplamento:

- Estrategias nao devem acessar diretamente detalhes internos do Paciente sem passar pela Avaliacao Clinica.
- Motores de seguranca devem consultar conhecimento cientifico por repositorios ou contratos do contexto de Evidencias.
- Explicabilidade deve referenciar resultados e fontes, nao recalcular decisoes.
- Auditoria deve registrar eventos, nao governar comportamento clinico.
- IA deve consumir saidas estruturadas e fontes, nao criar fatos clinicos primarios.

## 12. Diagrama Conceitual

### Mapa de contextos

```text
[Paciente]
    |
    v
[Avaliacao Clinica] <---- [Sintomas]
    |
    v
[Hipoteses Diagnosticas]
    |
    v
[Objetivos Terapeuticos]
    |
    v
[Seguranca Clinica] <---- [Psicofarmacos] <---- [Evidencias Cientificas]
    |
    v
[Estrategias Terapeuticas]
    |
    v
[Monitorizacao]

[Explicabilidade] observa e explica:
Paciente, Avaliacao, Hipoteses, Objetivos, Seguranca, Estrategias, Psicofarmacos e Evidencias.

[Auditoria] registra eventos de todos os contextos.
```

### Estrutura central do dominio

```text
Paciente
  -> AvaliacaoClinica
      -> Sintoma
      -> HipoteseDiagnostica
      -> ObjetivoTerapeutico
      -> AnaliseClinica
          -> AlertaDeSeguranca
          -> EstrategiaTerapeutica
          -> Explicacao
          -> RegistroDeAuditoria

Psicofarmaco
  -> ClasseFarmacologica
  -> InteracaoMedicamentosa
  -> RegraClinica
  -> EvidenciaCientifica

EvidenciaCientifica
  -> NivelDeEvidencia
  -> ReferenciaCientifica
  -> Versao
```

### Sequencia conceitual de analise

```text
1. Medico atualiza Paciente
2. AvaliacaoClinica e registrada
3. Sintomas e dados objetivos sao organizados
4. HipotesesDiagnosticas sao formuladas com nivel de confianca
5. ObjetivosTerapeuticos sao definidos
6. SegurancaClinica executa avaliacao obrigatoria
7. AlertasDeSeguranca podem ser emitidos
8. EstrategiasTerapeuticas sao comparadas somente se permitido pela seguranca
9. EvidenciasCientificas justificam afirmacoes e comparacoes
10. Explicabilidade gera justificativa rastreavel
11. Auditoria registra entradas, saidas, fontes, regras e versoes
12. Medico decide
```

## 13. Preparacao para Implementacao

Esta modelagem prepara o PsychRx para implementacao futura em qualquer tecnologia porque define o dominio antes da infraestrutura. As entidades, value objects, aggregates, eventos, servicos de dominio e repositorios aqui descritos nao dependem de linguagem, framework, banco de dados ou arquitetura fisica especifica.

A implementacao futura deve preservar:

- separacao entre dominio e infraestrutura;
- conhecimento cientifico fora do codigo operacional;
- fronteiras claras entre bounded contexts;
- aggregate roots como pontos de consistencia;
- domain services para regras que atravessam entidades;
- eventos de dominio para comunicacao desacoplada;
- repositorios como abstracoes conceituais de persistencia;
- logs e auditoria como parte nativa do dominio;
- explicabilidade como requisito obrigatorio;
- medico como decisor final.

O modelo permite evoluir o MVP sem comprometer a coerencia clinica. Novos motores, novas fontes, novos objetos de conhecimento e futuras interfaces podem ser adicionados desde que respeitem os invariantes do dominio e a separacao entre paciente, raciocinio, seguranca, conhecimento cientifico, explicabilidade e auditoria.

O resultado esperado da implementacao futura nao deve ser um prescritor automatico, mas uma plataforma clinicamente rastreavel de apoio ao julgamento medico em psicofarmacologia.
