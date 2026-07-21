# 645 - Apresentacao explicita do alvo residual

## Objetivo

Evitar que a expressao `alvo residual` apareca como se fosse um dado clinico ja demonstrado quando o caso informa apenas sintomas atuais e uma resposta global parcial.

## Regra aplicada

- Em resposta parcial com sintomas informados, o PsychRx mostra: `Alvo residual ainda nao confirmado longitudinalmente` e lista os sintomas atuais que precisam ser verificados como persistentes.
- Em resposta parcial sem sintomas informados, o PsychRx mostra: `Alvo residual nao definido` e solicita o registro dos sintomas ou prejuizos persistentes e do impacto funcional.
- A expressao isolada `alvo residual` nao sustenta troca ou associacao. Antes dessa discussao, a saida exige revisar tempo, adesao, tolerabilidade, prejuizo funcional e confirmar longitudinalmente o que permaneceu.
- A interface apenas apresenta a explicacao produzida pela camada Application; ela nao classifica sintomas como residuais.

## Base arquitetural

- `docs/008_CLINICAL_OPERATING_MIND.md`: incerteza deve ser declarada antes de certeza falsa.
- `docs/009_CLINICAL_SNAPSHOT.md`: sintomas atuais pertencem ao estado do momento e precisam ser comparados com snapshots anteriores.
- `docs/022_LONGITUDINAL_REASONING.md`: a evolucao deve registrar o que mudou, melhorou, piorou ou permaneceu.
- `docs/051_DOMAIN_IMPLEMENTATION_SPEC.md`: um sintoma pode ter curso residual, mas esse estado nao deve ser inferido automaticamente pela interface.

## Fonte clinica oficial de apoio

- NICE NG222, recomendacoes 1.9.1 a 1.9.5: diante de resposta ausente ou limitada, revisar fatores explicativos, adesao, tempo adequado, diagnostico e necessidades clinicas antes de decidir em conjunto por aumento, troca ou outra estrategia: https://www.nice.org.uk/guidance/ng222/chapter/recommendations

## Testes obrigatorios

- resposta parcial com sintomas lista os sintomas atuais como itens a confirmar longitudinalmente;
- resposta parcial sem sintomas declara `Alvo residual nao definido`;
- Motor 2 nao usa mais `Revisar alvo residual` como justificativa suficiente;
- interface nao contem as frases antigas `tratar alvo residual` ou `checar tempo, alvo residual`.
