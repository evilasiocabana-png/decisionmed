# 150 - Risk Widget

## Objetivo

Implementar e documentar o Risk Widget em modo read-only no Clinical Workspace.

## Conceito

O Risk Widget torna categorias de risco clinico visiveis antes de qualquer Strategy Widget.

Nesta fase, ele e apenas uma camada de apresentacao conceitual. Ele nao calcula risco real, nao emite alerta clinico real, nao recomenda encaminhamento e nao bloqueia estrategia terapeutica real.

## Escopo Entregue

- Widget visual "Risk Widget" no app localhost.
- Categorias de risco exibidas em modo read-only.
- Diferenciacao textual entre risco critico conceitual, atencao conceitual e nao avaliado.
- Aviso explicito de dependencia futura do Clinical Kernel e do Safety Engine.
- Testes atualizados para impedir que o widget seja confundido com avaliacao clinica real.

## Categorias Minimas

- Suicidio.
- Agressividade.
- Mania.
- Psicose.
- Interacao medicamentosa.
- QT.
- Sedacao.
- Metabolico.
- Gestacao/lactacao.
- Uso de substancias.

## Limites

O Risk Widget nao:

- calcula risco real;
- emite alerta clinico real;
- recomenda encaminhamento;
- bloqueia estrategia terapeutica real;
- substitui Safety First Engine;
- substitui avaliacao medica;
- usa IA;
- usa Clinical Kernel;
- acessa conhecimento cientifico;
- cria regra clinica executavel.

## Relacao com o Clinical Workspace

O widget permanece na regiao Safety and Strategy.

Ele aparece antes do Strategy Widget para reforcar a regra arquitetural de que seguranca clinica vem antes de qualquer estrategia.

## Relacao com o Clinical Kernel

Nesta fase, os riscos sao estaticos e conceituais.

Futuramente, o Clinical Kernel e o Safety Engine poderao alimentar estados reais de risco, desde que exista:

- fonte cientifica rastreavel;
- explicabilidade;
- auditoria;
- validacao clinica;
- decisao final do medico.

## Criterios de Aceite

- Risk Widget aparece no localhost.
- Todos os riscos sao conceituais/read-only.
- Ha aviso claro de que avaliacao real depende do Clinical Kernel.
- Nao calcula risco real.
- Nao emite alerta clinico real.
- Nao recomenda encaminhamento.
- Testes passam.
- PROJECT_STATUS foi atualizado.
- NEXT_MISSION aponta para MISSION 151 - Strategy Widget.

## Declaracao Final

O Risk Widget e uma camada visual read-only de seguranca conceitual. Ele nao avalia risco clinico real e aguarda futura integracao com Clinical Kernel e Safety Engine.
