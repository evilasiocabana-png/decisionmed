# 046 - Error Handling Specification

## 1. Objetivo

Definir como erros devem ser tratados conceitualmente no PsychRx, sem implementar excecoes, codigos de erro, logs tecnicos ou software.

## 2. Missao

Impedir que falhas clinicas, de dominio, validacao, integracao, conhecimento ou evidencia sejam ocultadas ou convertidas em respostas inseguras.

## 3. Erros Clinicos

Erros clinicos incluem risco nao avaliado, dado essencial ausente, alerta ignorado, contraindicação nao considerada, interacao omitida e estrategia sem seguranca.

Tratamento: bloquear, sinalizar, explicar e registrar para auditoria.

## 4. Erros de Dominio

Erros de dominio incluem entidade invalida, invariant violada, objetivo sem paciente, estrategia sem objetivo ou hipotese sem confianca.

Tratamento: rejeitar a operacao conceitual e indicar invariant violada.

## 5. Erros de Validacao

Erros de validacao incluem entrada incompleta, formato conceitual inadequado, nomenclatura nao oficial ou campo obrigatorio ausente.

Tratamento: solicitar correcao ou retornar ao Question Engine.

## 6. Erros de Integracao

Erros de integracao incluem contrato quebrado entre modulos, saida inesperada, dependencia ausente ou ordem de chamada indevida.

Tratamento: interromper fluxo, registrar falha e impedir inferencia insegura.

## 7. Erros de Conhecimento

Erros de conhecimento incluem objeto sem fonte, versao ausente, status invalido, relacao semantica indefinida ou conhecimento depreciado usado como ativo.

Tratamento: bloquear uso oficial e enviar para validacao ou curadoria.

## 8. Erros de Evidencia

Erros de evidencia incluem fonte ausente, conflito nao resolvido, qualidade insuficiente nao marcada, guideline desatualizada ou recomendacao sem aplicabilidade.

Tratamento: reduzir confianca, declarar incerteza ou bloquear regra clinica.

## 9. Mensagens

Mensagens devem ser claras, nao prescritivas e orientadas a correcao.

Devem informar:

- o que falhou;
- por que importa;
- qual risco existe;
- qual acao conceitual e necessaria;
- qual parte do fluxo foi interrompida.

## 10. Recuperacao

Recuperacao pode envolver:

- coletar dado ausente;
- revisar Snapshot;
- reavaliar seguranca;
- atualizar evidencia;
- validar conhecimento;
- corrigir contrato;
- retornar a estado anterior.

## 11. Limites

Este documento nao define classes de erro, exceptions, HTTP status, observabilidade tecnica ou log implementation.

## 12. Declaracao Final

Error Handling Specification transforma falhas em barreiras de seguranca.

No PsychRx, erro clinico ou arquitetural nunca deve ser escondido para manter o fluxo andando.
