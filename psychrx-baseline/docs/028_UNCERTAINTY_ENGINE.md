# 028 - Uncertainty Engine

## 1. Definicao

O Uncertainty Engine e o motor conceitual responsavel por representar, comunicar e reduzir incertezas clinicas no PsychRx.

Ele impede que o sistema transforme dados incompletos, evidencia limitada ou hipoteses concorrentes em conclusoes artificiais.

Este documento nao implementa software, nao define API, nao cria banco de dados, nao escolhe tecnologia e nao descreve algoritmo executavel.

## 2. Missao

A missao do Uncertainty Engine e tornar a incerteza explicita, rastreavel e clinicamente util.

## 3. Responsabilidades

- Identificar dados ausentes.
- Identificar evidencia insuficiente.
- Identificar conflitos entre diretrizes ou estudos.
- Representar hipoteses concorrentes.
- Comunicar incerteza.
- Indicar impacto da incerteza na decisao.
- Acionar Question Engine quando perguntas podem reduzir incerteza.
- Apoiar Explanation Engine.

## 4. Entradas Conceituais

- Clinical Snapshot.
- Dados ausentes.
- Hipoteses diagnosticas.
- Evidencias e conflitos.
- Restricoes.
- Alertas de seguranca.
- Estrategias candidatas.
- Historico longitudinal.
- Perguntas pendentes.

## 5. Saidas Conceituais

- Incertezas identificadas.
- Fonte da incerteza.
- Impacto clinico.
- Perguntas para reducao da incerteza.
- Restricoes decorrentes da incerteza.
- Limites da explicacao.
- Necessidade de monitorizacao ou reavaliacao.

## 6. Dados Ausentes

Dado ausente nao deve ser tratado como dado negativo.

Quando a ausencia envolver seguranca essencial, o sistema deve reduzir confianca, gerar pergunta ou bloquear comparacao favoravel.

## 7. Evidencia Insuficiente

Evidencia insuficiente deve ser explicitada quando a base cientifica nao sustentar conclusao forte.

Isso pode ocorrer por baixa qualidade, baixa aplicabilidade, poucos estudos, populacao diferente ou resultados inconsistentes.

## 8. Conflitos entre Diretrizes

Conflitos entre diretrizes, estudos ou documentos regulatorios devem ser registrados.

O sistema nao deve esconder conflito para produzir resposta simples.

## 9. Hipoteses Concorrentes

Hipoteses concorrentes devem permanecer abertas quando os dados nao permitirem diferenciar com seguranca.

Cada hipotese deve ter dados favoraveis, dados contrarios e perguntas pendentes.

## 10. Comunicacao da Incerteza

Incerteza deve ser comunicada de forma clara, proporcional e util para o medico.

Ela deve indicar o que se sabe, o que nao se sabe, por que isso importa e como pode ser reduzida.

## 11. Impacto na Decisao

Incerteza pode:

- reduzir confianca;
- exigir nova pergunta;
- exigir monitorizacao;
- limitar estrategia;
- bloquear comparacao;
- exigir encaminhamento;
- preservar alternativas.

## 12. Reducao da Incerteza

Incerteza deve ser reduzida por novas informacoes, melhor contextualizacao, evidencia adicional, monitorizacao ou revisao longitudinal.

Nao deve ser reduzida por inferencia sem base.

## 13. Integracao com Question Engine

Quando uma pergunta pode reduzir incerteza clinicamente relevante, o Uncertainty Engine deve alimentar o Question Engine.

## 14. Integracao com Explanation Engine

O Explanation Engine deve comunicar incertezas como parte da justificativa, nao como nota secundaria.

## 15. Limites

O Uncertainty Engine nao deve:

- decidir conduta;
- ocultar duvida;
- criar certeza artificial;
- substituir evidencia;
- tratar falta de dado como seguranca;
- permitir recomendacao sem justificativa.

## 16. Declaracao Final

O Uncertainty Engine protege o PsychRx contra falsas certezas.

No PsychRx, incerteza bem representada e parte da seguranca clinica, da rastreabilidade e da explicabilidade.
