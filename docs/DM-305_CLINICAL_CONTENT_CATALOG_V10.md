# DM-305 — Catálogo de conteúdo clínico v10

O schema `10.0.0` acrescenta `clinical-content.json` ao pacote externo. O
primeiro lote contém os 14 conteúdos parciais migrados do protótipo, ligados
aos seus IDs do catálogo DM-300.

O contrato comporta:

- definição e limites;
- manifestações, fatores de risco, red flags e critérios de interrupção;
- três grupos de diagnóstico diferencial;
- perguntas discriminadoras;
- exame físico;
- exames complementares com pergunta clínica, momento e limitações;
- critérios, reavaliação pós-exames, conduta de segurança, tratamento,
  destino, retorno e acompanhamento;
- fontes, versão, estado e revisão.

Nesta migração, somente os campos que já existiam no protótipo foram
transportados. Campos ausentes permaneceram vazios, sem preenchimento
inventado. Os 14 registros são `partial` e `draft`.

O loader v10 verifica hash, contagem, IDs, referências de módulo e fontes,
campos exatos, perguntas, exames e metadados. A interface consome o conteúdo
externo e mantém o conteúdo antigo apenas como fallback de compatibilidade.
Nenhum registro autoriza execução clínica automática.

