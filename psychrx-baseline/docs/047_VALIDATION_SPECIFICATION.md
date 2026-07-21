# 047 - Validation Specification

## 1. Objetivo

Definir todas as validacoes conceituais obrigatorias do PsychRx, sem implementar validadores, schemas, testes ou codigo.

## 2. Missao

Garantir que dominio, conhecimento, motores, entradas, saidas, seguranca e evidencia sejam avaliados antes de uso oficial.

## 3. Validacao de Dominio

Verifica invariantes:

- paciente identificado conceitualmente;
- Snapshot coerente;
- hipotese com nivel de confianca;
- objetivo antes de estrategia;
- estrategia com justificativa;
- decisao com rastreabilidade.

## 4. Validacao de Conhecimento

Verifica:

- fonte;
- versao;
- status;
- metadados;
- aplicabilidade;
- relacoes;
- conflitos;
- data de revisao.

## 5. Validacao de Motores

Cada motor deve validar pre-condicoes, entradas obrigatorias, saidas obrigatorias, erros, limites e dependencia correta.

## 6. Validacao de Entradas

Entradas devem ser completas, coerentes, rastreaveis e semanticamente validas.

Dado ausente relevante deve ser tratado como incerteza.

## 7. Validacao de Saidas

Saidas devem ter justificativa, status, fonte quando aplicavel, incerteza e trilha de auditoria.

Saida clinica sem explicacao deve falhar.

## 8. Validacao de Seguranca

Deve confirmar avaliacao de risco suicida, agressividade, delirium, intoxicacao, abstinencia, gestacao, lactacao, insuficiencia renal, insuficiencia hepatica, doenca cardiovascular, QT, epilepsia, interacoes, alergias e reacoes graves previas quando aplicavel.

## 9. Validacao de Evidencia

Deve confirmar fonte, ano, tipo, qualidade, forca, status, conflitos, aplicabilidade e data de revisao.

Nenhuma regra terapeutica entra sem evidencia rastreavel.

## 10. Limites

Este documento nao implementa validacao tecnica nem define biblioteca de validacao.

## 11. Declaracao Final

Validation Specification define o que precisa ser verdadeiro antes do PsychRx confiar em qualquer entrada, saida, motor ou conhecimento.

No PsychRx, validar e parte da seguranca clinica.
