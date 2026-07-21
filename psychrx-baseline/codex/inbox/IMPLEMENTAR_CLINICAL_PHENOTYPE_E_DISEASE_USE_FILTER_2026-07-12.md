# MISSÃO — Implementar Clinical Phenotype Filter + Disease Use Filter no PsychRx

## Objetivo

Implementar no aplicativo, de ponta a ponta, uma camada clínica que permita ao motor funcionar tanto:

1. quando existe diagnóstico definido; quanto
2. quando ainda não existe diagnóstico, mas há um quadro clínico/síndrome predominante.

A entrega deve ficar funcional no app, integrada ao ranking, à justificativa clínica, aos quatro quadros da interface e aos testes.

## Contexto confirmado pela auditoria

A base atual possui:

- 46 medicamentos na matriz farmacológica;
- 46 medicamentos com `Dose - efeito`;
- 46 medicamentos com `Uso por doença`;
- 249 linhas de uso por doença/contexto;
- fontes mapeadas no perfil `Dose - efeito`;
- 172 testes atualmente aprovados.

Problema atual:

> `Uso por doença` é exibido como explicação, mas ainda não funciona como filtro forte de elegibilidade antes do ranking.

Além disso, o app precisa continuar útil quando o diagnóstico ainda não estiver fechado, usando o quadro clínico predominante sem inventar diagnóstico.

---

# 1. Novo fluxo obrigatório

Implementar o fluxo:

```text
Dados clínicos
↓
Detecção do quadro/fenótipo predominante
↓
Existe diagnóstico definido?
├── SIM → Clinical Phenotype Filter + Disease Use Filter
└── NÃO → Clinical Phenotype Filter + regras de segurança para diagnóstico incerto
↓
Definição do papel terapêutico permitido
↓
Filtros de contraindicação e segurança
↓
Ranking farmacológico somente entre candidatos elegíveis
↓
Exibição nos quatro quadros
↓
Dose–efeito + Uso por doença/quadro + fontes
```

O sistema não deve escolher primeiro e justificar depois. Os filtros devem agir antes do ranking final.

---

# 2. Clinical Phenotype Filter

Criar uma camada explícita chamada, preferencialmente:

```text
ClinicalPhenotypeFilter
```

Ela deve identificar, a partir dos dados já coletados pelo app, um ou mais fenótipos/síndromes clínicas, sem afirmar diagnóstico definitivo.

## Fenótipos mínimos

- `DEPRESSIVE_SYNDROME`
- `ANXIOUS_SYNDROME`
- `MANIFORM_SYNDROME`
- `PSYCHOTIC_SYNDROME`
- `OBSESSIVE_COMPULSIVE_SYNDROME`
- `AGITATION_SYNDROME`
- `INSOMNIA_PREDOMINANT`
- `COGNITIVE_SYNDROME`
- `SUBSTANCE_WITHDRAWAL_OR_USE_SYNDROME`
- `UNSPECIFIED_OR_INSUFFICIENT_DATA`

A nomenclatura pode ser adaptada ao padrão existente, mas deve ser centralizada e testável.

## Regras essenciais

1. Não converter fenótipo em diagnóstico automaticamente.
2. Permitir mais de um fenótipo, com um principal e secundários.
3. Registrar quais dados sustentaram a classificação.
4. Quando houver dados insuficientes, devolver `UNSPECIFIED_OR_INSUFFICIENT_DATA`.
5. Não recomendar antidepressivo em monoterapia quando houver fenótipo maniforme relevante ou suspeita bipolar não esclarecida.
6. Não tratar insônia isolada como indicação automática para antipsicótico.
7. Não tratar sedação como sinônimo de indicação formal.

## Saída sugerida

```python
PhenotypeAssessment(
    primary_phenotype=...,
    secondary_phenotypes=[...],
    supporting_features=[...],
    confidence=...,
    warnings=[...],
)
```

---

# 3. Disease Use Filter

Criar uma camada explícita chamada, preferencialmente:

```text
DiseaseUseFilter
```

Ela deve usar os dados existentes de `Uso por doença` para definir elegibilidade antes do ranking.

## Papéis terapêuticos mínimos

- `PRIMARY_TREATMENT`
- `AUGMENTATION`
- `ADJUVANT`
- `MAINTENANCE`
- `RELAPSE_PREVENTION`
- `OFF_LABEL_WITH_EVIDENCE`
- `LIMITED_EVIDENCE`
- `RESTRICTED`
- `NOT_RECOMMENDED`
- `NO_MAPPING`

## Regra de elegibilidade

- `NOT_RECOMMENDED` → excluir do ranking.
- `RESTRICTED` → excluir por padrão; permitir apenas se o contexto clínico e os pré-requisitos específicos estiverem explicitamente presentes.
- `AUGMENTATION` → não apresentar como substituição simples ou monoterapia principal.
- `MAINTENANCE` → não priorizar para episódio agudo sem papel agudo mapeado.
- `RELAPSE_PREVENTION` → não confundir com tratamento agudo.
- `OFF_LABEL_WITH_EVIDENCE` → permitir somente com sinalização clara e prioridade inferior às opções aprovadas/recomendadas, salvo justificativa explícita.
- `LIMITED_EVIDENCE` → rebaixar fortemente e sinalizar.
- `NO_MAPPING` → não presumir compatibilidade; excluir ou manter fora do ranking principal com aviso de ausência de mapeamento.
- `PRIMARY_TREATMENT` → elegível para ranking principal.
- `ADJUVANT` → elegível apenas quando a estratégia solicitada for associação/adjuvância.

---

# 4. Quando não houver diagnóstico

O app deve continuar funcionando com base no quadro clínico, mas de forma conservadora.

## Comportamento esperado

### Sem diagnóstico definido, mas com síndrome depressiva

O motor pode considerar medicamentos compatíveis com tratamento de síndrome depressiva, porém deve:

- sinalizar que o diagnóstico ainda não está fechado;
- verificar sinais de mania/hipomania, psicose, uso de substâncias, causas médicas e risco suicida;
- não afirmar `transtorno depressivo maior`;
- não usar automaticamente `Uso por doença` como se houvesse doença confirmada;
- aplicar somente medicamentos cujo papel seja compatível com o fenótipo e com o nível de incerteza.

### Sem diagnóstico definido, mas com síndrome maniforme

- bloquear antidepressivo em monoterapia no ranking principal;
- priorizar avaliação diagnóstica e segurança;
- permitir somente opções compatíveis com controle de mania/agitação, se todos os demais dados clínicos necessários estiverem presentes;
- deixar explícito que se trata de manejo orientado por síndrome, não de diagnóstico confirmado.

### Sem diagnóstico e com dados insuficientes

- não produzir recomendação farmacológica específica;
- solicitar/indicar os dados clínicos ausentes;
- exibir saída segura: `dados insuficientes para ranking farmacológico confiável`.

---

# 5. Estratégia terapêutica deve ser definida antes do medicamento

Criar ou consolidar um campo de estratégia clínica, por exemplo:

- `KEEP_CURRENT`
- `OPTIMIZE_DOSE`
- `SWITCH_MONOTHERAPY`
- `AUGMENT`
- `ADD_ADJUVANT`
- `TAPER_OR_STOP`
- `NO_DRUG_RECOMMENDATION`

O ranking só pode avaliar medicamentos compatíveis com a estratégia.

Exemplos:

- Se a estratégia for `SWITCH_MONOTHERAPY`, excluir medicamentos mapeados apenas como potencializadores.
- Se a estratégia for `AUGMENT`, excluir medicamentos sem papel de potencialização/adjuvância.
- Se a estratégia for `KEEP_CURRENT`, não gerar linguagem contraditória de troca.

Eliminar contradições como:

```text
Ação: substituir
Justificativa: ainda é possível otimizar
```

A saída deve ter uma única estratégia principal, podendo registrar alternativas secundárias separadamente.

---

# 6. Integração com o ranking

A ordem deve ser:

```text
1. estratégia terapêutica
2. fenótipo clínico
3. doença/fase, quando existente
4. papel terapêutico permitido
5. segurança/contraindicações
6. adequação ao perfil sintomático
7. ranking final
```

O ranking deve receber apenas candidatos elegíveis ou receber uma estrutura com estado explícito:

```python
MedicationEligibility(
    medication=...,
    eligible=True/False,
    therapeutic_role=...,
    exclusion_reason=...,
    penalty=...,
    evidence_status=...,
)
```

Não usar somente pontuação negativa para situações que exigem bloqueio clínico.

---

# 7. Interface — quatro quadros

Manter quatro quadros claros e sem texto concatenado.

## Quadro 1 — Decisão clínica

Mostrar:

- estratégia principal;
- se o raciocínio foi por diagnóstico ou por fenótipo;
- grau de incerteza quando não houver diagnóstico.

Exemplo:

```text
DECISÃO CLÍNICA
Substituição em monoterapia
Base: síndrome depressiva; diagnóstico ainda não confirmado
```

## Quadro 2 — Por que

Mostrar apenas os fatores decisivos:

- adesão;
- tempo de uso;
- resposta;
- tolerabilidade;
- fenótipo predominante;
- alertas relevantes.

## Quadro 3 — Estratégia/medicamento elegível

Mostrar:

- medicamento sugerido;
- papel terapêutico;
- motivo de elegibilidade;
- principais exclusões relevantes, quando útil.

Exemplo:

```text
Sertralina
Papel: tratamento principal compatível com síndrome depressiva
```

Não mostrar potencializador como substituto simples.

## Quadro 4 — Objetivo e segurança

Mostrar:

- alvos clínicos;
- principais cuidados;
- necessidade de confirmação diagnóstica;
- monitorização essencial.

## Blocos complementares

Após os quatro quadros, manter:

- faixa terapêutica;
- dose–efeito;
- uso por doença ou uso por quadro/fenótipo;
- fontes.

Quando não houver diagnóstico, o título deve ser:

```text
Uso por quadro clínico
```

Não exibir uma doença como confirmada.

---

# 8. Explicabilidade obrigatória

Para cada medicamento exibido, informar:

- `por que foi incluído`;
- `qual papel terapêutico possui`;
- `qual dado clínico sustentou a compatibilidade`;
- `se o uso é aprovado, recomendado por diretriz, off-label, restrito ou de evidência limitada`;
- `fonte correspondente`.

Para medicamentos excluídos, registrar internamente e permitir auditoria de:

- papel incompatível;
- doença incompatível;
- fenótipo incompatível;
- fase incompatível;
- contraindicação;
- ausência de mapeamento;
- uso restrito;
- evidência insuficiente.

Não é necessário poluir a tela principal com todos os excluídos, mas a decisão deve ser rastreável.

---

# 9. Compatibilidade com a base dos 46 medicamentos

Não remover nem reduzir os dados existentes.

Garantir:

- 46 medicamentos preservados;
- `Dose - efeito` preservado;
- `Uso por doença` preservado;
- fontes preservadas;
- formulações relacionadas corretamente tratadas, sem confundir princípio ativo e formulação;
- nenhum dado inventado para preencher lacunas.

Bupropiona/Bupropiona XL, Venlafaxina/Venlafaxina XR e Valproato/Divalproato devem manter distinções farmacocinéticas/formulação, mas sem serem interpretados como mecanismos totalmente diferentes.

---

# 10. Testes obrigatórios

Manter os 172 testes atuais aprovados e criar testes adicionais cobrindo, no mínimo:

1. diagnóstico definido + tratamento principal elegível;
2. diagnóstico definido + potencializador não pode aparecer como substituto simples;
3. manutenção não pode ser priorizada indevidamente em fase aguda;
4. `NOT_RECOMMENDED` é excluído;
5. `RESTRICTED` é excluído sem pré-requisito;
6. `OFF_LABEL_WITH_EVIDENCE` aparece sinalizado e rebaixado;
7. ausência de mapeamento não gera compatibilidade inventada;
8. síndrome depressiva sem diagnóstico permite fluxo conservador;
9. síndrome maniforme sem diagnóstico bloqueia antidepressivo em monoterapia;
10. dados insuficientes retornam `NO_DRUG_RECOMMENDATION`;
11. estratégia `AUGMENT` aceita potencializadores e rejeita substitutos inadequados;
12. estratégia `SWITCH_MONOTHERAPY` rejeita medicamentos apenas de potencialização;
13. interface mostra quatro quadros sem concatenação de rótulos/valores;
14. interface diferencia `Uso por doença` de `Uso por quadro clínico`;
15. fontes continuam visíveis e vinculadas ao conteúdo exibido;
16. não há contradição entre decisão, estratégia e justificativa.

Executar:

```bash
python -m unittest discover -s tests -t .
```

Registrar total final de testes e resultado.

---

# 11. Auditoria de implementação

Ao concluir, gerar relatório em:

```text
docs/decision_support_engine/CLINICAL_PHENOTYPE_DISEASE_FILTER_IMPLEMENTATION.md
```

O relatório deve conter:

- arquivos alterados;
- fluxo anterior e fluxo novo;
- classes/funções criadas;
- regras de bloqueio;
- regras de rebaixamento;
- como funciona sem diagnóstico;
- como funciona com diagnóstico;
- exemplos reais de entrada e saída;
- testes adicionados;
- total de testes aprovados;
- limitações remanescentes;
- screenshots ou descrição objetiva dos quatro quadros no app.

---

# 12. Critérios de aceitação

A missão só está concluída quando:

- o app estiver funcionando com o novo fluxo;
- o ranking usar efetivamente o filtro antes de selecionar medicamentos;
- houver fluxo seguro sem diagnóstico definido;
- o app não inventar diagnóstico;
- potencializador não aparecer como substituto simples;
- medicamentos não recomendados/restritos forem bloqueados corretamente;
- as quatro caixas estiverem coerentes;
- Dose–efeito, Uso por doença/quadro e fontes continuarem visíveis;
- todos os testes antigos e novos passarem;
- o relatório de implementação for criado;
- a alteração for commitada no repositório.

## Restrições

- Não fazer apenas mock visual.
- Não implementar apenas texto explicativo na interface.
- Não deixar o filtro apenas como pontuação decorativa.
- Não alterar dados farmacológicos ou fontes sem justificativa documentada.
- Não afirmar diagnóstico quando houver apenas quadro/fenótipo.
- Não liberar recomendação específica com dados clínicos insuficientes.
