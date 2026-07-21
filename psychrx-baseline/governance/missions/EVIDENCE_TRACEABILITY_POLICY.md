# Evidence Traceability Policy

## 1. Proposito

Este documento define a politica obrigatoria de rastreabilidade cientifica do PsychRx.

Seu objetivo e impedir a entrada de conhecimento clinico sem fonte, sem qualidade definida, sem status de revisao e sem aplicabilidade clinica documentada.

No PsychRx, nenhuma regra terapeutica, alerta clinico, relacao farmacologica, contraindicação, interacao, efeito adverso ou afirmacao cientifica relevante pode entrar no sistema sem evidencia rastreavel.

## 2. Regra Central

Toda informacao clinica devera conter:

- fonte;
- ano;
- tipo de evidencia;
- qualidade da evidencia;
- forca da recomendacao;
- data de revisao;
- status;
- conflitos conhecidos;
- aplicabilidade clinica.

Se qualquer item obrigatorio estiver ausente, a informacao deve permanecer em estado incompleto e nao pode sustentar recomendacao, regra terapeutica ou alerta definitivo.

## 3. Escopo

Esta politica se aplica a:

- regras terapeuticas;
- alertas de seguranca;
- contraindicações;
- interacoes medicamentosas;
- efeitos adversos;
- perfis de psicofarmacos;
- objetivos terapeuticos baseados em evidencia;
- criterios de monitorizacao;
- relacoes entre sintomas, sindromes e tratamentos;
- recomendacoes, comparacoes ou sugestoes clinicas futuras;
- qualquer conhecimento usado por motores clinicos futuros.

## 4. Campos Obrigatorios

### Fonte

Toda informacao deve indicar sua origem cientifica ou regulatoria.

Fontes podem incluir:

- diretrizes;
- revisoes sistematicas;
- meta-analises;
- ensaios clinicos;
- estudos observacionais;
- livros-texto;
- consensos;
- regulamentacoes;
- alertas oficiais.

### Ano

Toda fonte deve registrar o ano de publicacao ou atualizacao.

O ano permite avaliar atualidade, necessidade de revisao e possivel substituicao por evidencia mais recente.

### Tipo de Evidencia

O tipo de evidencia deve classificar a natureza da fonte.

Exemplos:

- guideline;
- systematic review;
- meta-analysis;
- randomized clinical trial;
- observational study;
- textbook;
- consensus;
- regulation;
- safety alert.

### Qualidade da Evidencia

Toda evidencia deve receber avaliacao de qualidade.

Categorias conceituais:

- high;
- moderate;
- low;
- very low;
- insufficient.

A qualidade deve considerar metodologia, vies, consistencia, precisao, aplicabilidade, atualidade e conflitos de interesse.

### Forca da Recomendacao

A forca da recomendacao deve indicar o quanto uma evidencia sustenta uma orientacao clinica.

Categorias conceituais:

- strong;
- moderate;
- weak;
- conditional;
- insufficient for recommendation.

Forca da recomendacao nao e igual a qualidade da evidencia. Ela tambem depende de risco, beneficio, aplicabilidade, preferencia do paciente e contexto clinico.

### Data de Revisao

Toda informacao deve possuir data de revisao interna.

A data de revisao indica quando a fonte ou sua interpretacao foi avaliada pelo projeto.

### Status

Toda informacao deve possuir status definido.

Status oficiais:

- `draft`;
- `awaiting validation`;
- `validated`;
- `deprecated`;
- `conflicting evidence`.

### Conflitos Conhecidos

Toda informacao deve registrar se ha conflito entre fontes, diretrizes, estudos ou interpretacoes.

Quando houver conflito, deve indicar:

- fontes conflitantes;
- natureza do conflito;
- impacto na conclusao;
- necessidade de cautela;
- efeito sobre a forca da recomendacao.

### Aplicabilidade Clinica

Toda informacao deve indicar em que contexto clinico se aplica.

Deve considerar:

- populacao;
- diagnostico ou sindrome;
- faixa etaria;
- comorbidades;
- gestacao ou lactacao;
- gravidade;
- setting clinico;
- restricoes;
- limites de generalizacao.

## 5. Status Oficiais

### draft

Informacao registrada de forma preliminar, ainda sem revisao suficiente.

Nao pode sustentar regra terapeutica, recomendacao ou alerta definitivo.

### awaiting validation

Informacao em processo de validacao cientifica ou metodologica.

Pode ser discutida internamente, mas deve ser apresentada com cautela e nao deve sustentar decisao clinica forte.

### validated

Informacao revisada, com fonte, qualidade, aplicabilidade e status aprovados.

Pode sustentar conhecimento, regra, alerta ou explicacao, respeitando limites clinicos.

### deprecated

Informacao substituida, desatualizada ou considerada inadequada.

Nao deve sustentar novas decisoes, mas pode permanecer para rastreabilidade historica.

### conflicting evidence

Informacao com conflito relevante entre fontes.

Pode ser usada apenas com declaracao explicita de incerteza, reducao da forca de recomendacao e revisao medica.

## 6. Regras Terapeuticas

Nenhuma regra terapeutica pode entrar no sistema sem evidencia rastreavel.

Uma regra terapeutica deve indicar:

- fonte primaria ou secundaria;
- ano;
- tipo de evidencia;
- qualidade;
- forca da recomendacao;
- aplicabilidade;
- conflitos;
- status;
- data de revisao;
- versao do conhecimento.

Regra terapeutica sem evidencia rastreavel deve ser rejeitada.

## 7. Conhecimento Clinico sem Fonte

Conhecimento clinico sem fonte nao deve ser tratado como conhecimento oficial do PsychRx.

Pode existir temporariamente apenas como:

- nota de pesquisa;
- item `draft`;
- pergunta em aberto;
- hipotese a validar;
- pendencia de curadoria.

Nao pode sustentar:

- `TherapeuticStrategy`;
- `SafetyAlert` definitivo;
- contraindicação oficial;
- interacao oficial;
- regra terapeutica;
- `ClinicalExplanation` conclusiva;
- criterio de monitorizacao obrigatorio.

## 8. Rastreabilidade Minima

Toda informacao clinica deve permitir reconstruir:

```text
informacao clinica -> fonte -> ano -> tipo de evidencia -> qualidade -> forca da recomendacao -> status -> revisao -> aplicabilidade
```

Sem essa cadeia, a informacao e incompleta.

## 9. Atualizacao e Revisao

Informacoes cientificas devem ser revisadas quando:

- nova diretriz for publicada;
- nova revisao sistematica ou meta-analise surgir;
- novo ensaio clinico relevante for publicado;
- alerta regulatorio modificar risco;
- conflito entre fontes for identificado;
- fonte anterior for depreciada;
- regra clinica depender de evidencia antiga;
- documento oficial do PsychRx for alterado.

Toda revisao deve atualizar:

- data de revisao;
- status;
- conflitos conhecidos;
- aplicabilidade clinica;
- impacto sobre regras ou alertas;
- versao do conhecimento.

## 10. Relacao com Evidence Graph

O Evidence Graph usa esta politica para conectar decisoes clinicas a evidencias.

Uma decisao explicavel deve indicar:

- quais fontes sustentam a decisao;
- qual qualidade da evidencia;
- qual forca da recomendacao;
- quais conflitos existem;
- qual aplicabilidade ao paciente;
- qual status da evidencia;
- quando a evidencia foi revisada.

## 11. Relacao com Biblioteca Cientifica

A Biblioteca Cientifica organiza fontes. Esta politica define os metadados obrigatorios para que essas fontes possam sustentar conhecimento clinico.

Fonte registrada sem metadados obrigatorios nao deve ser considerada pronta para uso clinico.

## 12. Relacao com Pull Requests

Todo Pull Request que introduzir conhecimento clinico deve declarar:

- fonte;
- ano;
- tipo de evidencia;
- qualidade;
- forca da recomendacao;
- data de revisao;
- status;
- conflitos conhecidos;
- aplicabilidade clinica.

Pull Requests que introduzirem conhecimento clinico sem esses campos devem ser rejeitados.

## 13. Criterio de Aceite

Esta politica deve impedir conhecimento clinico sem fonte.

Nenhuma informacao clinica deve ser aceita se:

- nao possuir fonte;
- nao possuir ano;
- nao possuir tipo de evidencia;
- nao possuir qualidade da evidencia;
- nao possuir forca da recomendacao;
- nao possuir data de revisao;
- nao possuir status;
- nao informar conflitos conhecidos;
- nao informar aplicabilidade clinica;
- tentar sustentar regra terapeutica sem evidencia rastreavel.

## 14. Declaracao Final

A rastreabilidade cientifica e obrigatoria no PsychRx.

Conhecimento clinico sem fonte nao e conhecimento oficial. Regra terapeutica sem evidencia rastreavel nao entra no sistema. Toda afirmacao clinica relevante deve carregar origem, qualidade, status, revisao, conflitos e aplicabilidade.

Essa politica protege o PsychRx contra opinioes sem lastro, recomendacoes opacas e conhecimento clinico impossivel de auditar.
