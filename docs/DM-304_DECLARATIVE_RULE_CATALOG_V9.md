# DM-304 — Catálogo declarativo de regras v9

O schema `9.0.0` acrescenta `clinical-rules.json` ao pacote externo governado.
As versões `7.0.0` e `8.0.0` continuam legíveis para preservar catálogos e
testes anteriores.

Cada regra declara:

- ID e versão;
- módulo clínico de destino;
- efeito qualitativo;
- força qualitativa;
- expressão recursiva `all`, `any` e `none`;
- racional;
- fontes;
- estado e metadados de revisão.

Os predicados disponíveis nesta etapa são `equals`, `contains`,
`contains_any`, `contains_all`, `count_at_least`, `matches` e `present`.
Nenhum operador produz probabilidade numérica.

O manifesto v9 inclui a contagem de regras e o hash SHA-256 do novo arquivo. O
loader rejeita regra duplicada, módulo ausente, fonte ausente, campos
desconhecidos, expressão inválida, contagem divergente ou hash incorreto.

Regras `draft` e `in_review` podem ser usadas apenas para demonstração
auditável do protótipo. Elas nunca autorizam diagnóstico, prescrição ou
conduta clínica automática.

