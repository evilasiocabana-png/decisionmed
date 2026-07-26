# DM-300 — Missão de execução do catálogo clínico

## Objetivo

Construir, integrar e validar a arquitetura para 300 módulos de raciocínio
clínico no DecisionMEd, preservando o que já funciona, sem alterar o PsychRx
original e sem apresentar conteúdo em rascunho como clinicamente validado.

O alvo é de **300 módulos clínicos**, não 300 rótulos artificialmente chamados
de síndrome. Cada módulo deve declarar seu tipo ontológico real.

## Resultado esperado

Ao final da missão, o DecisionMEd deverá:

- carregar um catálogo governado com exatamente 300 módulos;
- usar o mesmo núcleo nas portas Assistido, Direto e Investigação;
- conduzir entrevista progressiva por cliques;
- manter terminologia técnica, versionada e auditável;
- organizar diferenciais, exame físico e exames complementares;
- permitir reavaliação pós-exames e registro da conduta profissional;
- gerar e executar 15 casos determinísticos por módulo, totalizando 4.500;
- bloquear execução clínica de conteúdo não validado;
- apresentar relatório real de arquitetura, conteúdo e validação.

## Restrições obrigatórias

1. Não modificar `C:\Users\evcab\PsychRx`.
2. Não apagar, reverter ou sobrescrever mudanças existentes no worktree.
3. Manter IDs internos estáveis para preservar casos e auditorias anteriores.
4. Separar motor, interface e conteúdo clínico.
5. Respeitar a fronteira existente com o `DecisionMEd-Knowledge`.
6. Não criar referências, critérios, recomendações ou níveis de evidência
   inexistentes.
7. Usar fontes oficiais ou primárias, com versão, ano e localizador.
8. Não mostrar probabilidades numéricas sem modelo calibrado e validado.
9. Conteúdo `draft` ou `in_review` pode ser demonstrado, mas não pode liberar
   prescrição ou conduta automática.
10. Toda mudança clínica deve ser rastreável até módulo, regra, versão e fonte.

## Fase 0 — Baseline e inventário

- Inventariar as 14 entradas atuais, seus IDs, nomes, regras e dependências.
- Mapear conteúdo ainda escrito diretamente em `intake-reasoning.js`.
- Registrar testes, rotas, schemas, auditoria, anexos e estado do catálogo
  externo antes da migração.
- Identificar mudanças locais existentes e preservar todas.
- Documentar como os registros antigos continuarão reproduzíveis.

### Aceite

- Inventário versionado.
- Baseline de testes registrado.
- Matriz `ID atual → entidade nova → estratégia de migração`.
- Nenhum ID antigo quebrado.

## Fase 1 — Ontologia clínica

Cada objeto deverá declarar:

- `id` imutável;
- versão semântica;
- nome oficial e nome de exibição;
- sinônimos e abreviações;
- `entity_type`;
- especialidade principal e especialidades relacionadas;
- manifestação, fenótipo e entidade pai;
- população e cenário assistencial;
- códigos terminológicos quando aplicáveis e licenciados;
- relações com síndromes, diagnósticos e condições de risco;
- status `draft`, `in_review`, `validated` ou `retired`;
- fontes e metadados de revisão.

Tipos mínimos:

- `manifestation`;
- `clinical_presentation`;
- `initial_syndrome`;
- `standardized_syndrome`;
- `diagnosis`;
- `risk_condition`;
- `clinical_context`.

“Síndrome torácica aguda” permanece como síndrome clínica inicial interna. Ela
não substitui as hipóteses diagnósticas padronizadas.

## Fase 2 — Catálogo mestre de 300 módulos

Criar exatamente 300 IDs únicos, sem duplicar a mesma entidade em
especialidades diferentes.

Distribuição inicial de planejamento:

| Área | Quantidade |
| --- | ---: |
| Cardiologia | 25 |
| Pneumologia | 20 |
| Neurologia | 25 |
| Gastroenterologia e hepatologia | 25 |
| Nefrologia e urologia | 20 |
| Endocrinologia e metabolismo | 20 |
| Infectologia | 25 |
| Reumatologia | 20 |
| Hematologia | 15 |
| Dermatologia | 15 |
| Psiquiatria | 20 |
| Ginecologia | 15 |
| Obstetrícia | 15 |
| Pediatria | 20 |
| Ortopedia, emergência e trauma | 20 |
| **Total** | **300** |

A distribuição pode ser ajustada para evitar duplicação, desde que o total
permaneça 300 e a justificativa seja registrada.

### Aceite

- 300 IDs únicos.
- Nenhum nome duplicado sem relação explícita.
- Contagem por tipo e especialidade.
- Sinônimos não criam módulos duplicados.
- Todos começam com status honesto.

## Fase 3 — Pacote externo de conhecimento

Implementar:

- manifesto de release;
- arquivos por especialidade e módulo;
- registro central de fontes;
- hashes SHA-256;
- versões de schema e motor compatíveis;
- dependências entre módulos;
- data de revisão e vencimento;
- loader seguro no DecisionMEd.

O loader deve falhar fechado quando houver:

- manifesto inválido;
- hash divergente;
- schema incompatível;
- ID duplicado;
- referência ausente;
- dependência inexistente;
- tentativa de execução clínica de módulo não validado.

Assets do motor e catálogo precisam de versão explícita para impedir mistura de
arquivos antigos e novos no navegador.

## Fase 4 — Contrato de cada módulo

Cada módulo deverá conter, quando aplicável:

1. definição e limites;
2. manifestações obrigatórias;
3. manifestações frequentes;
4. manifestações atípicas;
5. achados contrários;
6. fatores de risco;
7. red flags;
8. critérios de interrupção e encaminhamento;
9. hipóteses principais;
10. graves que não podem ser perdidos;
11. imitadores;
12. perguntas discriminadoras e justificativas;
13. exame físico orientado;
14. exames complementares, pergunta clínica, indicação e momento;
15. limitações dos exames;
16. critérios diagnósticos e escalas;
17. reavaliação pós-exames;
18. impressão diagnóstica profissional;
19. conduta de segurança;
20. tratamento inicial e definitivo, sujeitos aos gates;
21. destino, retorno e acompanhamento;
22. referências, evidência e governança.

## Fase 5 — Motor de regras compartilhado

Substituir blocos clínicos repetitivos por regras declarativas contendo:

- ID da regra;
- fatos de entrada;
- operadores `all`, `any` e `none`;
- efeito `support`, `oppose`, `alarm` ou `route`;
- força qualitativa;
- racional clínico;
- referências;
- versão e estado de validação.

Reutilizar motores transversais para dor, dispneia, febre, sangramento, déficit
neurológico, consciência, sintomas urinários, lesões cutâneas e outros padrões.

O motor deve:

- preservar múltiplas hipóteses quando o quadro for ambíguo;
- nunca classificar apenas pela localização da dor;
- reconhecer equivalentes clínicos;
- abrir somente perguntas capazes de mudar segurança ou diferenciação;
- aceitar texto leigo como sinal auxiliar;
- exigir confirmação por clique dos fatos extraídos do texto;
- explicar por que cada pergunta foi aberta;
- registrar todas as regras disparadas.

## Fase 6 — Três portas de entrada

### Assistido

Triagem → anamnese geral → revisão → módulos progressivos → classificação
clínica → diferenciais → discriminadores → exame físico → exames →
reavaliação → impressão → conduta.

### Direto

Busca ou escolha da entidade → triagem → critérios presentes, ausentes e
contrários → diferenciais → exames → reavaliação → impressão → conduta.

### Investigação

Seleção de duas ou três hipóteses → comparação → discriminadores → exames →
efeito dos resultados → reclassificação.

A interface deverá mostrar nome, tipo, versão, especialidade, status e fontes.
Também deverá oferecer busca, filtros e carregamento progressivo.

## Fase 7 — População em camadas

### Lote 1

Completar e integrar 50 módulos essenciais.

### Lote 2

Expandir para 150 após corrigir as lacunas encontradas no primeiro lote.

### Lote 3

Completar os 300 módulos.

O esqueleto dos 300 pode ser criado de uma vez. A mudança de `draft` para
`validated` exige conteúdo completo, fontes e revisão humana registrada.

## Fase 8 — Gerador e robô de cobertura

Gerar exatamente 15 casos por módulo:

- 3 típicos;
- 2 atípicos;
- 2 com red flags ou condições que não podem ser perdidas;
- 2 imitadores;
- 2 com comorbidades;
- 2 contraditórios;
- 2 com reavaliação pós-exames.

Total: **4.500 casos determinísticos**.

Cada caso deverá registrar:

- narrativa inicial;
- respostas selecionadas;
- detalhes positivos;
- rotas esperadas e obtidas;
- perguntas abertas;
- classificação inicial;
- diferenciais;
- exame e exames complementares;
- resultado pós-exame;
- impressão esperada;
- auditoria completa e hash.

O robô deverá produzir contador, progresso, falhas reproduzíveis e relatório de
cobertura por módulo, tipo e especialidade. A narrativa e os cliques não podem
ser contraditórios.

## Fase 9 — Testes e segurança

- Validar schemas, manifests, hashes, IDs, versões e referências.
- Testar loader, regras, roteamento, discriminadores, segurança, anexos,
  reavaliação, auditoria e gates.
- Cobrir casos típicos, atípicos, negativos, equivalentes, contraditórios,
  sobrepostos e emergenciais.
- Manter todos os testes atuais aprovados.
- Validar visualmente no Chrome as três portas e casos representativos.
- Medir desempenho com 300 módulos sem carregar tudo desnecessariamente.

## Relatório final obrigatório

Separar os percentuais de:

- arquitetura;
- catálogo cadastrado;
- conteúdo preenchido;
- referências vinculadas;
- revisão clínica;
- testes automatizados;
- validação visual;
- prontidão clínica real.

Não usar um único percentual que misture estrutura pronta com conteúdo ainda
não revisado.

## Critérios de conclusão

- Exatamente 300 módulos tipados e sem IDs duplicados.
- Motor independente de 300 blocos hardcoded.
- Catálogo externo validado por manifesto e hashes.
- Três portas usando o mesmo núcleo.
- Contrato completo para cada módulo.
- 4.500 casos determinísticos auditáveis.
- Testes existentes e novos aprovados.
- Nome, tipo, versão, status e fontes visíveis.
- Conteúdo não validado bloqueado para execução clínica.
- Documentação de arquitetura, migração, governança e limitações.
- Resumo final com resultados, testes e bloqueios reais.

## Ordem mais eficiente

Executar nesta ordem:

1. baseline;
2. ontologia;
3. catálogo mestre;
4. pacote externo e loader;
5. motor declarativo;
6. migração dos 14 módulos atuais;
7. lote de 50;
8. validação;
9. expansão para 150;
10. validação;
11. expansão para 300;
12. execução dos 4.500 casos e relatório final.

Não interromper apenas porque a missão é extensa. Continuar enquanto existir
trabalho seguro, verificável e dentro do escopo.
