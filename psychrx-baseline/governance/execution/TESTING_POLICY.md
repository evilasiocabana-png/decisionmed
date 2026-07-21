# Testing Policy

## 1. Proposito

Este documento define a politica de testes do PsychRx antes da implementacao dos motores clinicos.

O objetivo e impedir que o projeto evolua sem base de testes suficiente para proteger dominio, contratos, seguranca clinica, explicabilidade, rastreabilidade, integracao e nao-regressao.

No PsychRx, testes nao sao etapa final. Eles fazem parte da governanca clinica e arquitetural do sistema.

## 2. Principio Central

Nenhum motor clinico podera ser considerado maduro sem:

- testes unitarios;
- testes de contrato;
- testes de cenarios clinicos simulados;
- testes de seguranca;
- testes de rastreabilidade da evidencia.

Um motor sem esses testes pode ser experimental, mas nao maduro.

## 3. Testes de Dominio

Testes de dominio validam se os conceitos centrais do PsychRx permanecem coerentes.

Devem verificar:

- entidades principais;
- value objects;
- aggregates;
- invariantes;
- eventos de dominio;
- relacoes entre paciente, sintomas, hipoteses, objetivos, riscos e estabilizacao;
- proibicao de recomendacao sem justificativa;
- proibicao de estrategia sem objetivo terapeutico;
- proibicao de decisao sem rastreabilidade.

Objetivo: garantir que o dominio nao seja distorcido por implementacao, interface ou conveniencia operacional.

## 4. Testes de Contratos

Testes de contratos validam fronteiras entre camadas e componentes.

Devem verificar:

- entradas esperadas;
- saidas esperadas;
- campos obrigatorios;
- formatos conceituais;
- erros ou respostas diante de dados incompletos;
- preservacao de rastreabilidade;
- ausencia de dependencia proibida;
- separacao entre interface, aplicacao, raciocinio, seguranca, conhecimento e evidencia.

Objetivo: garantir que uma camada possa evoluir sem quebrar contratos das demais.

## 5. Testes de Regressao

Testes de regressao verificam se funcionalidades, regras ou comportamentos ja validados continuam corretos apos alteracoes.

Devem cobrir:

- cenarios ja aceitos;
- bugs corrigidos;
- invariantes criticos;
- alertas de seguranca;
- explicacoes esperadas;
- rastreabilidade de evidencias;
- integridade de contratos.

Objetivo: impedir que uma mudanca nova quebre comportamento previamente validado.

## 6. Testes de Seguranca Clinica

Testes de seguranca clinica validam se o sistema reconhece riscos, restricoes e limites antes de qualquer comparacao estrategica.

Devem verificar:

- contraindicações;
- interacoes;
- risco elevado;
- dados ausentes criticos;
- comorbidades relevantes;
- efeitos adversos graves;
- bloqueio ou cautela diante de risco;
- ausencia de recomendacao forte quando a seguranca estiver incompleta;
- preservacao do medico como decisor final.

Objetivo: impedir que o sistema avance para raciocinio estrategico sem camada de seguranca.

## 7. Testes de Explicabilidade

Testes de explicabilidade validam se toda saida clinicamente relevante pode ser compreendida.

Devem verificar:

- justificativa da conclusao;
- dados usados;
- hipoteses consideradas;
- objetivos terapeuticos envolvidos;
- riscos identificados;
- fontes usadas;
- incertezas declaradas;
- limites da recomendacao ou comparacao;
- linguagem nao prescritiva quando aplicavel.

Objetivo: garantir que o sistema nao produza saidas opacas.

## 8. Testes de Rastreabilidade

Testes de rastreabilidade validam se cada saida pode ser reconstruida.

Devem verificar:

- Clinical Snapshot usado;
- versao do conhecimento;
- evidencias consultadas;
- fontes cientificas;
- regras ou criterios acionados;
- motores envolvidos;
- alertas emitidos;
- justificativas;
- registro de incertezas;
- relacao entre entrada e saida.

Objetivo: garantir que nenhuma decisao, alerta ou comparacao exista sem caminho auditavel.

## 9. Testes de Integracao

Testes de integracao validam a colaboracao entre camadas e componentes.

Devem verificar:

- aplicacao coordenando dominio, raciocinio, seguranca, conhecimento, evidencia e auditoria;
- interface consumindo apenas contratos permitidos;
- safety atuando antes de reasoning estrategico;
- evidence sustentando knowledge e safety;
- audit registrando sem decidir;
- ausencia de acesso direto proibido entre camadas.

Objetivo: garantir que componentes funcionem juntos sem violar arquitetura.

## 10. Testes de Nao-Regressao

Testes de nao-regressao sao uma protecao continua contra retorno de falhas clinicas ou arquiteturais.

Devem ser mantidos para:

- erros clinicos simulados ja corrigidos;
- violacoes de camada ja identificadas;
- falhas de explicabilidade;
- falhas de rastreabilidade;
- perda de fonte cientifica;
- recomendacoes indevidas;
- bugs de seguranca;
- conflitos de evidencia mal resolvidos.

Objetivo: impedir que erros criticos reaparecam.

## 11. Cenarios Clinicos Simulados

Motores clinicos devem ser testados com cenarios clinicos simulados, nunca com dados reais identificaveis sem politica especifica.

Cenarios simulados devem incluir:

- caso simples;
- caso com dados ausentes;
- caso com risco elevado;
- caso com interacao;
- caso com contraindicação;
- caso com comorbidade relevante;
- caso com incerteza diagnostica;
- caso com evidencia conflitante;
- caso com resposta parcial;
- caso com efeito adverso;
- caso com estabilidade parcial;
- caso com recaida ou recorrencia.

Objetivo: validar raciocinio, limites, seguranca e explicabilidade em situacoes proximas do uso real.

## 12. Maturidade dos Motores Clinicos

Um motor clinico so pode ser considerado maduro quando possuir:

- testes unitarios cobrindo comportamento interno esperado;
- testes de contrato cobrindo entradas e saidas;
- testes de cenarios clinicos simulados;
- testes de seguranca clinica;
- testes de explicabilidade;
- testes de rastreabilidade da evidencia;
- testes de regressao;
- testes de nao-regressao para falhas criticas;
- documentacao dos limites conhecidos;
- criterio claro de aceite.

Sem essa base, o motor deve permanecer em estado experimental.

## 13. Politica de Falhas

Falhas em testes devem ser tratadas conforme gravidade.

Falhas bloqueantes:

- recomendacao sem evidencia;
- recomendacao sem justificativa;
- perda de rastreabilidade;
- safety ignorado;
- interface decidindo conduta;
- dependencia proibida;
- mistura de conhecimento com algoritmo;
- teste clinico critico quebrado;
- regressao em alerta de seguranca.

Falhas bloqueantes impedem merge, maturidade ou release.

## 14. Relacao com Pull Requests

Todo Pull Request futuro que alterar dominio, raciocinio, seguranca, conhecimento, evidencia, aplicacao, interface ou auditoria deve informar:

- testes executados;
- testes nao executados e motivo;
- impacto em cenarios clinicos simulados;
- impacto em rastreabilidade;
- impacto em explicabilidade;
- risco de regressao;
- necessidade de novos testes.

Um Pull Request sem testes proporcionais ao risco deve ser rejeitado ou marcado como incompleto.

## 15. Criterio de Aceite da Politica

A evolucao do PsychRx nao deve ocorrer sem base de testes.

Nenhuma implementacao futura de motor clinico deve ser aceita se:

- nao possuir testes unitarios;
- nao possuir testes de contrato;
- nao possuir cenarios clinicos simulados;
- nao testar seguranca clinica;
- nao testar rastreabilidade da evidencia;
- quebrar regressao existente;
- reduzir explicabilidade;
- violar separacao entre camadas.

## 16. Declaracao Final

A politica de testes do PsychRx existe para proteger o sistema contra evolucao sem verificacao. Em um projeto de apoio ao raciocinio medico, testar nao e apenas garantir funcionamento tecnico; e preservar seguranca clinica, explicabilidade, rastreabilidade e confianca arquitetural.

Nenhum motor clinico deve amadurecer mais rapido que sua capacidade de ser testado, explicado e auditado.
