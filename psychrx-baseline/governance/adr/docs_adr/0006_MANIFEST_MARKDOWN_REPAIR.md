# ADR 0006 - Manifest Markdown Repair

## ID da Decisao

ADR-0006

## Data

2026-06-30

## Status

Aceita

## Contexto

O arquivo `docs/000_MANIFEST.md` existia com extensao Markdown, mas apresentava conteudo binario de Word ao ser lido como texto. Isso impedia leitura, revisao, rastreabilidade e uso do manifesto como fonte oficial em fluxos do Codex.

O usuario solicitou explicitamente a atualizacao do manifesto do projeto.

## Decisao

Preservar o arquivo binario anterior como:

```text
docs/000_MANIFEST_BINARY_BACKUP_20260630.md
```

Criar um novo `docs/000_MANIFEST.md` em Markdown legivel, atualizado com o estado atual do PsychRx.

O novo manifesto preserva os principios fundamentais ja estabelecidos:

- paciente no centro;
- medico como decisor final;
- seguranca antes de estrategia;
- nenhuma prescricao automatica;
- conhecimento separado do algoritmo;
- rastreabilidade e explicabilidade obrigatorias.

## Alternativas Consideradas

1. Manter o arquivo binario como estava.
2. Criar um segundo manifesto com outro nome e deixar o oficial ilegivel.
3. Preservar backup do binario e recriar o manifesto oficial em Markdown legivel.

A alternativa 3 foi escolhida porque o arquivo oficial precisa ser legivel, versionavel e utilizavel por revisoes futuras.

## Justificativa

Um manifesto oficial corrompido ou ilegivel compromete governanca, revisao arquitetural e continuidade do projeto. A conversao para Markdown reestabelece o manifesto como fonte primaria acessivel.

## Impacto

- `docs/000_MANIFEST.md` passa a ser legivel em Markdown.
- O manifesto passa a refletir Roadmap Enterprise, Localhost App e Clinical Experience Layer.
- A versao binaria anterior fica preservada como backup.
- A atualizacao fica rastreada por ADR.

## Riscos

- Possivel divergencia entre o conteudo binario anterior e o novo manifesto textual.
- Necessidade futura de recuperar conteudo original se houver copia externa.

## Mitigacao

A nova versao referencia os documentos fundadores, ADRs e documentos posteriores. A decisao foi registrada explicitamente nesta ADR e o arquivo anterior foi preservado.

## Documentos Afetados

- `docs/000_MANIFEST.md`
- `docs/000_MANIFEST_BINARY_BACKUP_20260630.md`
- `docs/adr/0006_MANIFEST_MARKDOWN_REPAIR.md`

## Criterios de Revisao Futura

Revisar esta ADR se:

- surgir uma versao textual anterior do manifesto;
- houver decisao de renumerar documentos fundadores;
- for criada politica formal de reparo de arquivos binarios com extensao `.md`.

## Declaracao Final

O manifesto oficial do PsychRx foi reparado e atualizado como Markdown legivel, preservando a seguranca clinica, a rastreabilidade e a governanca arquitetural do projeto.
