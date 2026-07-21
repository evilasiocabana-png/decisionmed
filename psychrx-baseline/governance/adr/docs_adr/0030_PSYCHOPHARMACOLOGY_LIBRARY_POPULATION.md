# ADR 0030 - Psychopharmacology Library Population

## Status

Accepted

## Contexto

A Official Scientific Knowledge Base foi criada no Program A01. O proximo passo e preparar a populacao da biblioteca de psicofarmacos sem adicionar conteudo cientifico ainda.

## Decisao

Criar `scientific_knowledge/psychopharmacology/` para contratos, templates, referencias, workflow editorial, gates, catalogos, integracao, auditoria e replay de pacotes farmacologicos.

## Alternativas Consideradas

- popular SSRIs diretamente com conteudo cientifico;
- usar `knowledge_library/` sem camada especifica;
- criar regras terapeuticas junto com metadados.

## Justificativa

A separacao permite revisar estrutura, identidade, versionamento e rastreabilidade antes de inserir conhecimento cientifico real.

## Impacto

O PsychRx passa a ter SSRI Package e SSRI Catalog metadata-only, prontos para populacao no Program A03.

## Riscos

- confundir registro de nome com conteudo cientifico;
- publicar pacote nao validado;
- usar catalogo metadata-only como fonte assistencial.

## Criterios de Revisao Futura

- primeira populacao cientifica real de SSRI;
- revisao editorial completa;
- integracao com Evidence Runtime apos validacao;
- auditoria do primeiro pacote publicado.

