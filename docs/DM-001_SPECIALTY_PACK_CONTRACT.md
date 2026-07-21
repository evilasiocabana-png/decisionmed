# DM-001 — Contrato SpecialtyPack

## Objetivo

Definir a menor fundação executável que permite ao DecisionMEd reconhecer
especialidades sem incorporar conhecimento clínico ou lógica terapêutica ao
núcleo da plataforma.

## Contrato

Cada `SpecialtyPack` declara:

| Campo | Responsabilidade |
| --- | --- |
| `key` | identidade canônica e estável da especialidade |
| `display_name` | nome destinado à apresentação |
| `version` | versão semântica do manifesto |
| `workflow_contract` | fluxo clínico governado que o pacote pretende usar |
| `safety_contract` | gate de segurança obrigatório |
| `evidence_policy` | política de evidência e rastreabilidade |
| `knowledge_namespace` | origem lógica do conhecimento versionado |
| `audit_namespace` | namespace da trilha de auditoria |
| `required_capabilities` | capacidades que precisam existir antes da ativação |
| `status` | `reference_only`, `active` ou `retired` |

O contrato é imutável após criação. O registro recusa chaves duplicadas e torna
explícita a ausência de uma especialidade requerida.

## Pacote inicial

Psiquiatria é o primeiro pacote registrado:

```text
key: psychiatry
version: 0.1.0
status: reference_only
origem arquitetural: PsychRx
```

O estado `reference_only` significa que o manifesto pode ser inspecionado e
validado, mas não autoriza uso clínico nem execução de conduta.

## Fluxo de composição

```text
SpecialtyPackRegistry
  -> SpecialtyPack
    -> workflow contract
    -> safety contract
    -> evidence policy
    -> knowledge namespace
    -> audit namespace
```

O registro não chama motores, não consulta pacientes e não apresenta
estratégias. Uma camada de aplicação futura deverá resolver os contratos e
manter a ordem clínica oficial: paciente, snapshot, segurança, evidência,
raciocínio, explicação, monitorização e auditoria.

## Limites obrigatórios

- não contém medicamento, dose, indicação ou recomendação;
- não cria diagnóstico ou estratégia terapêutica;
- não consulta interface ou dashboard;
- não substitui Safety, Evidence, Reasoning ou Audit;
- não ativa automaticamente um pacote recém-registrado;
- não altera `psychrx-baseline/`.

## Arquivos da missão

- `decisionmed/__init__.py`;
- `decisionmed/specialties.py`;
- `tests/test_specialties.py`;
- `docs/adr/DM-001_SPECIALTY_PACK_COMPOSITION.md`;
- `docs/DM-001_SPECIALTY_PACK_CONTRACT.md`.

Qualquer arquivo não listado permaneceu fora do escopo.

## Critérios de aceite

- contrato imutável e validado;
- versionamento semântico obrigatório;
- identificadores canônicos obrigatórios;
- registry determinístico;
- duplicidade e ausência explícitas por erro;
- Psiquiatria registrada como `reference_only`;
- segurança, evidência e auditoria declaradas;
- nenhum conteúdo clínico hardcoded;
- testes novos e regressão do baseline aprovados.
