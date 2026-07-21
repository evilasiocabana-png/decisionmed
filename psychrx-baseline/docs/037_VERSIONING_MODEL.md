# 037 - Versioning Model

## 1. Objetivo

Definir o modelo oficial de versionamento cientifico e conceitual do PsychRx, sem implementar ferramenta, controle de versao tecnico ou banco de dados.

## 2. Missao

A missao do Versioning Model e permitir que cada mudanca no conhecimento clinico seja identificavel, historica, auditavel e interpretavel.

## 3. Versoes

Cada objeto de conhecimento deve possuir versao.

Versao identifica o estado de um objeto em determinado momento, incluindo fonte, interpretacao, status, relacoes e aplicabilidade.

## 4. Compatibilidade

Compatibilidade indica se uma nova versao preserva relacoes e interpretacoes anteriores ou se exige revisao de objetos dependentes.

Mudancas podem ser:

- compativeis;
- parcialmente compativeis;
- incompatíveis;
- depreciadoras.

## 5. Mudancas

Mudancas devem registrar:

- motivo;
- fonte da mudanca;
- data;
- responsavel;
- impacto;
- objetos afetados;
- necessidade de revisao;
- status anterior e novo.

## 6. Historico

Historico deve preservar versoes anteriores para auditoria.

Uma decisao tomada com versao anterior deve continuar explicavel mesmo depois da atualizacao do conhecimento.

## 7. Revisao

Revisao pode confirmar, corrigir, substituir, depreciar ou arquivar uma versao.

Cada revisao deve indicar se altera seguranca, evidencia, explicabilidade, monitorizacao ou aplicabilidade.

## 8. Relacao com Evidencia

Mudanca de evidencia pode exigir nova versao de Recommendation de fonte, ClinicalRule, Contraindication, DrugInteraction ou MonitoringRecommendation.

## 9. Limites

Este modelo nao define Git, schema, tabela, API ou semantica tecnica de versionamento.

## 10. Declaracao Final

O Versioning Model torna o conhecimento do PsychRx historico e auditavel.

No PsychRx, toda informacao clinica precisa dizer de qual versao veio e por que aquela versao era valida naquele momento.
