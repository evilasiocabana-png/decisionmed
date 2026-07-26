# DM-303 — Progresso verificável da missão DM-300

Data da medição: 2026-07-26.

Este documento registra um ponto intermediário. Ele não declara a missão
DM-300 concluída e não apresenta os 300 esqueletos como conteúdo clínico
validado.

O consolidado de arquitetura, conteúdo, referências, revisão e prontidão está
em [DM-308](DM-308_DM300_READINESS_REPORT.md).

## Resultado alcançado

- baseline versionado das 14 classificações legadas e das baterias anteriores;
- ontologia com sete tipos clínicos e estados separados de terminologia,
  conteúdo e revisão;
- catálogo externo com exatamente 300 IDs únicos;
- pacote de catálogo v11 com manifesto, hashes SHA-256 e validação fechada;
- loader compatível com os catálogos v7 a v10 anteriores e obrigatório para os
  oito arquivos do catálogo v11;
- 14 chaves legadas preservadas e ligadas a IDs governados;
- API e tela de catálogo com busca, filtros e carregamento progressivo;
- três portas atuais usando o mesmo catálogo governado de 300 entradas, com
  busca e seleção exata nas portas Direto e Investigação;
- ID, nome, tipo, versão, status e fontes adicionados à apresentação e à
  auditoria do formulário;
- motor genérico de expressões `all`, `any` e `none`;
- 50 regras declarativas carregadas do pacote externo: 30 de rota, oito de
  suporte diferencial e 12 de segurança;
- condicionais de diferenciação e segurança retiradas de
  `intake-reasoning.js`; cada disparo registra regra, módulo, versão, força,
  racional e fontes;
- 300 contratos estruturais `partial` em `clinical-content.json`, preservando
  os 14 conteúdos anteriores e mantendo os demais como rascunho gerado;
- 4.500 casos determinísticos, 15 por módulo, com sequência de eventos e hash
  de auditoria;
- robô DM-300 executado sem falhas estruturais nos 4.500 casos;
- todos os 300 módulos permanecem `draft`, com execução clínica automática
  bloqueada.

## Medidas atuais

| Dimensão | Medida objetiva | Progresso honesto |
| --- | --- | ---: |
| Arquitetura DM-300 | baseline, ontologia, schemas v11, manifesto, loader, API, identidade, conteúdo, casos, motor declarativo e três portas integrados | 90% |
| Catálogo cadastrado | 300/300 identidades tipadas | 100% |
| Conteúdo preenchido | 300/300 contratos estruturais `partial`; 14/300 preservam curadoria anterior; 0/300 completos | 100% estrutural; 4,7% com curadoria anterior; 0% completo |
| Referências vinculadas | 300/300 com ao menos uma fonte oficial candidata; as 901 perguntas e os 898 exames têm fonte candidata em cada campo; sustentação de campo ainda não revisada | 100% descoberta e ligação candidata; 0% validação de campo concluída |
| Regras declarativas | 50 regras: 30 `route`, oito `support`, 12 `alarm`; nenhuma validada clinicamente | 100% da migração das condicionais atuais |
| Relações explícitas | 3/300 módulos atualmente ligados a pai ou relacionados | 1,0% |
| Terminologia revisada | 0/300; todas as entradas ainda são candidatas | 0% |
| Revisão clínica humana | 0/300 módulos revisados ou validados | 0% |
| Casos exigidos | 4.500/4.500 casos determinísticos; robô estrutural sem falhas | 100% estrutural; não valida precisão clínica |
| Testes automatizados da base atual | 273 Python + 28 JavaScript aprovados | 100% da bateria atual |
| Validação visual desta fase | três portas e catálogo verificados no Chrome na v10; formulário v0.18 validado no navegador integrado, incluindo fontes por campo, anexos, conduta e gates | 90% |
| Prontidão clínica real | conteúdo não revisado, sem autorização de execução | 0% |

Os percentuais não devem ser somados nem transformados em um único percentual.

## Distribuição das 300 identidades

### Por tipo

- 18 contextos clínicos;
- 82 apresentações clínicas;
- 11 síndromes iniciais;
- 40 síndromes padronizadas;
- 143 diagnósticos;
- 6 condições de risco.

### Por especialidade principal

| Especialidade | Quantidade |
| --- | ---: |
| Cardiologia | 23 |
| Dermatologia | 13 |
| Emergência | 12 |
| Endocrinologia | 18 |
| Gastroenterologia | 17 |
| Ginecologia | 13 |
| Hematologia | 13 |
| Hepatologia | 5 |
| Infectologia | 22 |
| Clínica médica | 9 |
| Nefrologia | 9 |
| Neurologia | 22 |
| Obstetrícia | 13 |
| Oftalmologia | 12 |
| Ortopedia | 13 |
| Pediatria | 18 |
| Psiquiatria | 18 |
| Pneumologia | 18 |
| Reumatologia | 18 |
| Trauma | 5 |
| Urologia | 9 |
| **Total** | **300** |

A distribuição difere da estimativa inicial porque separa emergência, trauma,
oftalmologia, clínica médica e hepatologia e evita cadastrar a mesma entidade
em mais de uma especialidade.

## Validação executada

- `python -m unittest discover -s tests -p 'test_*.py'`: 273 testes aprovados;
- `node --test tests/intake_routing.test.cjs`: 28 testes aprovados;
- validação do catálogo externo: `300` módulos, `50` regras, `300` conteúdos e
  `4.500` casos carregados;
- `validate_dm300_cases.py`: 4.500 casos aprovados, zero falhas;
- `validate_essential_50_curation.py --count 50|150|300`: os três marcos
  passaram; no lote completo, 901 perguntas e 898 exames têm fonte candidata
  e execução bloqueada;
- `benchmark_dm300_load.py`: mediana local abaixo de 1 s em três cargas completas
  do catálogo governado (300 módulos, 50 regras e 4.500 casos); o gate de CI
  falha apenas acima de 10 s para detectar regressão técnica grosseira;
- `curation/dm300-review-queue.json`: 300/300 módulos em fila auditável de
  revisão humana, todos `pending_human_review` e bloqueados para execução;
- CI do pacote de conhecimento executa a validação do catálogo, o robô dos
  4.500 casos e o gate de fontes por campo dos 50 módulos prioritários;
- sintaxe dos quatro arquivos JavaScript do formulário validada;
- scripts embutidos de `index.html`, `catalog.html` e `intake.html` validados;
- schemas JSON e manifesto v11 lidos sem erro;
- `git diff --check` sem erros de whitespace.

## Próximo gate

O próximo gate não é mais de engenharia básica. A fonte candidata de cada
pergunta e exame do lote essencial já está vinculada, mas falta substituir
conteúdo transversal gerado por critérios e recomendações específicos, ligar
cada campo à seção exata da fonte e obter revisão humana identificada. Depois,
repetir a revisão para 150 e 300. Até esse gate, os 300 módulos permanecem
visíveis como rascunho e bloqueados para prescrição, tratamento ou conduta
automática.
