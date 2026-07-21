# 014 - Evidence Graph

## 1. Objetivo

Este documento define como cada decisão clínica futura do PsychRx será ligada às evidências científicas.

O Evidence Graph representa a arquitetura conceitual que conecta decisões, estratégias, alertas, explicações e afirmações clínicas às fontes científicas que as sustentam, limitam ou contradizem.

Este documento não implementa banco de dados, não cria software, não define algoritmo e não prescreve.

## 2. Conceito Geral

O Evidence Graph organiza a relação entre:

- decisão clínica;
- pergunta clínica;
- fonte científica;
- qualidade da evidência;
- hierarquia da evidência;
- conflitos;
- múltiplas evidências;
- força da recomendação;
- atualização;
- rastreabilidade;
- transparência.

No PsychRx, nenhuma decisão clinicamente relevante deve aparecer como afirmação isolada. Toda decisão deve poder explicar de onde veio, qual evidência a sustenta, qual incerteza permanece e qual é sua força.

## 3. Fontes

Fontes são a origem científica, regulatória ou metodológica de uma afirmação clínica.

Podem incluir:

- diretrizes;
- revisões sistemáticas;
- meta-análises;
- ensaios clínicos;
- estudos observacionais;
- livros-texto;
- consensos;
- regulamentações;
- alertas oficiais de segurança;
- bulas e documentos regulatórios.

Cada `EvidenceSource` deve registrar:

- fonte;
- ano;
- tipo de evidência;
- qualidade;
- força da recomendação;
- data de revisão;
- status;
- conflitos conhecidos;
- aplicabilidade clínica.

Fonte sem metadados obrigatórios não deve sustentar decisão clínica.

## 4. Hierarquia

A hierarquia da evidência organiza o peso relativo das fontes.

Hierarquia conceitual:

1. regulamentações e alertas oficiais de segurança quando definem risco obrigatório;
2. diretrizes clínicas recentes com metodologia explícita;
3. revisões sistemáticas e meta-análises de alta qualidade;
4. ensaios clínicos randomizados;
5. estudos observacionais robustos;
6. consensos formais;
7. livros-texto;
8. estudos preliminares, relatos de caso e hipóteses mecanísticas.

Hierarquia não deve ser aplicada de forma cega. A aplicabilidade ao paciente, a segurança e o contexto clínico podem modificar o peso de uma evidência.

## 5. Conflitos

Conflitos ocorrem quando fontes científicas apontam para conclusões divergentes.

Podem surgir por:

- populações diferentes;
- métodos diferentes;
- desfechos diferentes;
- duração de acompanhamento diferente;
- comparadores diferentes;
- qualidade metodológica diferente;
- conflito de interesse;
- atualização de diretrizes;
- diferenças regulatórias;
- diferença entre eficácia em ensaio e efetividade no mundo real.

Quando houver conflito, o Evidence Graph deve registrar:

- fontes conflitantes;
- natureza do conflito;
- impacto sobre a conclusão;
- efeito sobre força da recomendação;
- necessidade de cautela;
- necessidade de decisão médica individualizada.

Conflito não resolvido deve reduzir a força da conclusão.

## 6. Múltiplas Evidências

Uma decisão clínica pode depender de múltiplas evidências.

As evidências podem sustentar dimensões diferentes:

- eficácia;
- segurança;
- tolerabilidade;
- interações;
- contraindicações;
- populações específicas;
- risco de recaída;
- monitorização;
- qualidade de vida;
- estabilidade.

O Evidence Graph deve permitir que uma decisão seja explicada por um conjunto de fontes, e não apenas por uma referência isolada.

Quando múltiplas evidências convergem, a confiança pode aumentar. Quando divergem, a recomendação deve ser mais cautelosa.

## 7. Qualidade

Qualidade da evidência indica o grau de confiança metodológica da fonte.

Deve considerar:

- desenho do estudo;
- risco de viés;
- consistência;
- precisão;
- tamanho da amostra;
- relevância clínica dos desfechos;
- aplicabilidade ao paciente;
- atualidade;
- conflitos de interesse;
- coerência com outras fontes.

Categorias conceituais:

- alta;
- moderada;
- baixa;
- muito baixa;
- insuficiente.

Evidência de baixa qualidade não deve sustentar recomendação forte.

## 8. Força da Recomendação

Força da recomendação indica o quanto uma evidência ou conjunto de evidências sustenta uma orientação clínica.

Ela depende de:

- qualidade da evidência;
- magnitude do benefício;
- gravidade do risco;
- aplicabilidade ao paciente;
- disponibilidade de alternativas;
- preferências do paciente;
- reversibilidade da decisão;
- necessidade de monitorização;
- impacto sobre estabilização.

Categorias conceituais:

- forte;
- moderada;
- fraca;
- condicional;
- insuficiente para recomendação.

Força da recomendação não é igual à qualidade da evidência. Uma evidência forte pode gerar recomendação fraca se o paciente tiver restrições relevantes.

## 9. Atualização

Evidências devem ser atualizadas de forma governada.

Atualização pode ocorrer por:

- nova diretriz;
- nova revisão sistemática;
- nova meta-análise;
- novo ensaio clínico;
- alerta regulatório;
- mudança de bula;
- nova evidência de segurança;
- conflito identificado;
- depreciação de fonte anterior.

Cada atualização deve registrar:

- fonte nova;
- fonte substituída ou afetada;
- motivo da atualização;
- impacto sobre conhecimento existente;
- impacto sobre alertas;
- impacto sobre estratégias;
- impacto sobre explicações;
- data de revisão;
- status.

Decisões futuras devem apontar para a versão da evidência utilizada.

## 10. Rastreabilidade

Rastreabilidade é a capacidade de reconstruir o caminho entre decisão e evidência.

Toda decisão clínica futura deve permitir responder:

- qual Clinical Snapshot estava vigente;
- qual pergunta clínica foi formulada;
- quais evidências foram usadas;
- qual fonte sustentou cada afirmação;
- qual qualidade da evidência;
- qual força da recomendação;
- quais conflitos existiam;
- qual aplicabilidade ao paciente;
- qual data de revisão;
- qual status da evidência;
- quais incertezas permaneceram.

A cadeia mínima deve ser:

```text
decisão clínica
  -> pergunta clínica
  -> evidências
  -> fontes
  -> qualidade
  -> força
  -> conflitos
  -> aplicabilidade
  -> versão/revisão
  -> explicação clínica
```

Sem rastreabilidade, a decisão é incompleta.

## 11. Transparência

Transparência significa que o médico deve conseguir compreender por que uma decisão, alerta ou comparação foi apresentada.

O Evidence Graph deve tornar visível:

- quais fontes foram usadas;
- quais fontes foram descartadas;
- quais fontes entram em conflito;
- quais evidências são fortes;
- quais evidências são fracas;
- onde existe incerteza;
- onde a aplicabilidade é limitada;
- por que a força da recomendação foi reduzida;
- por que a decisão final permanece médica.

Transparência impede que o PsychRx se torne uma caixa-preta clínica.

## 12. Relação com Outros Componentes

O Evidence Graph se relaciona com:

- Biblioteca Científica, que organiza fontes;
- Evidence Traceability Policy, que define metadados obrigatórios;
- Knowledge Graph, que organiza relações;
- Constraint Graph, que liga evidência a restrições;
- Decision Graph, que usa evidência em caminhos de decisão;
- Clinical Explanation, que comunica a justificativa;
- Audit, que preserva rastreabilidade.

## 13. Limites

O Evidence Graph:

- não implementa banco de dados;
- não cria software;
- não prescreve;
- não decide pelo médico;
- não elimina incerteza;
- não transforma evidência populacional em decisão individual automática;
- não substitui julgamento clínico;
- não deve ocultar conflitos;
- não deve gerar recomendação sem contexto.

Sua função é ligar decisões clínicas às evidências de forma clara, rastreável e transparente.

## 14. Declaração Final

O Evidence Graph do PsychRx garante que nenhuma decisão clínica futura seja apresentada sem lastro científico explícito.

Ele conecta decisões a fontes, hierarquia, conflitos, múltiplas evidências, qualidade, força da recomendação, atualização, rastreabilidade e transparência.

No PsychRx, uma decisão clínica só é aceitável quando pode explicar sua origem científica, seus limites, suas incertezas e sua aplicabilidade ao paciente.
