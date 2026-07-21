# A03-001 - SSRI Scientific Content Population Planning

## Objetivo

Planejar o Program A03 - Scientific Content Population: SSRIs sem publicar conteudo cientifico ainda.

O Program A03 e o primeiro programa que pretende adicionar conteudo cientifico real a Base Oficial de Conhecimento. Por isso, sua execucao exige um gate mais rigoroso que os programas A01 e A02.

## Decisao de Execucao

A populacao cientifica completa dos SSRIs nao esta desbloqueada neste momento.

Motivo:

- o repositorio nao contem corpus local autorizado de Stahl, Maudsley, APA, CANMAT, NICE, WFSBP, FDA, EMA, ANVISA, Cochrane e PubMed;
- nao ha registro de revisor editorial humano atribuido;
- nao ha aprovacao cientifica por campo;
- nao ha pacote de fontes versionado;
- nao ha validacao semantica final para cada afirmacao clinica;
- nao ha publication checklist aprovado.

## Escopo Desbloqueado

Nesta missao, ficam autorizados apenas:

- plano de populacao;
- matriz de fontes candidatas;
- template de rastreabilidade por campo;
- gate editorial;
- bloqueio formal de publicacao ate validacao.

## Escopo Bloqueado

Permanecem bloqueados:

- preenchimento integral de Fluoxetine;
- preenchimento integral de Sertraline;
- preenchimento integral de Paroxetine;
- preenchimento integral de Citalopram;
- preenchimento integral de Escitalopram;
- preenchimento integral de Fluvoxamine;
- qualquer recomendacao terapeutica;
- qualquer posologia como orientacao assistencial;
- qualquer publicacao no Knowledge Layer;
- qualquer consumo pelo Evidence Runtime.

## Ordem de Populacao Aprovada

1. Fluoxetine
2. Sertraline
3. Paroxetine
4. Citalopram
5. Escitalopram
6. Fluvoxamine

## Requisitos por Campo

Cada campo devera conter:

- fonte;
- ano;
- tipo de evidencia;
- qualidade da evidencia;
- forca da recomendacao, quando aplicavel;
- data de revisao;
- status;
- conflitos conhecidos;
- aplicabilidade clinica;
- trace id;
- knowledge version;
- semantic version;
- editorial reviewer;
- editorial decision.

## Status Inicial dos Medicamentos

```text
Fluoxetine   - registered, not_populated, not_validated, not_published
Sertraline   - registered, not_populated, not_validated, not_published
Paroxetine   - registered, not_populated, not_validated, not_published
Citalopram   - registered, not_populated, not_validated, not_published
Escitalopram - registered, not_populated, not_validated, not_published
Fluvoxamine  - registered, not_populated, not_validated, not_published
```

## Condicao para Desbloquear A03-002

A populacao de Fluoxetine so podera iniciar quando houver:

- pacote de fontes aceito;
- referencias oficiais registradas;
- revisor editorial definido;
- criterio de extracao por campo aprovado;
- template de traceabilidade preenchivel;
- decisao explicita de que o conteudo sera `draft` ate validacao.

## Declaracao Final

O Program A03 foi iniciado apenas como planejamento e gate de seguranca cientifica. Nenhum conteudo cientifico real foi publicado.

