# 015 - Biblioteca Cientifica

## 1. Objetivo

Este documento define a organizacao oficial da Biblioteca Cientifica do PsychRx.

A Biblioteca Cientifica e o conjunto governado de fontes que sustenta conhecimento, evidencias, alertas, restricoes, comparacoes, explicacoes e futuras decisoes clinicas dentro do projeto.

Este documento nao descreve nem aborda implementacao tecnica, banco de dados, APIs, software ou algoritmos. Ele define criterios cientificos, organizacionais e de governanca.

## 2. Proposito

O proposito da Biblioteca Cientifica e impedir que o PsychRx utilize conhecimento clinico sem fonte, sem revisao, sem hierarquia, sem versionamento ou sem rastreabilidade.

Ela deve garantir que toda informacao cientifica usada pelo sistema possa ser ligada a:

- fonte;
- ano;
- tipo de evidencia;
- qualidade;
- forca da recomendacao;
- aplicabilidade clinica;
- conflitos conhecidos;
- data de revisao;
- status.

## 3. Diretrizes Clinicas

Diretrizes clinicas sao documentos produzidos por sociedades cientificas, instituicoes ou grupos especializados com metodologia explicita.

Na Biblioteca Cientifica, diretrizes devem registrar:

- instituicao responsavel;
- ano;
- versao;
- escopo;
- populacao-alvo;
- metodologia;
- grau de recomendacao quando disponivel;
- principais recomendacoes;
- limites de aplicabilidade;
- conflitos ou divergencias com outras diretrizes.

Diretrizes devem orientar padroes gerais, mas nao substituir contexto individual do paciente.

## 4. Revisoes Sistematicas

Revisoes sistematicas sintetizam a literatura a partir de pergunta definida, busca estruturada e criterios explicitos.

Devem registrar:

- pergunta de pesquisa;
- estrategia de busca;
- periodo pesquisado;
- criterios de inclusao e exclusao;
- estudos incluidos;
- avaliacao de qualidade;
- conclusoes;
- limitacoes;
- aplicabilidade clinica.

Revisoes sistematicas devem ter prioridade quando o objetivo for compreender corpo de evidencia sobre uma pergunta clinica.

## 5. Meta-analises

Meta-analises combinam quantitativamente resultados de estudos.

Devem registrar:

- estudos incluidos;
- populacao;
- comparadores;
- desfechos;
- tamanho de efeito;
- heterogeneidade;
- risco de vies;
- analises de subgrupo;
- limitacoes;
- aplicabilidade ao contexto do PsychRx.

Meta-analises de baixa qualidade ou alta heterogeneidade devem ter sua forca reduzida.

## 6. Ensaios Clinicos

Ensaios clinicos sao fontes primarias relevantes para eficacia, seguranca, tolerabilidade e comparacao de intervencoes.

Devem registrar:

- desenho do estudo;
- tamanho da amostra;
- populacao;
- criterios de inclusao e exclusao;
- comparador;
- intervencao;
- duracao;
- desfechos primarios;
- desfechos secundarios;
- eventos adversos;
- conflitos de interesse;
- aplicabilidade ao paciente real.

Ensaios clinicos devem ser interpretados considerando diferenca entre ambiente controlado e pratica clinica.

## 7. Livros-texto

Livros-texto podem ser usados para fundamentos, definicoes, farmacologia, fisiopatologia, organizacao conceitual e contexto historico.

Devem registrar:

- titulo;
- autores ou editores;
- edicao;
- ano;
- capitulo;
- topico;
- escopo da afirmacao;
- relacao com evidencias mais recentes.

Livros-texto nao devem prevalecer sobre evidencia recente de alta qualidade quando houver conflito clinicamente relevante.

## 8. Consensos

Consensos sao documentos produzidos por grupos de especialistas quando a evidencia e limitada, heterogenea ou insuficiente.

Devem registrar:

- grupo responsavel;
- participantes;
- metodologia de consenso;
- grau de concordancia;
- escopo;
- recomendacoes;
- areas de incerteza;
- limitacoes;
- conflitos de interesse.

Consenso deve ser claramente diferenciado de evidencia robusta.

## 9. Documentos Regulatorios

Documentos regulatorios incluem normas, alertas, bulas oficiais, aprovacoes, restricoes e comunicados de agencias reguladoras.

Devem registrar:

- orgao emissor;
- jurisdicao;
- data;
- status vigente;
- conteudo regulatorio;
- implicacao clinica;
- restricoes de uso;
- advertencias;
- diferencas entre jurisdicoes quando relevantes.

Documentos regulatorios possuem peso especial em seguranca clinica.

## 10. Criterios de Inclusao

Uma fonte so deve entrar na Biblioteca Cientifica quando atender criterios minimos.

Criterios obrigatorios:

- identificacao clara da fonte;
- ano;
- tipo de evidencia;
- relevancia para psicofarmacologia, psiquiatria clinica, seguranca, monitorizacao ou estabilizacao;
- qualidade avaliavel;
- escopo definido;
- aplicabilidade clinica descrita;
- limitacoes registradas;
- status atribuido;
- data de revisao interna.

Fontes sem identificacao, sem ano, sem tipo de evidencia ou sem aplicabilidade clinica nao devem ser consideradas prontas para uso.

## 11. Versionamento

Toda fonte e toda interpretacao cientifica derivada devem possuir versao.

O versionamento deve permitir responder:

- quando a fonte foi adicionada;
- qual versao estava vigente em determinada analise;
- se a fonte foi revisada;
- se foi substituida;
- se foi depreciada;
- quais documentos ou relacoes dependiam dela;
- qual impacto a atualizacao produziu.

Status possiveis devem seguir a politica de rastreabilidade cientifica:

- `draft`;
- `awaiting validation`;
- `validated`;
- `deprecated`;
- `conflicting evidence`.

## 12. Atualizacao

A Biblioteca Cientifica deve ser atualizada de forma governada.

Gatilhos de atualizacao:

- nova diretriz;
- nova revisao sistematica;
- nova meta-analise;
- novo ensaio clinico relevante;
- alerta regulatorio;
- mudanca de bula;
- nova evidencia de seguranca;
- identificacao de conflito;
- revisao periodica;
- depreciacao de fonte anterior.

Toda atualizacao deve registrar:

- motivo;
- fonte nova ou revisada;
- fonte afetada;
- impacto sobre conhecimento;
- impacto sobre seguranca;
- impacto sobre explicabilidade;
- impacto sobre documentos relacionados;
- data de revisao;
- responsavel pela curadoria.

## 13. Rastreabilidade

Toda informacao cientifica deve ser rastreavel ate sua fonte.

A rastreabilidade minima deve conectar:

```text
afirmacao clinica
  -> fonte
  -> ano
  -> tipo de evidencia
  -> qualidade
  -> forca da recomendacao
  -> status
  -> data de revisao
  -> aplicabilidade clinica
```

Sem rastreabilidade, a informacao nao deve sustentar regra terapeutica, alerta, estrategia ou explicacao.

## 14. Resolucao de Conflitos

Conflitos entre fontes devem ser documentados, nao escondidos.

Conflitos podem ocorrer por:

- populacoes diferentes;
- metodos diferentes;
- desfechos diferentes;
- qualidade metodologica divergente;
- recomendacoes divergentes;
- diferencas regulatorias;
- mudanca temporal da evidencia;
- conflitos de interesse;
- aplicabilidade limitada.

A resolucao deve considerar:

- hierarquia da evidencia;
- qualidade metodologica;
- atualidade;
- seguranca clinica;
- aplicabilidade ao paciente;
- consistencia com outras fontes;
- gravidade do risco;
- transparencia sobre incerteza.

Quando o conflito nao puder ser resolvido, a fonte ou relacao deve receber status `conflicting evidence`.

## 15. Governanca Cientifica

Governanca cientifica define como fontes entram, permanecem, mudam ou saem da Biblioteca Cientifica.

Ela deve garantir:

- criterios de inclusao claros;
- revisao critica;
- classificacao por tipo e qualidade;
- versionamento;
- rastreabilidade;
- registro de conflitos;
- controle de status;
- revisao periodica;
- separacao entre evidencia e algoritmo;
- documentacao das decisoes de curadoria.

Nenhuma fonte deve ser incorporada como conhecimento oficial sem passar por curadoria minima.

## 16. Relacao com Outros Documentos

A Biblioteca Cientifica se relaciona com:

- `014_EVIDENCE_GRAPH.md`, que define como evidencias sustentam decisoes;
- `EVIDENCE_TRACEABILITY_POLICY.md`, que define metadados obrigatorios;
- `CLINICAL_SAFETY_CONTRACT.md`, que exige fonte para alertas e restricoes;
- `011_KNOWLEDGE_GRAPH.md`, que reutiliza conhecimento estruturado;
- `013_CONSTRAINT_GRAPH.md`, que depende de evidencias para restricoes;
- `031_DOMAIN_MODEL.md`, que define `EvidenceSource`;
- `051_DOMAIN_IMPLEMENTATION_SPEC.md`, que especifica contratos futuros.

## 17. Limites

A Biblioteca Cientifica:

- nao prescreve;
- nao decide conduta;
- nao substitui julgamento medico;
- nao implementa software;
- nao e banco de dados;
- nao resolve sozinha conflitos clinicos;
- nao transforma evidencia populacional em decisao individual;
- nao deve conter conhecimento sem fonte.

Sua funcao e sustentar raciocinio clinico com conhecimento cientifico organizado, revisavel e rastreavel.

## 18. Declaracao Final

A Biblioteca Cientifica do PsychRx e a base governada do conhecimento cientifico do projeto.

Ela organiza diretrizes, revisoes sistematicas, meta-analises, ensaios clinicos, livros-texto, consensos e documentos regulatorios para que toda informacao clinica possa ser rastreada, revisada, atualizada e interpretada em contexto.

No PsychRx, conhecimento sem fonte nao e conhecimento oficial. Evidencia sem rastreabilidade nao pode sustentar decisao. Governanca cientifica e condicao para seguranca clinica.
