# DM-002 — SpecialtyPack Resolver

## Objetivo

Carregar um `SpecialtyPack` registrado, verificar suas capacidades estruturais
e devolver um resultado rastreável sem executar raciocínio clínico.

## Entrada

- `SpecialtyPackRegistry`;
- chave canônica da especialidade;
- catálogo de `CapabilityBinding` versionados.

## Saída

`SpecialtyLoadResult` contém:

- pacote resolvido;
- estado de composição;
- bindings encontrados;
- capacidades ausentes;
- razões de bloqueio;
- `trace_id`;
- propriedade `clinical_execution_allowed`, sempre falsa nesta missão.

## Estados

| Estado | Significado |
| --- | --- |
| `blocked` | composição incompleta ou pacote retirado |
| `reference_only` | pacote disponível apenas para inspeção e validação |
| `ready_for_validation` | composição presente, ainda bloqueada pelo gate clínico futuro |

## Fluxo

```text
SpecialtyPackRegistry
  -> SpecialtyPackResolver
    -> verificar capacidades obrigatórias
    -> vincular descritores versionados
    -> produzir trace_id e razões explícitas
    -> manter execução clínica bloqueada
```

## Psiquiatria

O pacote de Psiquiatria resolve os sete descritores estruturais definidos na
DM-001: snapshot, safety, evidence, reasoning, explanation, monitoring e audit.
O resultado permanece `reference_only`.

## Limites

- nenhum import do `psychrx-baseline`;
- nenhum paciente ou dado clínico como entrada;
- nenhum medicamento, diagnóstico ou estratégia como saída;
- nenhuma chamada a motor clínico;
- nenhuma integração com interface, banco ou rede;
- nenhuma autorização de execução clínica.

## Arquivos permitidos

- `decisionmed/composition.py`;
- `decisionmed/__init__.py`;
- `tests/test_composition.py`;
- `docs/adr/DM-002_SAFE_SPECIALTY_RESOLUTION.md`;
- `docs/DM-002_SPECIALTY_PACK_RESOLVER.md`.

Qualquer outro arquivo permanece proibido.

## Critérios de aceite

- Psiquiatria carregada como `reference_only`;
- bindings versionados e imutáveis;
- capacidade ausente bloqueia o resultado;
- pacote retirado bloqueia o resultado;
- pacote ativo continua dependente de validação futura;
- `trace_id` presente;
- nenhuma saída clínica;
- testes novos e regressões aprovados.

## Rollback

Reverter o commit da DM-002. A DM-001 permanece utilizável sem o resolver.
