# DM-016 — Fronteiras arquiteturais executáveis

## Objetivo

Transformar as regras de dependência herdadas do blueprint do PsychRx em uma
verificação estática executada junto da suíte de testes do DecisionMEd.

## Política aplicada

| Camada protegida | Dependências internas permitidas |
| --- | --- |
| `domain` | nenhuma |
| `evidence` | nenhuma |
| `knowledge` | `evidence` |
| `safety` | `domain`, `evidence`, `knowledge` |
| `audit` | `domain` |

Importações dentro da própria camada são permitidas. Bibliotecas externas e da
biblioteca padrão não participam desta verificação.

## Implementação

`decisionmed.architecture.scan_architecture` analisa a árvore sintática dos
arquivos Python sem importar nem executar o produto. Importações absolutas e
relativas que cruzem uma fronteira proibida geram violações determinísticas.

O teste `test_current_source_respects_layer_boundaries` faz a política valer no
CI. Testes isolados também provam que violações artificiais são detectadas e que
dependências documentadas são aceitas.

## Segurança e reversão

A missão não altera comportamento clínico, dados, interface ou o baseline do
PsychRx. A reversão consiste em remover o analisador, seu teste e este documento.
