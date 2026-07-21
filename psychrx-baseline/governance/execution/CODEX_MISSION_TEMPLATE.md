# Codex Mission Template

Use este template para toda missao futura enviada ao Codex no projeto PsychRx.

Regra geral: toda missao deve alterar o menor numero possivel de arquivos.

Regra clinica: nenhuma missao pode introduzir nova entidade clinica sem atualizar a Ontologia.

Regra cientifica: nenhuma missao pode introduzir regra terapeutica sem fonte cientifica rastreavel.

---

# Missao

Descrever em uma frase clara o que o Codex deve entregar.

Exemplo:

Criar o documento `docs/NOME_DO_DOCUMENTO.md` definindo [tema] sem implementar software.

# Contexto

Informar o contexto necessario para executar a missao.

Incluir, quando aplicavel:

- documentos oficiais relacionados;
- decisoes arquiteturais ja tomadas;
- limites clinicos;
- relacao com dominio, conhecimento, evidencia, seguranca ou interface;
- o que deve ser preservado.

# Arquivos permitidos

Listar exatamente quais arquivos podem ser criados, alterados ou removidos.

Exemplo:

- `docs/NOME_DO_DOCUMENTO.md`

Regra: se um arquivo nao estiver listado aqui, ele deve ser considerado fora do escopo.

# Arquivos proibidos

Listar arquivos ou pastas que nao podem ser alterados.

Exemplo:

- `domain/`
- `knowledge/`
- `evidence/`
- `interfaces/`
- qualquer arquivo nao listado em "Arquivos permitidos"

# O que fazer

Listar tarefas objetivas.

Exemplo:

- criar o documento solicitado;
- incluir secoes obrigatorias;
- manter linguagem conceitual;
- preservar separacao entre conhecimento, raciocinio, seguranca e interface;
- registrar limites e criterios de aceite.

# O que nao fazer

Listar proibicoes especificas.

Exemplo:

- nao escrever codigo;
- nao implementar APIs;
- nao criar motores;
- nao escolher tecnologia;
- nao criar banco de dados;
- nao prescrever;
- nao criar recomendacao clinica automatica;
- nao misturar conhecimento cientifico com algoritmo;
- nao alterar arquivos fora do escopo.

# Criterios de aceite

Definir como saber que a missao foi concluida.

Exemplo:

- arquivo criado no caminho correto;
- todas as secoes obrigatorias presentes;
- nenhuma alteracao fora do escopo;
- nenhuma dependencia proibida adicionada;
- nenhuma regra terapeutica sem fonte rastreavel;
- nenhuma nova entidade clinica sem atualizacao da Ontologia;
- documentacao coerente com os documentos oficiais do PsychRx.

# Testes obrigatorios

Definir verificacoes obrigatorias.

Exemplo:

- verificar existencia do arquivo criado;
- verificar cabecalhos obrigatorios;
- verificar ausencia de codigo quando a missao for documental;
- verificar que arquivos proibidos nao foram alterados;
- executar testes existentes quando houver implementacao;
- justificar testes nao executados.

# Riscos arquiteturais

Listar riscos que o Codex deve evitar.

Exemplo:

- misturar dominio com aplicacao;
- misturar conhecimento com algoritmo;
- permitir interface decidir conduta;
- criar regra clinica sem fonte;
- criar entidade clinica fora da Ontologia;
- duplicar conceito existente;
- reduzir rastreabilidade;
- reduzir explicabilidade;
- ampliar escopo sem autorizacao.

# Rollback

Descrever como desfazer a missao se necessario.

Exemplo:

- remover o arquivo criado;
- restaurar versao anterior do documento alterado;
- reverter somente os arquivos listados em "Arquivos permitidos";
- registrar se rollback exigir revisao manual.

# Saida esperada

Descrever como o Codex deve responder ao final.

Exemplo:

Informar:

- arquivo criado ou alterado;
- resumo objetivo da entrega;
- testes ou verificacoes executadas;
- arquivos fora do escopo preservados;
- riscos restantes, se houver.

---

# Template Copiavel

```text
Voce esta trabalhando no projeto PsychRx.

Missao:
[Descrever a entrega em uma frase clara.]

Contexto:
[Informar documentos, limites e decisoes ja existentes que devem ser respeitados.]

Arquivos permitidos:
- [arquivo ou pasta permitida]

Arquivos proibidos:
- [arquivo ou pasta proibida]
- qualquer arquivo nao listado em "Arquivos permitidos"

O que fazer:
- [tarefa 1]
- [tarefa 2]
- [tarefa 3]

O que nao fazer:
- nao escrever codigo, se a missao for documental;
- nao criar motores;
- nao criar recomendacoes automaticas;
- nao alterar arquivos fora do escopo;
- nao misturar conhecimento cientifico com algoritmo;
- nao introduzir nova entidade clinica sem atualizar a Ontologia;
- nao introduzir regra terapeutica sem fonte cientifica rastreavel.

Criterios de aceite:
- [criterio 1]
- [criterio 2]
- [criterio 3]

Testes obrigatorios:
- verificar existencia dos arquivos criados ou alterados;
- verificar cabecalhos ou secoes obrigatorias;
- verificar que arquivos proibidos nao foram alterados;
- executar testes existentes quando houver implementacao;
- justificar testes nao executados.

Riscos arquiteturais:
- [risco 1]
- [risco 2]
- [risco 3]

Rollback:
- [como desfazer a alteracao]

Saida esperada:
- informar arquivos criados ou alterados;
- resumir a entrega;
- informar verificacoes executadas;
- informar riscos restantes, se houver.

Regras obrigatorias:
- alterar o menor numero possivel de arquivos;
- nenhuma nova entidade clinica sem atualizacao da Ontologia;
- nenhuma regra terapeutica sem fonte cientifica rastreavel.
```
