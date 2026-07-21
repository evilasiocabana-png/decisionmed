# 016 - Question Engine

## 1. Definicao

O Question Engine e o motor conceitual responsavel por identificar quais informacoes clinicas ainda precisam ser coletadas para reduzir a incerteza do raciocinio do PsychRx.

Ele nao entrevista o paciente de forma autonoma, nao substitui a anamnese medica e nao decide conduta. Sua funcao e organizar lacunas clinicas relevantes para que o medico saiba quais dados ainda sao necessarios antes de formular hipoteses, objetivos, restricoes ou estrategias.

## 2. Missao

A missao do Question Engine e transformar um Clinical Snapshot incompleto em uma agenda de investigacao clinica priorizada, explicavel e rastreavel.

Ele responde a pergunta:

```text
Quais informacoes ainda faltam para compreender melhor este paciente, reduzir risco e sustentar o raciocinio clinico?
```

## 3. Responsabilidades

O Question Engine deve:

- identificar lacunas no Clinical Snapshot;
- priorizar perguntas clinicamente relevantes;
- diferenciar perguntas obrigatorias de perguntas condicionais;
- indicar dados ausentes que aumentam risco;
- apoiar o Diagnostic Reasoning;
- apoiar a avaliacao de seguranca;
- reduzir incerteza antes de qualquer comparacao estrategica;
- explicitar por que determinada informacao e necessaria.

## 4. Entradas Conceituais

As entradas conceituais incluem:

- Clinical Snapshot atual;
- sintomas, sindromes e hipoteses em avaliacao;
- objetivos terapeuticos preliminares;
- restricoes conhecidas;
- dados ausentes relevantes;
- alertas de seguranca pendentes;
- historico longitudinal quando disponivel;
- evidencias ou criterios que exigem determinada informacao para interpretacao segura.

## 5. Saidas Conceituais

As saidas conceituais incluem:

- lista priorizada de perguntas;
- perguntas obrigatorias;
- perguntas condicionais;
- justificativa para cada pergunta relevante;
- indicacao de incertezas ainda abertas;
- criterios de suficiencia da coleta;
- sinalizacao de risco quando dado essencial estiver ausente.

## 6. Estrategia de Investigacao Clinica

A investigacao clinica deve seguir o principio de raciocinio antes de estrategia.

O Question Engine deve organizar perguntas em torno de:

- seguranca imediata;
- caracterizacao dos sintomas;
- curso temporal;
- sindromes possiveis;
- hipoteses diagnosticas;
- funcionalidade;
- tratamentos atuais e previos;
- comorbidades;
- uso de substancias;
- fatores individuais;
- preferencias e contexto do paciente;
- restricoes que podem modificar qualquer estrategia futura.

## 7. Priorizacao de Perguntas

A prioridade deve considerar:

- risco clinico potencial;
- impacto sobre seguranca;
- impacto sobre hipoteses diagnosticas;
- impacto sobre objetivos terapeuticos;
- impacto sobre restricoes;
- grau de incerteza;
- possibilidade de mudar a interpretacao do caso;
- urgencia clinica.

Perguntas relacionadas a risco agudo e seguranca devem preceder perguntas voltadas a refinamento terapeutico.

## 8. Perguntas Obrigatorias

Perguntas obrigatorias sao aquelas sem as quais o raciocinio fica inseguro ou insuficientemente rastreavel.

Podem envolver:

- risco de suicidio;
- risco de agressividade;
- delirium;
- intoxicacao;
- abstinencia;
- gestacao;
- lactacao;
- alergias;
- reacoes adversas graves previas;
- interacoes medicamentosas;
- doenca cardiovascular;
- QT prolongado;
- epilepsia;
- insuficiencia renal;
- insuficiencia hepatica.

Quando uma pergunta obrigatoria nao for respondida, o sistema deve tratar a ausencia como incerteza relevante, nao como ausencia de risco.

## 9. Perguntas Condicionais

Perguntas condicionais surgem quando uma informacao previa abre uma nova necessidade de investigacao.

Exemplos conceituais:

- sintoma novo pode exigir caracterizacao de inicio, duracao e gravidade;
- suspeita sindromica pode exigir dados de curso temporal;
- restricao identificada pode exigir dados de monitorizacao;
- resposta parcial pode exigir avaliacao de adesao, tolerabilidade e objetivos;
- evento adverso pode exigir avaliacao de gravidade e relacao temporal.

Perguntas condicionais devem manter relacao clara com o dado que as motivou.

## 10. Criterios para Encerrar a Coleta

A coleta pode ser considerada suficiente quando:

- riscos essenciais foram avaliados;
- o Clinical Snapshot possui dados minimos para raciocinio;
- hipoteses principais podem ser formuladas com nivel explicito de incerteza;
- objetivos terapeuticos podem ser definidos sem inversao de prioridade;
- restricoes relevantes foram identificadas ou explicitamente permanecem desconhecidas;
- lacunas remanescentes foram registradas como incerteza.

Encerrar coleta nao significa eliminar toda incerteza. Significa tornar a incerteza visivel, proporcional e clinicamente manejavel.

## 11. Integracao com Clinical Snapshot

O Clinical Snapshot e a principal entrada do Question Engine.

Quando o Snapshot estiver incompleto, inconsistente ou desatualizado, o Question Engine deve indicar quais informacoes precisam ser acrescentadas ou revisadas.

Cada nova informacao coletada deve poder atualizar o Snapshot e, se necessario, modificar hipoteses, objetivos, restricoes e alertas.

## 12. Integracao com Diagnostic Reasoning

O Question Engine apoia o Diagnostic Reasoning ao identificar dados que:

- favorecem uma hipotese;
- enfraquecem uma hipotese;
- diferenciam sindromes semelhantes;
- aumentam ou reduzem confianca diagnostica;
- indicam necessidade de avaliacao adicional.

Ele nao cria diagnosticos finais. Ele organiza perguntas que tornam o raciocinio diagnostico mais seguro e explicavel.

## 13. Reducao da Incerteza

A incerteza deve ser reduzida por coleta direcionada, nao por suposicao.

O Question Engine deve:

- tornar lacunas explicitas;
- diferenciar dado ausente de dado negativo;
- preservar duvida clinica quando apropriado;
- impedir conclusoes prematuras;
- registrar incertezas persistentes.

## 14. Relacao com Outros Motores

O Question Engine se relaciona com:

- Clinical Snapshot, que fornece o estado clinico atual;
- Safety First Engine, que exige dados de risco antes de estrategia;
- Diagnostic Reasoning, que depende de informacoes suficientes;
- Therapeutic Objective Engine, que depende de objetivos ancorados no paciente;
- Monitoring Engine, que pode gerar perguntas de acompanhamento;
- Explanation Engine, que deve explicar por que uma pergunta importa.

## 15. Limites

O Question Engine nao deve:

- prescrever;
- recomendar estrategia terapeutica;
- substituir entrevista clinica;
- diagnosticar sozinho;
- transformar pergunta em conduta;
- assumir ausencia de risco quando dado essencial estiver ausente;
- criar novos conceitos clinicos fora da Ontologia.

## 16. Declaracao Final

O Question Engine e o motor que protege o raciocinio do PsychRx contra conclusoes prematuras.

Ele organiza a investigacao clinica, torna lacunas visiveis, prioriza seguranca e reduz incerteza antes de qualquer estrategia.

No PsychRx, perguntar corretamente vem antes de comparar qualquer caminho terapeutico.
