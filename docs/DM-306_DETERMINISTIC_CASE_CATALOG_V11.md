# DM-306 — Catálogo determinístico de 4.500 casos (v11)

O schema `11.0.0` acrescenta `clinical-cases.json` ao pacote governado. O
arquivo contém exatamente 15 casos sintéticos por módulo, totalizando 4.500.

## Distribuição obrigatória por módulo

- 3 casos típicos;
- 2 atípicos;
- 2 com red flag;
- 2 imitadores;
- 2 com comorbidade;
- 2 contraditórios;
- 2 com reavaliação pós-exame.

Cada caso preserva narrativa, fatos selecionados, detalhes positivos, rota
esperada e obtida, perguntas abertas, classificação inicial, diferenciais,
exame físico, exames complementares, reavaliação, impressão esperada, eventos
de auditoria e hash SHA-256.

Os casos são fixtures determinísticas de qualidade. Não representam pacientes,
não validam o conteúdo clínico e nunca liberam diagnóstico, prescrição ou
conduta automática.
