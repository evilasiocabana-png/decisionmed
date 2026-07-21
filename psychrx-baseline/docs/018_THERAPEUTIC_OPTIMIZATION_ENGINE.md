# 018 - Therapeutic Optimization Engine

## 1. Definicao

O Therapeutic Optimization Engine e o motor conceitual responsavel por organizar, comparar e refinar estrategias terapeuticas possiveis a partir do estado clinico do paciente, dos objetivos terapeuticos, das restricoes, da seguranca e das evidencias.

Ele nao prescreve, nao escolhe conduta final e nao substitui o medico. Sua funcao e apoiar o raciocinio comparativo.

## 2. Missao

A missao do Therapeutic Optimization Engine e transformar objetivos terapeuticos, restricoes e evidencias em uma comparacao explicavel de caminhos terapeuticos possiveis.

Ele responde a pergunta:

```text
Quais estrategias sao conceitualmente possiveis, quais sao seus beneficios, riscos, limites e justificativas?
```

## 3. Responsabilidades

O motor deve:

- organizar estrategias terapeuticas possiveis;
- comparar alternativas;
- explicitar beneficio-risco;
- individualizar a analise ao paciente;
- respeitar restricoes;
- respeitar alertas e bloqueios de seguranca;
- vincular estrategias a evidencias;
- indicar incertezas;
- produzir insumos para explicabilidade;
- preservar o medico como decisor final.

## 4. Entradas Conceituais

As entradas conceituais incluem:

- Clinical Snapshot atualizado;
- objetivos terapeuticos ativos;
- hipoteses diagnosticas e nivel de incerteza;
- restricoes absolutas e relativas;
- resultados do Safety First Engine;
- evidencias cientificas rastreaveis;
- historico de resposta;
- tolerabilidade;
- preferencias do paciente;
- necessidades de monitorizacao;
- dados longitudinais quando disponiveis.

## 5. Saidas Conceituais

As saidas conceituais incluem:

- estrategias possiveis;
- estrategias limitadas ou bloqueadas;
- comparacao entre alternativas;
- fatores favoraveis;
- fatores desfavoraveis;
- incertezas;
- justificativas;
- necessidades de monitorizacao;
- vinculo com evidencias;
- indicacao de que a decisao final cabe ao medico.

## 6. Geracao de Estrategias

A geracao de estrategias deve partir de:

- objetivo terapeutico definido;
- estado clinico atual;
- seguranca avaliada;
- restricoes conhecidas;
- evidencias aplicaveis;
- contexto individual.

Nenhuma estrategia deve surgir apenas porque existe um psicofarmaco disponivel. O raciocinio deve partir do paciente e do objetivo, nao do medicamento.

## 7. Comparacao Entre Estrategias

A comparacao deve considerar:

- alinhamento com objetivo terapeutico;
- adequacao ao Clinical Snapshot;
- beneficio esperado;
- riscos;
- restricoes;
- tolerabilidade;
- interacoes;
- monitorizacao necessaria;
- qualidade da evidencia;
- aplicabilidade da evidencia ao paciente;
- preferencias e contexto.

Comparar nao significa recomendar automaticamente.

## 8. Beneficio-Risco

Beneficio-risco e a leitura integrada entre possivel ganho clinico e possivel dano.

O motor deve reconhecer que:

- alto beneficio nao anula risco critico;
- baixo risco nao justifica estrategia sem objetivo;
- evidencia populacional precisa ser contextualizada;
- risco individual pode modificar a forca de uma alternativa;
- seguranca precede otimizacao.

## 9. Individualizacao

A individualizacao deve considerar:

- sintomas predominantes;
- sindromes e hipoteses;
- curso longitudinal;
- comorbidades;
- tratamentos previos;
- resposta anterior;
- eventos adversos;
- preferencias do paciente;
- funcionalidade;
- qualidade de vida;
- capacidade de acompanhamento.

Individualizar nao significa improvisar. Significa aplicar conhecimento rastreavel ao contexto clinico real.

## 10. Evidencias

Toda estrategia considerada deve ter relacao com evidencias rastreaveis.

O motor deve diferenciar:

- evidencia forte;
- evidencia moderada;
- evidencia limitada;
- evidencia conflitante;
- ausencia de evidencia suficiente.

Quando a evidencia for incerta, isso deve aparecer na explicacao.

## 11. Restricoes

Restricoes podem:

- bloquear estrategia;
- reduzir favorabilidade;
- exigir monitorizacao;
- exigir encaminhamento;
- tornar alternativa dependente de avaliacao medica adicional.

O motor nao deve contornar restricoes para manter uma estrategia atraente.

## 12. Explicabilidade

Toda comparacao deve ser explicavel.

A explicacao deve incluir:

- por que a estrategia foi considerada;
- quais objetivos ela tenta atender;
- quais evidencias a sustentam;
- quais riscos foram identificados;
- quais alternativas foram consideradas;
- quais incertezas permanecem;
- quais limites existem.

## 13. Integracao com Safety First Engine

O Therapeutic Optimization Engine so pode operar apos avaliacao de seguranca suficiente.

Bloqueios absolutos impedem comparacao favoravel. Alertas criticos devem aparecer antes de qualquer comparacao. Alertas moderados devem modificar a leitura beneficio-risco.

## 14. Integracao com Evidence Graph

O Evidence Graph fornece o vinculo entre estrategia, fonte, qualidade, conflito, atualizacao e rastreabilidade.

Sem evidencia rastreavel, uma estrategia nao deve ser apresentada como sustentada.

## 15. Limites

O Therapeutic Optimization Engine nao deve:

- prescrever;
- escolher conduta final;
- substituir julgamento medico;
- criar recomendacao sem justificativa;
- operar sem seguranca;
- operar sem objetivo terapeutico;
- misturar evidencia com algoritmo;
- ocultar incerteza ou conflito.

## 16. Declaracao Final

O Therapeutic Optimization Engine e o motor de comparacao conceitual de estrategias do PsychRx.

Ele organiza possibilidades, riscos, beneficios, restricoes e evidencias para apoiar o raciocinio medico.

No PsychRx, otimizar nao e prescrever: e tornar a decisao clinica mais clara, segura, rastreavel e explicavel.
