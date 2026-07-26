# DM-309 — Orquestração dos motores clínicos

## Objetivo

Complementar o fluxo existente sem substituir `DecisionMedReasoning`, o
roteamento, a triagem, as três portas, os 300 módulos, os 4.500 casos DM-300,
os anexos ou a auditoria.

```text
Entrada registrada pelo profissional
              ↓
Motor Sindrômico
              ↓
Motor Diagnóstico
              ↓
Motor Terapêutico
              ↓
Gate de Confiança (> 95%, estrito)
       ┌──────┴──────────┐
       ↓                 ↓
Determinístico      Caso complexo
sem LLM                  ↓
                    LLM em standby
```

## Componentes

- `intake-syndromic-engine.js`: adapta a saída legada para classificações
  sindrômicas, preservando representação, segurança, achados e governança.
- `intake-diagnostic-engine.js`: organiza hipóteses em mais prováveis, graves a
  excluir e imitadores. Critérios observados, ausentes, conflitantes e pendentes
  permanecem separados. O motor nunca confirma diagnóstico.
- `intake-therapeutic-engine.js`: monta plano estrutural por hipótese, com
  segurança, exame físico, exames, tratamento em revisão, limites, destino e
  retorno. Tratamento e prescrição automáticos são sempre falsos.
- `intake-confidence-gate.js`: avalia requisitos governados. Compatibilidade
  qualitativa não é probabilidade e nunca alimenta o score.
- `intake-llm-standby.js`: adaptador inerte, sem provedor, rede, transmissão ou
  tokens.
- `intake-clinical-orchestrator.js`: executa os componentes na ordem fixa e
  produz uma decisão única, versionada e auditável.
- `intake-engine-gate-cases.js`: registro isolado das 30 fixtures do gate.

## Gate de confiança

A comparação é estritamente `score > 0.95`. A rota determinística só é elegível
quando todos os requisitos abaixo são verdadeiros:

1. score numérico calibrado entre 0 e 1;
2. calibração validada e proveniência completa;
3. hipótese dominante pertencente ao diferencial;
4. competição entre hipóteses resolvida;
5. triagem estável;
6. critérios suficientes;
7. ausência de conflito crítico;
8. hipóteses graves relevantes excluídas;
9. ausência de evidência crítica pendente;
10. ausência de conflito pós-exame;
11. conteúdo completo e fontes validadas;
12. módulo e conteúdo validados;
13. execução clínica liberada pela governança;
14. confirmação profissional;
15. autoridade e integridade da entrada verificadas.

Qualquer falha fecha o gate para `complex_case_llm_standby`. O catálogo real da
release atual está em `draft`, não possui score calibrado e informa
`clinical_execution_allowed=false`; por isso todos os casos reais seguem para
standby.

## LLM em standby

O contrato é fixo:

```json
{
  "disabled": true,
  "provider": null,
  "invoked": false,
  "transmitted": false,
  "tokenUsage": 0
}
```

Não existem chave, endpoint, `fetch`, `XMLHttpRequest` ou `WebSocket` no
adaptador. A futura ativação deverá ser outra decisão arquitetural e clínica.

## Fixtures isoladas

As 15 fixtures de alta confiança e as 15 complexas usam o namespace
`fixture.engine-gate.*`, possuem `fixtureOnly=true` e `simulationOnly=true` e
não fazem parte de `/api/clinical-cases`. Os 4.500 casos DM-300 permanecem
exatamente 300 × 15.

A bateria de alta confiança usa calibração sintética governada apenas para
provar a rota. Mesmo nessa simulação:

- a saída pública mantém execução clínica bloqueada;
- tratamento e prescrição automáticos permanecem bloqueados;
- a LLM continua sem chamada;
- adulterar os fatos altera o digest e fecha o gate.

## Auditoria

O formulário usa `decisionmed.intake-audit.v2`, preserva a referência a
`decisionmed.intake-audit.v1` e registra:

- fatos e IDs das perguntas;
- versões e ordem dos motores;
- classificações, hipóteses e critérios;
- planos terapêuticos estruturais;
- score, calibração e proveniência quando existirem;
- checks, rota e motivos do gate;
- estado completo da LLM;
- confirmações profissionais.

Anexos continuam restritos a nome do exame, grupo MIME, tamanho, tipo de entrada
e `local_only=true`. Bytes, imagem, PDF, URL de preview e base64 não entram no
registro.

## Compatibilidade

`DecisionMedReasoning`, `DecisionMedRouting`, `DecisionMedSequences`,
`DecisionMedCases.buildSuite()` e os endpoints existentes permanecem
inalterados. O PsychRx não é modificado; seu baseline é apenas executado no CI.
