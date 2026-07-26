# DM-307 — Gate de curadoria do lote essencial de 50

## Escopo verificável

O primeiro lote é definido de forma determinística pelos 50 primeiros módulos
do catálogo mestre, na ordem governada. Ele cobre 23 módulos de cardiologia,
20 de pneumologia e sete de neurologia. A ordem é estável porque o gerador
reproduz o mesmo catálogo antes de produzir conteúdo e casos.

No segmento cardiológico, os módulos de síndrome coronariana aguda, doença
coronariana crônica, fibrilação atrial, insuficiência cardíaca, síncope,
bradiarritmia, dissecção aórtica e choque cardiogênico também recebem fontes
oficiais candidatas específicas; os demais mantêm a biblioteca oficial da
especialidade até a seleção da seção aplicável.

## O que este gate comprova

- cada um dos 50 módulos tem conteúdo `partial` e `draft`;
- cada pergunta discriminadora e cada exame complementar do lote tem ao menos
  uma fonte oficial **candidata** vinculada;
- a fonte do campo também é uma fonte do respectivo módulo;
- nenhuma dessas ligações abre execução clínica, prescrição ou conduta
  automática.

O verificador é `DecisionMEd-Knowledge/validate_essential_50_curation.py`.
Ele aceita os lotes determinísticos `--count 50`, `--count 150` e
`--count 300`; o nome foi preservado por compatibilidade. O workflow
`validate-catalog` do repositório de conhecimento executa os três marcos junto
com a validação do manifesto e com o robô dos 4.500 casos, usando os contratos
da plataforma baixados no próprio CI.

## O que este gate não comprova

Ele não comprova que uma fonte sustenta a redação exata de cada campo, nem que
um critério, exame, escala, tratamento ou destino seja clinicamente validado.
Cada entrada continua exigindo, antes de mudar para `validated`:

1. seção e versão exatas da fonte;
2. confirmação de população e cenário de uso;
3. revisão humana identificada;
4. prazo de nova revisão;
5. teste de regressão e caso clínico revisado.

Assim, o gate aumenta rastreabilidade para a curadoria sem transformar uma
ligação de fonte em recomendação clínica.

## Fila de revisão humana

`DecisionMEd-Knowledge/curation/dm300-review-queue.json` contém uma entrada
determinística para cada módulo. Ela agrupa os primeiros 50, os primeiros 150
e o catálogo completo de 300, registra fontes candidatas, contagem de campos e
sete verificações obrigatórias. Todos os 300 itens permanecem
`pending_human_review`, sem revisor ou data atribuídos, e com execução clínica
bloqueada. `validate_dm300_review_queue.py` impede que a fila se desalinhe do
catálogo governado ou que um item seja marcado como aprovado sem a governança
humana correspondente.
