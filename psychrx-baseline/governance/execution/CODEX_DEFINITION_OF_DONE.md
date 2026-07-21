# Codex Definition of Done

## 1. Proposito

Este documento define quando uma missao do Codex no projeto PsychRx pode ser considerada concluida.

Ele e uma regra obrigatoria para todas as proximas missoes. Nenhuma entrega deve ser tratada como finalizada apenas porque arquivos foram criados ou alterados. Uma missao so esta concluida quando atende ao objetivo, respeita o escopo, preserva a arquitetura, nao viola seguranca clinica e deixa rastreabilidade suficiente para revisao.

## 2. Regra Principal

Toda missao futura do Codex deve conter, antes ou durante sua execucao:

1. objetivo claro;
2. escopo limitado;
3. arquivos permitidos;
4. arquivos proibidos;
5. criterios de aceite;
6. testes esperados;
7. impacto arquitetural;
8. riscos;
9. rollback possivel;
10. documentacao atualizada.

Se algum desses itens estiver ausente, a missao deve ser considerada incompleta ou precisa ser explicitamente limitada.

## 3. Objetivo Claro

Uma missao deve declarar o que precisa ser entregue.

O objetivo deve responder:

- qual documento, modulo, ajuste ou validacao sera produzido;
- qual problema sera resolvido;
- qual resultado esperado deve existir ao final;
- o que nao faz parte da entrega.

Objetivos vagos devem ser refinados antes de qualquer alteracao relevante.

## 4. Escopo Limitado

Toda missao deve ter fronteiras claras.

O escopo deve definir:

- quais pastas podem ser tocadas;
- quais tipos de alteracao sao permitidos;
- quais responsabilidades estao dentro da missao;
- quais responsabilidades pertencem a outra missao;
- quais temas clinicos, tecnicos ou documentais devem ficar fora.

Alteracoes oportunistas, refatoracoes nao solicitadas e expansoes de escopo nao devem ser feitas sem nova autorizacao.

## 5. Arquivos Permitidos

A missao deve declarar ou inferir com clareza quais arquivos podem ser criados, alterados ou removidos.

Arquivos permitidos devem estar diretamente relacionados ao objetivo.

Quando a missao for documental, os arquivos permitidos devem se limitar aos documentos solicitados e, se necessario, indices ou relatorios explicitamente relacionados.

Quando a missao for arquitetural, deve respeitar os contratos de camadas e dependencias.

## 6. Arquivos Proibidos

A missao deve indicar arquivos ou pastas que nao podem ser alterados.

Mesmo quando nao houver lista explicita, sao proibidas alteracoes em:

- arquivos fora do escopo;
- documentos oficiais nao relacionados;
- fontes cientificas sem motivo;
- camadas arquiteturais nao envolvidas;
- dados sensiveis;
- configuracoes globais sem necessidade;
- qualquer arquivo cuja alteracao nao possa ser justificada pela missao.

Alterar arquivo proibido torna a missao incompleta ate que a violacao seja corrigida ou explicitamente aprovada.

## 7. Criterios de Aceite

Toda missao deve ter criterios verificaveis de aceite.

Os criterios podem incluir:

- arquivo criado no caminho correto;
- secoes obrigatorias presentes;
- conteudo alinhado aos documentos oficiais;
- nenhuma implementacao quando a missao for conceitual;
- nenhuma recomendacao clinica automatica;
- nenhuma dependencia proibida;
- rastreabilidade preservada;
- testes executados ou justificativa para nao execucao.

Uma entrega sem criterio de aceite nao deve ser considerada finalizada.

## 8. Testes Esperados

Toda missao deve declarar quais testes ou verificacoes sao esperados.

Podem incluir:

- testes automatizados existentes;
- verificacao de estrutura de arquivos;
- verificacao de links ou referencias;
- validacao de cabecalhos obrigatorios;
- busca por dependencias proibidas;
- revisao de separacao entre camadas;
- checagem de ausencia de conteudo clinico indevido;
- validacao de rastreabilidade.

Se testes nao forem executados, a resposta final deve explicar por que.

## 9. Impacto Arquitetural

Toda missao deve avaliar impacto arquitetural.

Perguntas obrigatorias:

- a alteracao respeita as camadas oficiais?
- cria nova dependencia?
- altera responsabilidade de alguma pasta?
- mistura conhecimento, raciocinio, seguranca, interface ou aplicacao?
- afeta rastreabilidade?
- afeta explicabilidade?
- cria precedente arquitetural?

Impactos arquiteturais relevantes devem ser documentados.

## 10. Riscos

Toda missao deve identificar riscos proporcionais ao seu escopo.

Riscos possiveis:

- quebrar testes existentes;
- alterar arquivo errado;
- duplicar conceito ja existente;
- criar inconsistencia documental;
- misturar conhecimento com algoritmo;
- introduzir logica clinica sem governanca;
- reduzir explicabilidade;
- enfraquecer seguranca;
- criar dependencia proibida;
- gerar recomendacao sem rastreabilidade.

Riscos devem ser mitigados antes de declarar conclusao.

## 11. Rollback Possivel

Toda missao deve permitir algum caminho de reversao.

Rollback pode significar:

- remover documento criado;
- restaurar conteudo anterior;
- desfazer alteracao em arquivo especifico;
- reverter nova dependencia;
- retornar a versao anterior de uma regra documental;
- registrar que a reversao exige intervencao manual.

Se rollback nao for simples, isso deve ser declarado.

## 12. Documentacao Atualizada

Toda missao que altera arquitetura, dominio, conhecimento, evidencia, seguranca, raciocinio, interface, testes ou governanca deve atualizar a documentacao correspondente.

Nao basta alterar comportamento ou estrutura. O PsychRx exige que mudancas relevantes sejam explicaveis e rastreaveis documentalmente.

Documentacao deve indicar:

- o que mudou;
- por que mudou;
- qual escopo foi afetado;
- quais limites permanecem;
- quais proximos passos existem, se aplicavel.

## 13. Quando uma Missao Esta Concluida

Uma missao esta concluida quando:

- objetivo foi atendido;
- escopo foi respeitado;
- arquivos permitidos foram os unicos alterados;
- arquivos proibidos permaneceram intactos;
- criterios de aceite foram cumpridos;
- testes esperados foram executados ou justificados;
- impacto arquitetural foi considerado;
- riscos foram avaliados;
- rollback e possivel ou documentado;
- documentacao esta atualizada;
- nenhuma regra arquitetural obrigatoria foi violada.

## 14. Quando uma Missao Nao Esta Concluida

Uma missao nao esta concluida se:

- quebrou testes existentes;
- alterou arquivos fora do escopo;
- misturou conhecimento com algoritmo;
- criou logica clinica nao documentada;
- criou recomendacao sem rastreabilidade;
- adicionou dependencia proibida;
- removeu explicabilidade;
- ocultou incerteza clinica relevante;
- criou prescricao automatica;
- violou separacao entre camadas;
- deixou arquivo corrompido ou ilegivel;
- removeu fonte cientifica sem justificativa;
- criou comportamento sem criterio de aceite;
- nao informou testes nao executados;
- deixou rollback impossivel sem documentar.

Qualquer item acima bloqueia a conclusao da missao.

## 15. Checklist Obrigatorio para Codex

Antes de finalizar, Codex deve verificar:

- O objetivo foi cumprido?
- O escopo foi respeitado?
- Somente arquivos permitidos foram alterados?
- Nenhum arquivo proibido foi alterado?
- Os criterios de aceite foram satisfeitos?
- Os testes ou verificacoes esperados foram executados?
- Falhas de teste foram informadas?
- O impacto arquitetural foi considerado?
- Nao houve dependencia proibida?
- Conhecimento e algoritmo permanecem separados?
- Interface nao decidiu conduta clinica?
- Explicabilidade foi preservada?
- Rastreabilidade foi preservada?
- Rollback e possivel ou documentado?
- Documentacao foi atualizada?

## 16. Regra para Pull Requests

Todo Pull Request futuro deve poder apontar para esta Definition of Done.

Um PR nao deve ser aprovado se:

- nao declara objetivo e escopo;
- altera arquivos sem justificativa;
- viola camadas;
- mistura evidencia cientifica com logica executavel;
- enfraquece seguranca;
- remove rastreabilidade;
- remove explicabilidade;
- nao informa testes;
- nao atualiza documentacao quando necessario.

Esta Definition of Done deve ser usada como criterio de revisao, nao como sugestao opcional.

## 17. Declaracao Final

No PsychRx, uma missao do Codex so termina quando entrega valor dentro do escopo, preserva arquitetura, respeita seguranca clinica, mantem conhecimento separado de algoritmo, conserva rastreabilidade e deixa o projeto mais claro do que estava antes.

Concluir nao e apenas modificar arquivos. Concluir e deixar uma mudanca verificavel, reversivel, documentada e coerente com a arquitetura clinica do PsychRx.
