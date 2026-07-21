# DM-032 — Escopo e exclusões no manifesto da especialidade

## Objetivo

Fazer cada `SpecialtyPack` declarar seu uso pretendido e seus usos excluídos,
sem manter descrições específicas das especialidades dentro do frontend.

## Contrato

O manifesto imutável agora exige:

- `intended_scope`: descrição não vazia e governada do escopo atual;
- `excluded_uses`: coleção não vazia e sem duplicatas dos usos não autorizados.

Esses metadados são expostos pela API de estado. A página inicial monta os
cartões usando os valores do manifesto e apresenta as exclusões de forma
expansível.

## Segurança

A renderização foi migrada de interpolação HTML para criação de nós com
`textContent`. Assim, futuros textos de manifesto não são interpretados como
marcação executável. Os escopos atuais são estruturais ou de referência; todos
excluem diagnóstico, classificação de risco, recomendação de conduta e execução
clínica.

## Limites

Escopo declarado não equivale a validação científica ou regulatória. Conteúdo
clínico permanece no catálogo externo e os gates de execução continuam fechados.
