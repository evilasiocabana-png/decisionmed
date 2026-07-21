# 024 - Therapeutic Objective Engine

## 1. Definicao

O Therapeutic Objective Engine e o motor conceitual responsavel por estabelecer, priorizar e revisar objetivos terapeuticos no PsychRx.

Ele define o que o raciocinio clinico esta tentando alcancar antes de qualquer geracao ou comparacao de TherapeuticStrategy.

Este documento nao implementa software, nao define API, nao cria banco de dados, nao escolhe tecnologia e nao descreve algoritmo executavel.

## 2. Missao

A missao do Therapeutic Objective Engine e transformar Clinical Snapshot, hipoteses diagnosticas, riscos, funcionalidade, preferencias e trajetoria longitudinal em objetivos terapeuticos explicitos, rastreaveis e revisaveis.

## 3. Responsabilidades

- Definir objetivos primarios e secundarios.
- Priorizar objetivos conforme risco, gravidade e contexto.
- Identificar conflitos entre objetivos.
- Individualizar objetivos ao paciente.
- Definir criterios conceituais de sucesso.
- Atualizar objetivos ao longo do tempo.
- Impedir estrategia sem objetivo terapeutico.
- Apoiar explicabilidade e monitorizacao.

## 4. Entradas Conceituais

- Clinical Snapshot.
- Hipoteses diagnosticas e nivel de confianca.
- Sintomas-alvo.
- Riscos e restricoes.
- Funcionalidade.
- Qualidade de vida.
- Preferencias do paciente.
- Historico de resposta e tolerabilidade.
- Dados de monitorizacao.
- Trajetoria longitudinal.

## 5. Saidas Conceituais

- Objetivos terapeuticos primarios.
- Objetivos terapeuticos secundarios.
- Prioridade relativa entre objetivos.
- Conflitos entre objetivos.
- Criterios de sucesso.
- Necessidades de monitorizacao.
- Incertezas relacionadas aos objetivos.
- Justificativa para cada objetivo.

## 6. Objetivos Primarios

Objetivos primarios sao os alvos clinicos centrais de um ciclo de raciocinio.

Podem envolver reducao de risco, estabilizacao de quadro agudo, melhora de sintomas-alvo, restauracao funcional, prevencao de deterioracao, remissao ou estabilidade clinica.

Devem ser poucos, claros e clinicamente justificados.

## 7. Objetivos Secundarios

Objetivos secundarios refinam o cuidado sem deslocar o foco principal.

Podem envolver melhora do sono, reducao de sintomas residuais, melhora de adesao, reducao de efeitos adversos, qualidade de vida, funcionalidade e prevencao de recaida.

Objetivos secundarios nao devem competir silenciosamente com objetivos primarios.

## 8. Priorizacao

A priorizacao deve considerar:

- seguranca clinica;
- risco imediato;
- gravidade;
- impacto funcional;
- sofrimento subjetivo;
- reversibilidade;
- potencial de deterioracao;
- preferencia do paciente;
- evidencia disponivel;
- viabilidade de monitorizacao;
- relacao com estabilizacao.

Seguranca clinica prevalece sobre eficacia sintomatica quando houver risco relevante.

## 9. Conflitos entre Objetivos

Conflitos surgem quando otimizar um objetivo pode prejudicar outro.

Exemplos conceituais incluem eficacia versus seguranca, resposta rapida versus tolerabilidade, sedacao terapeutica versus funcionalidade, melhora sintomatica versus qualidade de vida e preferencia do paciente versus risco clinico.

O motor deve nomear o conflito, explicar seus polos e preservar decisao medica final.

## 10. Individualizacao

Objetivos devem ser individualizados ao paciente, considerando sintomas, sindromes, hipoteses, comorbidades, funcionalidade, qualidade de vida, preferencias, historico de resposta, eventos adversos e capacidade de acompanhamento.

O mesmo diagnostico pode gerar objetivos diferentes em pacientes diferentes.

## 11. Criterios de Sucesso

Cada objetivo deve ter criterios de sucesso conceituais.

Podem incluir reducao de sintomas-alvo, melhora funcional, reducao de risco, ausencia de deterioracao, tolerabilidade aceitavel, adesao viavel, melhora de qualidade de vida, remissao, estabilidade parcial ou estabilidade sustentada.

Sucesso terapeutico nao deve ser definido apenas por melhora sintomatica.

## 12. Atualizacao Longitudinal

Objetivos devem ser revisados quando houver mudanca do Clinical Snapshot, nova hipotese diagnostica, novo risco, evento adverso, resposta parcial, remissao, recaida, recorrencia, deterioracao clinica ou mudanca nas preferencias do paciente.

Objetivos podem ser mantidos, rebaixados, substituidos, suspensos ou priorizados novamente.

## 13. Integracao com Clinical Snapshot

O Clinical Snapshot fornece o estado clinico atual que ancora os objetivos.

Sem Snapshot atualizado, objetivos terapeuticos ficam abstratos e perdem rastreabilidade.

## 14. Integracao com Diagnostic Reasoning

O Diagnostic Reasoning Engine informa quais hipoteses sustentam ou limitam os objetivos.

Objetivos nao devem depender de diagnostico tratado como certeza quando o proprio raciocinio ainda expressa incerteza relevante.

## 15. Limites

O Therapeutic Objective Engine nao deve:

- prescrever;
- escolher conduta final;
- definir estrategia antes do objetivo;
- ignorar seguranca;
- declarar sucesso sem monitorizacao;
- transformar preferencia em decisao automatica;
- operar sem rastreabilidade.

## 16. Declaracao Final

O Therapeutic Objective Engine da direcao ao raciocinio clinico do PsychRx.

No PsychRx, nenhuma estrategia deve existir antes de um objetivo, nenhum objetivo deve ignorar seguranca e nenhum sucesso deve ser declarado sem relacao com estabilidade clinica.
