# 294 - Evidence Kernel Integration

## Objetivo

Definir contrato de consumo do `EvidenceResult` pelo Kernel.

## Regra

Kernel pode ler `EvidenceResult`, mas nao deve modifica-lo.

## Declaracao Final

EvidenceResult se torna contrato imutavel para motores consumidores.
