# 021 - Explanation Engine

## 1. Definicao

O Explanation Engine e o motor conceitual responsavel por transformar o raciocinio do PsychRx em explicacoes clinicas compreensiveis, rastreaveis e revisaveis.

Ele nao cria justificativas decorativas. Ele torna visivel por que uma conclusao, alerta, comparacao, incerteza ou restricao apareceu no raciocinio.

## 2. Missao

A missao do Explanation Engine e garantir que nenhuma informacao clinica relevante seja apresentada sem justificativa, fonte, contexto e limites.

Ele responde a pergunta:

```text
Por que o sistema chegou a esta leitura clinica, com base em quais dados, evidencias, restricoes e incertezas?
```

## 3. Responsabilidades

O motor deve:

- explicar hipoteses;
- explicar objetivos;
- explicar alertas;
- explicar bloqueios;
- explicar comparacoes entre estrategias;
- explicar fatores favoraveis;
- explicar fatores desfavoraveis;
- mostrar alternativas consideradas;
- mostrar evidencias;
- mostrar incertezas;
- preservar rastreabilidade.

## 4. Entradas Conceituais

As entradas conceituais incluem:

- Clinical Snapshot;
- perguntas e lacunas do Question Engine;
- hipoteses diagnosticas;
- objetivos terapeuticos;
- restricoes;
- alertas e bloqueios de seguranca;
- estrategias consideradas;
- evidencias cientificas;
- conflitos de evidencia;
- dados longitudinais;
- decisao ou leitura clinica a ser explicada.

## 5. Saidas Conceituais

As saidas conceituais incluem:

- justificativa clinica;
- dados que sustentam a leitura;
- dados que contradizem ou limitam a leitura;
- evidencias vinculadas;
- qualidade e aplicabilidade da evidencia;
- alternativas consideradas;
- fatores favoraveis;
- fatores desfavoraveis;
- incertezas;
- limites da interpretacao;
- trilha de rastreabilidade.

## 6. Justificativas

Toda justificativa deve conectar:

- dado clinico;
- interpretacao;
- evidencia;
- restricao;
- grau de incerteza;
- implicacao clinica;
- limite da conclusao.

Justificativa sem rastreabilidade nao deve ser considerada suficiente.

## 7. Evidencias

O Explanation Engine deve mostrar quando uma leitura depende de:

- diretriz clinica;
- revisao sistematica;
- meta-analise;
- ensaio clinico;
- consenso;
- livro-texto;
- documento regulatorio;
- evidencia limitada ou conflitante.

Quando houver conflito, o conflito deve ser mencionado, nao escondido.

## 8. Alternativas Consideradas

Explicar uma estrategia tambem exige mostrar alternativas consideradas.

O motor deve indicar:

- quais caminhos foram comparados;
- por que uma alternativa parece mais favoravel;
- por que outra alternativa parece menos favoravel;
- quais alternativas foram bloqueadas;
- quais alternativas permanecem incertas.

## 9. Fatores Favoraveis

Fatores favoraveis podem incluir:

- alinhamento com objetivo terapeutico;
- evidencia aplicavel;
- resposta previa favoravel;
- tolerabilidade previa;
- menor conflito com restricoes;
- preferencia do paciente;
- facilidade de monitorizacao;
- coerencia com trajetoria longitudinal.

Fator favoravel nao anula risco critico.

## 10. Fatores Desfavoraveis

Fatores desfavoraveis podem incluir:

- risco clinico;
- contraindicação;
- interacao;
- evento adverso previo;
- evidencia fraca;
- evidencia conflitante;
- baixa aplicabilidade;
- baixa adesao;
- necessidade de monitorizacao indisponivel;
- preferencia contraria do paciente.

Fatores desfavoraveis devem ser apresentados com clareza proporcional ao risco.

## 11. Incertezas

O motor deve explicitar:

- dados ausentes;
- hipoteses alternativas;
- limites da evidencia;
- conflitos cientificos;
- ambiguidade longitudinal;
- baixa confianca;
- necessidade de nova avaliacao.

Incerteza nao deve ser escondida para produzir uma resposta aparentemente mais forte.

## 12. Transparencia

Transparencia significa permitir que o medico entenda e revise o raciocinio.

O Explanation Engine deve evitar:

- conclusoes opacas;
- autoridade sem justificativa;
- linguagem prescritiva automatica;
- ocultar dados contraditorios;
- apresentar evidencia como absoluta quando ela e limitada.

## 13. Rastreabilidade

Toda explicacao deve permitir reconstruir:

```text
dado clinico
  -> interpretacao
  -> evidencia ou regra conceitual
  -> restricao ou alerta
  -> conclusao explicada
```

Sem rastreabilidade, a explicacao e incompleta.

## 14. Relacao com Evidence Graph

O Evidence Graph sustenta a ligacao entre decisoes, fontes, qualidade da evidencia, conflitos e atualizacao.

O Explanation Engine transforma essa ligacao em explicacao clinica compreensivel.

## 15. Relacao com Decision Graph

O Decision Graph mostra caminhos, bifurcacoes e pontos criticos.

O Explanation Engine explica por que determinado caminho foi considerado, limitado, bloqueado ou mantido incerto.

## 16. Relacao com Clinical Operating Mind

O Explanation Engine atravessa todos os componentes do Clinical Operating Mind.

Ele deve explicar perguntas, hipoteses, objetivos, restricoes, seguranca, estrategias, monitorizacao e leitura longitudinal.

## 17. Limites

O Explanation Engine nao deve:

- fabricar justificativas;
- usar fonte inexistente;
- ocultar conflito;
- substituir decisao medica;
- transformar explicacao em prescricao;
- reduzir incerteza artificialmente;
- misturar conhecimento cientifico com algoritmo.

## 18. Declaracao Final

O Explanation Engine e o motor que torna o PsychRx clinicamente auditavel.

Ele transforma raciocinio em justificativa, evidencia em transparencia e incerteza em informacao util.

No PsychRx, nenhuma estrategia, alerta ou conclusao deve existir sem explicacao rastreavel.
