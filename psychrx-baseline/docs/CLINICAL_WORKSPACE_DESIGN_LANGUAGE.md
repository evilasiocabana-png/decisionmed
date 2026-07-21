# Clinical Workspace Design Language

## 1. Objetivo

Definir a linguagem oficial de experiencia do Clinical Workspace do PsychRx.

Este documento nao cria software, nao implementa UI, nao cria IA, nao cria Clinical Kernel e nao define regra terapeutica.

Ele padroniza conceitos usados na documentacao, arquitetura, contratos futuros e implementacao.

## 2. Principio Central

O PsychRx nao deve pensar primeiro em telas.

O PsychRx deve pensar em microexperiencias clinicas.

Essas microexperiencias sao chamadas de:

```text
Clinical Widgets
```

## 3. Clinical Workspace

Clinical Workspace e o ambiente da consulta.

Ele organiza paciente, snapshot, investigacao, medicacao, riscos, objetivos, estrategias bloqueadas ou revisaveis, monitorizacao, evidencia, conversa, timeline, informacoes ausentes e confianca clinica futura.

O Workspace nao decide conduta.

O Workspace nao prescreve.

O Workspace nao substitui o medico.

## 4. Clinical Widget

Clinical Widget e a unidade basica da experiencia clinica.

Um Clinical Widget pode ser:

- card;
- timeline;
- lista;
- painel;
- modal;
- overlay;
- indicador;
- faixa de status.

O termo `Card` fica reservado para uma forma visual possivel, nao para a unidade arquitetural.

## 5. Estrutura Conceitual de um Widget

Cada Clinical Widget deve possuir:

```text
View
-> ViewModel
-> Contracts
-> Tests
-> Documentation
```

Nesta fase, esses elementos sao conceituais. Implementacao so deve ocorrer em missao futura de software.

## 6. Widgets Oficiais Iniciais

```text
Clinical Workspace
    Patient Widget
    Snapshot Widget
    Clinical Investigation Panel
    Medication Widget
    Risk Widget
    Objectives Widget
    Strategy Widget
    Timeline Widget
    Monitoring Widget
    Evidence Widget
    Conversation Widget
    Missing Information Widget
    Clinical Confidence Widget
    Clinical Compass
```

## 7. Clinical Investigation Panel

Substitui o nome `Live Question Panel` para novas missoes.

O painel nao mostra apenas perguntas.

Ele conduz investigacao clinica de forma organizada, exibindo poucas lacunas relevantes em cada momento.

Exemplo conceitual:

```text
Investigar Sono

[ ] Latencia
[ ] Despertares
[ ] Ronco
[ ] Cafeina
[ ] Alcool
```

Nesta fase, nao ha IA e nao ha algoritmo clinico. A dinamica e uma especificacao de experiencia futura.

## 8. Clinical Compass

Clinical Compass e o indicador de orientacao da consulta.

Ele pode mostrar, conceitualmente:

```text
Consulta
[#######---]

Informacoes suficientes: nao
Hipoteses: em avaliacao
Seguranca: pendente
```

O Clinical Compass informa progresso.

Ele nao decide se a consulta esta pronta.

Ele nao libera estrategia.

## 9. Missing Information Widget

O Missing Information Widget mostra lacunas clinicas relevantes.

Exemplo:

```text
Ainda falta descobrir

[ ] Mania
[ ] Uso de alcool
[ ] Gestacao
[ ] Ideacao suicida
```

Ele nao diagnostica, nao prescreve e nao substitui a entrevista medica.

## 10. Clinical Confidence Widget

Clinical Confidence Widget representa, no futuro, graus de confianca de hipoteses ou informacoes.

Nesta fase, e apenas infraestrutura conceitual.

Ele nao deve apresentar diagnostico automatico.

Ele nao deve substituir julgamento medico.

## 11. Arquitetura Futura de Apresentacao

Estrutura conceitual futura:

```text
presentation/
    workspace/
        widgets/
            patient/
            snapshot/
            investigation/
            medication/
            risks/
            objectives/
            strategy/
            monitoring/
            evidence/
            conversation/
            timeline/
            compass/
            missing_information/
            confidence/
```

Essa estrutura nao deve ser criada sem missao de software especifica.

## 12. Regras de Linguagem

Usar:

- Clinical Workspace;
- Clinical Widget;
- Clinical Investigation Panel;
- Clinical Compass;
- Missing Information Widget;
- Clinical Confidence Widget.

Evitar:

- tela como unidade arquitetural;
- card como unidade geral;
- question panel como nome principal;
- dashboard como fonte da experiencia;
- widget como motor clinico.

## 13. Limites

Clinical Widgets nao podem:

- prescrever;
- diagnosticar automaticamente;
- gerar conduta;
- esconder risco;
- apresentar estrategia antes de safety;
- usar evidencia sem fonte futura;
- substituir o medico.

## Declaracao Final

A Clinical Workspace Design Language define o vocabulario do PsychRx para transformar a consulta em um conjunto de microexperiencias clinicas reutilizaveis, preparando a futura integracao com o Clinical Kernel sem permitir que a interface decida conduta.
