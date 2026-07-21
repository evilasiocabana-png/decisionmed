# 027 - Clinical Context Engine

## 1. Definicao

O Clinical Context Engine e o motor conceitual responsavel por organizar fatores contextuais que modificam o raciocinio clinico do PsychRx.

Ele garante que o paciente seja compreendido como pessoa em uma trajetoria, nao apenas como lista de sintomas ou diagnosticos.

Este documento nao implementa software, nao define API, nao cria banco de dados, nao escolhe tecnologia e nao descreve algoritmo executavel.

## 2. Missao

A missao do Clinical Context Engine e integrar historico, comorbidades, funcionalidade, contexto social, contexto familiar, preferencias e qualidade de vida ao raciocinio clinico.

## 3. Responsabilidades

- Identificar fatores contextuais relevantes.
- Diferenciar contexto de evidencia terapeutica.
- Modificar objetivos, restricoes e monitorizacao quando apropriado.
- Apoiar individualizacao.
- Preservar paciente no centro.
- Evitar recomendacao sem evidencia.

## 4. Entradas Conceituais

- Clinical Snapshot.
- Historico clinico.
- Comorbidades.
- Contexto social.
- Contexto familiar.
- Funcionalidade.
- Qualidade de vida.
- Preferencias do paciente.
- Acesso a cuidado e monitorizacao.
- Eventos longitudinais.

## 5. Saidas Conceituais

- Fatores contextuais relevantes.
- Modificadores de risco.
- Modificadores de objetivo.
- Modificadores de estrategia.
- Necessidades de monitorizacao.
- Incertezas contextuais.
- Justificativas de individualizacao.

## 6. Historico

Historico clinico inclui tratamentos previos, respostas, eventos adversos, recaidas, recorrencias, remissoes, hospitalizacoes e mudancas importantes de curso.

Historico deve prevenir raciocinio como se o paciente estivesse sendo visto pela primeira vez.

## 7. Comorbidades

Comorbidades podem modificar risco, tolerabilidade, objetivos, monitorizacao e aplicabilidade da evidencia.

Elas devem ser tratadas como parte do contexto clinico e como possiveis restricoes.

## 8. Contexto Social

Contexto social pode influenciar adesao, acesso, suporte, exposicao a estressores, capacidade de monitorizacao e continuidade do cuidado.

Contexto social nao substitui evidencia, mas altera aplicabilidade e viabilidade.

## 9. Contexto Familiar

Contexto familiar pode influenciar suporte, risco, adesao, observacao de sinais de alerta e tomada de decisao compartilhada quando apropriado.

Deve ser considerado sem violar confidencialidade ou autonomia.

## 10. Funcionalidade

Funcionalidade e dimensao central do resultado clinico.

Melhora sintomatica sem recuperacao funcional pode representar sucesso parcial, nao estabilidade sustentada.

## 11. Preferencias

Preferencias do paciente devem ser registradas, respeitadas e integradas ao raciocinio.

Preferencia nao deve anular bloqueio de seguranca ou ausencia de evidencia.

## 12. Qualidade de Vida

Qualidade de vida ajuda a avaliar se a estrategia e clinicamente significativa para o paciente.

Deve dialogar com sintomas, funcionalidade, efeitos adversos, autonomia e estabilidade.

## 13. Integracao com Clinical Snapshot

O Clinical Context Engine alimenta e interpreta o Clinical Snapshot.

Contexto relevante deve aparecer no Snapshot quando modificar risco, objetivo, estrategia, monitorizacao ou explicacao.

## 14. Limites

O Clinical Context Engine nao deve:

- criar recomendacao sem evidencia;
- justificar conduta insegura;
- substituir avaliacao medica;
- transformar preferencia em prescricao;
- usar contexto para contornar restricoes;
- criar entidades fora da Ontologia.

## 15. Declaracao Final

O Clinical Context Engine preserva o paciente no centro do PsychRx.

No PsychRx, contexto nao e detalhe: e a condicao que torna evidencia, objetivo e estrategia clinicamente aplicaveis.
