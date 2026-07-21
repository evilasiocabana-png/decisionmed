# 035 - Decision State Machine

## 1. Objetivo

Modelar conceitualmente a maquina de estados da decisao clinica do PsychRx, sem implementar codigo, software, workflow tecnico ou automacao prescritiva.

## 2. Missao

A missao da Decision State Machine e definir estados, transicoes, gatilhos, condicoes, bloqueios, rollback e encerramento do fluxo de decisao clinica.

## 3. Estados

Estados conceituais principais:

- aguardando dados;
- Snapshot em construcao;
- seguranca pendente;
- hipoteses em avaliacao;
- objetivos em definicao;
- restricoes em avaliacao;
- estrategias candidatas;
- estrategias em comparacao;
- explicacao em construcao;
- monitorizacao definida;
- acompanhamento longitudinal;
- fluxo interrompido por risco;
- fluxo encerrado.

## 4. Transicoes

Transicoes sao mudancas entre estados quando condicoes clinicas sao satisfeitas.

Exemplos:

- de Snapshot em construcao para seguranca pendente;
- de seguranca pendente para hipoteses em avaliacao;
- de objetivos em definicao para estrategias candidatas;
- de estrategias em comparacao para explicacao;
- de monitorizacao para acompanhamento longitudinal.

## 5. Gatilhos

Gatilhos podem incluir:

- novo dado clinico;
- risco identificado;
- dado essencial ausente;
- evidencia conflitante;
- mudanca de hipotese;
- mudanca de objetivo;
- evento adverso;
- resposta parcial;
- recaida;
- recorrencia;
- remissao;
- estabilidade.

## 6. Condicoes

Condicoes definem quando uma transicao e permitida.

Exemplos:

- estrategia exige objetivo terapeutico;
- comparacao exige seguranca avaliada;
- explicacao exige rastreabilidade;
- monitorizacao exige risco e objetivo conhecidos;
- estabilidade exige dados longitudinais.

## 7. Bloqueios

Bloqueios impedem avancar no fluxo.

Bloqueios podem ocorrer por risco agudo, ausencia de dado essencial, contraindicação critica, interacao grave, falta de evidencia rastreavel ou impossibilidade de explicacao.

## 8. Rollback

Rollback conceitual e o retorno a estado anterior quando uma premissa muda.

Exemplos:

- nova informacao invalida hipotese;
- novo risco bloqueia estrategia;
- evidencia e depreciada;
- evento adverso exige revisao;
- monitorizacao mostra deterioracao.

## 9. Encerramento

Encerramento ocorre quando o raciocinio atingiu uma saida conceitual suficiente:

- explicacao entregue ao medico;
- necessidade de encaminhamento indicada;
- monitorizacao definida;
- incerteza registrada;
- fluxo bloqueado por seguranca;
- acompanhamento longitudinal iniciado.

Encerramento nao significa decisao medica final automatica.

## 10. Limites

Esta maquina de estados nao e implementacao tecnica. Nao define codigo, eventos de software, filas, APIs ou persistencia.

## 11. Declaracao Final

A Decision State Machine organiza a decisao clinica como percurso controlado, reversivel e seguro.

No PsychRx, nenhum estado deve avancar quando seguranca, evidencia, objetivo, explicabilidade ou rastreabilidade estiverem insuficientes.
