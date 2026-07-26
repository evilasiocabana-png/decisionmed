# DM-308 — Relatório de prontidão DM-300

Medição: 2026-07-26. Este é um relatório de estado verificável, não um aceite
clínico nem declaração de conclusão da missão DM-300.

## Resumo executivo

O DecisionMEd possui a infraestrutura governada para 300 módulos, as três
portas integradas e a cobertura sintética exigida. O catálogo está tecnicamente
íntegro, mas o conteúdo clínico continua em rascunho e não tem revisão humana
identificada. Portanto, a prontidão clínica real é zero e o bloqueio de
prescrição, tratamento e conduta automática deve permanecer ativo.

## Percentuais separados

| Dimensão | Resultado | Percentual honesto |
| --- | --- | ---: |
| Arquitetura | Ontologia, loader fechado, manifesto/hash, motor declarativo, API, auditoria e três portas | 100% estrutural |
| Catálogo cadastrado | 300/300 identidades únicas e tipadas | 100% |
| Conteúdo preenchido | 300 contratos estruturais; 300 módulos com definição, limites, tratamento inicial, tratamento definitivo e destino específicos em rascunho | 100% estrutural; 300/300 com conteúdo clínico específico não revisado |
| Referências | 300 módulos, 901 perguntas e 898 exames com fonte oficial candidata | 100% ligação candidata; 0% sustentação de campo validada |
| Revisão clínica | 0/300 revisados, 0/300 validados; 300 em fila auditável | 0% |
| Casos auditáveis | 4.500/4.500, 15 por módulo, com categorias, eventos e hash | 100% estrutural |
| Testes automatizados | 273 Python, 28 JavaScript e validadores externos aprovados | 100% da bateria atual |
| Validação visual | Assistido, Direto e Investigação verificados no Chrome; versão 0.22.0 verificada na API; três portas cobertas pela suíte JavaScript | smoke test atual aprovado |
| Desempenho | carga governada completa em 2,015 s de mediana local | medido; gate técnico ativo |
| Prontidão clínica real | sem curadoria/revisão humana e execução bloqueada | 0% |

Os percentuais são independentes e não podem ser somados em um percentual único.

## Evidências técnicas

- `catalog-valid decisionmed.knowledge 0.22.0 46 7 1 0 300 50 300 4500`;
- `specific-draft-overrides 300`: todos os 300 módulos possuem conteúdo
  clínico específico em rascunho e o gerador falha se qualquer módulo faltar;
- `dm300-case-robot passed 300 4500 0`;
- lotes de fonte candidata: 50 módulos/151 perguntas/150 exames; 150/451/450;
  300/901/898, todos com execução bloqueada;
- `dm300-review-queue passed 300 pending-human-review`;
- `dm300-load-benchmark passed median=2015.0ms`;
- `python -m unittest discover -s tests -p 'test_*.py'`: 273 aprovados;
- `node --test tests/intake_routing.test.cjs`: 28 aprovados;
- GitHub Actions remoto: `tests` da plataforma e `validate-catalog` do pacote
  de conhecimento concluídos com sucesso após a publicação;
- inspeção no Chrome: equivalente anginoso roteado para cardiologia; Assistido,
  Direto e Investigação chegaram ao resumo auditável exibindo conduta,
  tratamento, destino, fontes e botão de anexo por exame, sem erros de console.

## Bloqueios reais de aceite clínico

1. Nenhum dos 300 módulos possui revisor humano identificado, data de revisão
   ou prazo de nova revisão.
2. As fontes nos campos são candidatas; ainda faltam seção exata, população,
   cenário e redação confirmados por campo.
3. Critérios, diferenciais, red flags, exames, condutas, tratamentos e destinos
   ainda não podem ser apresentados como recomendações validadas.
4. A fila `DecisionMEd-Knowledge/curation/dm300-review-queue.json` está inteira
   em `pending_human_review`.
5. A licença e a permissão de uso de cada fonte ainda precisam ser confirmadas
   antes de qualquer uso comercial; a APA foi retirada das fontes candidatas
   após a identificação de sua restrição expressa ao uso em sistemas de IA e
   substituída, no lote psiquiátrico, pela diretriz mhGAP da OMS.

## Próximo aceite permitido

Um módulo só pode sair de `draft` depois de revisão humana identificada que
preencha todos os itens da fila, registre conflitos e prazo de nova revisão,
preserve os testes e mantenha as regras de segurança aplicáveis. A mudança deve
ser feita primeiro no lote de 50, depois 150 e, por fim, 300.
