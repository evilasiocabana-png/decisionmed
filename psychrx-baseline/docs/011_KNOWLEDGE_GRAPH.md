# 011 - Knowledge Graph

## 1. Objetivo

Este documento define a arquitetura conceitual do Knowledge Graph do PsychRx.

O Knowledge Graph representa a rede de relações clínicas e científicas que permite ao sistema organizar o raciocínio psicofarmacológico de forma contextual, rastreável e reutilizável.

Este documento não define banco de dados, tecnologia, implementação ou ferramenta específica. Ele define como os conceitos se relacionam no plano clínico.

## 2. Estrutura Conceitual Central

O Knowledge Graph do PsychRx organiza o conhecimento a partir da seguinte cadeia clínica:

```text
Paciente
  ↓
Sintomas
  ↓
Síndromes
  ↓
Hipóteses
  ↓
Objetivos
  ↓
Restrições
  ↓
Estratégias
  ↓
Psicofármacos
  ↓
Resposta
  ↓
Monitorização
  ↓
Estabilização
```

Essa cadeia não deve ser entendida como fluxo rígido ou algoritmo. Ela representa uma ordem conceitual de dependência clínica: o sistema parte do paciente, organiza manifestações, formula hipóteses, define objetivos, reconhece restrições, compara estratégias, considera psicofármacos, acompanha resposta, monitora evolução e avalia estabilização.

## 3. Paciente

O `Patient` é o centro do Knowledge Graph.

Todas as relações clínicas devem poder retornar ao paciente:

- sintomas pertencem a um paciente;
- síndromes são inferidas a partir de sintomas de um paciente;
- hipóteses diagnósticas são formuladas no contexto de um paciente;
- objetivos terapêuticos são definidos para um paciente;
- restrições dependem de características do paciente;
- estratégias são consideradas para um paciente;
- resposta clínica é observada em um paciente;
- estabilização é avaliada na trajetória de um paciente.

O paciente não é apenas um identificador. Ele é o eixo longitudinal do grafo.

## 4. Sintomas

`Symptom` representa manifestação clínica observada, relatada ou monitorada.

Sintomas se relacionam com:

- paciente;
- intensidade;
- duração;
- frequência;
- curso temporal;
- funcionalidade;
- qualidade de vida;
- medicamentos em uso;
- eventos adversos;
- síndromes;
- hipóteses diagnósticas;
- objetivos terapêuticos;
- monitorização.

Sintomas não devem gerar diagnóstico automaticamente. Eles são sinais clínicos que ganham significado pela relação com outros elementos.

## 5. Síndromes

`Syndrome` representa agrupamento clínico de sintomas.

Síndromes ajudam a organizar padrões psicopatológicos sem fechar diagnóstico definitivo.

Relações principais:

- sintomas compõem síndromes;
- síndromes sugerem hipóteses;
- síndromes podem coexistir;
- síndromes podem modificar objetivos;
- síndromes podem indicar riscos;
- síndromes podem exigir monitorização específica.

Síndrome é um nível intermediário entre sintoma e hipótese diagnóstica.

## 6. Hipóteses

`DiagnosticHypothesis` representa uma hipótese diagnóstica em avaliação.

Hipóteses se relacionam com:

- sintomas que favorecem;
- sintomas que contradizem;
- síndromes associadas;
- diagnósticos diferenciais;
- nível de confiança;
- dados ausentes;
- objetivos terapêuticos;
- restrições;
- necessidade de revisão longitudinal.

Hipóteses não são conclusões finais. Elas carregam incerteza e devem poder ser atualizadas quando o Clinical Snapshot muda.

## 7. Objetivos

`TherapeuticObjective` representa o alvo clínico que orienta raciocínio, comparação e monitorização.

Objetivos derivam da relação entre:

- paciente;
- sintomas;
- síndromes;
- hipóteses;
- riscos;
- funcionalidade;
- qualidade de vida;
- resposta anterior;
- estabilidade desejada.

Exemplos de objetivos:

- reduzir sintomas-alvo;
- reduzir risco;
- melhorar funcionalidade;
- preservar qualidade de vida;
- melhorar tolerabilidade;
- prevenir recaída;
- sustentar remissão;
- alcançar estabilidade sustentada.

Nenhuma estratégia deve existir sem objetivo.

## 8. Restrições

`TherapeuticRestriction` representa limites que modificam, reduzem ou bloqueiam estratégias.

Restrições podem vir de:

- contraindicações;
- interações;
- comorbidades;
- alergias;
- reações adversas graves prévias;
- gestação;
- lactação;
- função renal;
- função hepática;
- doença cardiovascular;
- QT prolongado;
- epilepsia;
- risco suicida;
- risco de agressividade;
- delirium;
- intoxicação;
- abstinência;
- preferências do paciente;
- capacidade de adesão e monitorização.

As restrições conectam segurança clínica ao raciocínio terapêutico. Elas devem ser avaliadas antes de qualquer estratégia.

## 9. Estratégias

`TherapeuticStrategy` representa caminho terapêutico conceitual comparável, sem equivaler a prescrição.

Estratégias se relacionam com:

- objetivos;
- restrições;
- evidências;
- riscos;
- benefícios esperados;
- psicofármacos;
- monitorização;
- resposta clínica;
- estabilização.

Uma estratégia deve ser compreendida como possibilidade argumentada, não como ordem clínica.

## 10. Psicofármacos

`PsychopharmacologicalAgent` representa agente psicofarmacológico dentro do modelo oficial do PsychRx.

Psicofármacos se relacionam com:

- classes;
- mecanismos;
- sistemas de neurotransmissão;
- indicações;
- sintomas-alvo;
- síndromes;
- estratégias;
- contraindicações;
- interações;
- efeitos adversos;
- monitorização;
- evidências;
- resposta clínica.

O Knowledge Graph deve evitar que psicofármaco seja tratado isoladamente. Todo agente precisa ser compreendido em contexto clínico, restritivo e evidencial.

## 11. Resposta

`ClinicalResponse` representa mudança clínica observada ao longo do tempo.

Resposta pode envolver:

- melhora sintomática;
- piora sintomática;
- resposta parcial;
- ausência de resposta;
- remissão;
- deterioração clínica;
- melhora funcional;
- piora funcional;
- efeitos adversos;
- adesão;
- tolerabilidade;
- qualidade de vida.

Resposta liga estratégia, psicofármaco, paciente e monitorização.

## 12. Monitorização

`MonitoringPlan` representa acompanhamento conceitual de sintomas, riscos, efeitos adversos, funcionalidade e objetivos.

Monitorização se relaciona com:

- objetivos terapêuticos;
- restrições;
- psicofármacos;
- efeitos adversos;
- resposta clínica;
- recaída;
- recorrência;
- remissão;
- estabilização.

Sem monitorização, não há base suficiente para afirmar estabilidade sustentada.

## 13. Estabilização

Estabilização é o nó integrador final do Knowledge Graph.

Ela depende da relação entre:

- sintomas;
- funcionalidade;
- qualidade de vida;
- risco;
- restrições;
- resposta;
- tolerabilidade;
- adesão;
- monitorização;
- recaída;
- recorrência;
- remissão.

Estabilização não é apenas melhora sintomática. É o resultado integrado da trajetória clínica.

## 14. Tipos de Relações

O Knowledge Graph deve representar diferentes tipos de relação.

### Relações de pertencimento

Indicam que um elemento pertence ao contexto de outro.

Exemplos:

- paciente apresenta sintoma;
- paciente possui restrição;
- estratégia pertence a objetivo.

### Relações de composição

Indicam que um conjunto forma uma estrutura clínica.

Exemplos:

- sintomas compõem síndrome;
- fatores compõem restrição;
- indicadores compõem monitorização.

### Relações de sustentação

Indicam que um elemento apoia outro.

Exemplos:

- sintomas sustentam hipótese;
- evidência sustenta estratégia;
- resposta sustenta avaliação de estabilidade.

### Relações de contradição

Indicam que um elemento enfraquece outro.

Exemplos:

- sintoma contradiz hipótese;
- efeito adverso reduz adequação de estratégia;
- restrição bloqueia psicofármaco.

### Relações de modificação

Indicam que um elemento altera peso ou aplicabilidade de outro.

Exemplos:

- comorbidade modifica estratégia;
- preferência do paciente modifica adesão esperada;
- qualidade da evidência modifica força da comparação.

### Relações de risco

Indicam potencial de dano, cautela ou bloqueio.

Exemplos:

- psicofármaco aumenta risco;
- interação aumenta risco;
- QT prolongado modifica segurança.

### Relações longitudinais

Indicam evolução ao longo do tempo.

Exemplos:

- sintoma melhora;
- resposta se sustenta;
- remissão evolui para estabilidade;
- estabilidade se rompe por recaída.

### Relações de evidência

Indicam origem científica, qualidade e aplicabilidade.

Exemplos:

- relação possui fonte;
- fonte possui qualidade;
- evidência sustenta afirmação;
- conflito reduz confiança.

## 15. Hierarquia

O Knowledge Graph possui hierarquia clínica.

A hierarquia principal é:

```text
Paciente
  -> Sintomas
    -> Síndromes
      -> Hipóteses
        -> Objetivos
          -> Restrições
            -> Estratégias
              -> Psicofármacos
                -> Resposta
                  -> Monitorização
                    -> Estabilização
```

Essa hierarquia organiza dependência conceitual, não superioridade absoluta.

Exemplo: uma restrição pode modificar uma estratégia, mas também pode obrigar revisão de objetivo ou hipótese. O grafo deve permitir retorno e revisão, não apenas avanço linear.

## 16. Herança Semântica

Herança semântica significa que conceitos mais específicos herdam significado clínico de conceitos mais gerais.

Exemplos:

- um sintoma herda contexto do paciente;
- uma síndrome herda os sintomas que a compõem;
- uma hipótese herda o suporte e as incertezas de sintomas e síndromes;
- um objetivo herda relevância das hipóteses, sintomas e riscos;
- uma estratégia herda limites dos objetivos e restrições;
- um psicofármaco herda contexto da estratégia em que é considerado;
- uma resposta herda o contexto da estratégia e do paciente;
- a estabilização herda a trajetória de resposta, monitorização, risco e funcionalidade.

Essa herança impede que elementos sejam interpretados isoladamente.

## 17. Rastreabilidade

Toda relação clinicamente relevante no Knowledge Graph deve ser rastreável.

Rastreabilidade deve permitir responder:

- qual paciente originou a relação;
- qual Clinical Snapshot estava vigente;
- quais sintomas sustentaram a relação;
- quais hipóteses estavam ativas;
- quais objetivos orientaram a decisão;
- quais restrições foram consideradas;
- quais evidências sustentaram a relação;
- qual versão do conhecimento foi usada;
- quais incertezas permaneceram.

Sem rastreabilidade, a relação não deve sustentar decisão clínica.

## 18. Reutilização de Conhecimento

O Knowledge Graph deve permitir reutilização controlada de conhecimento.

Reutilização significa que conceitos científicos e clínicos estruturados podem ser usados em diferentes contextos sem duplicação.

Exemplos:

- uma interação medicamentosa pode ser reutilizada em múltiplos pacientes;
- uma contraindicação pode ser aplicada a diferentes estratégias;
- um efeito adverso pode informar restrições, monitorização e explicação;
- uma evidência pode sustentar mais de uma relação;
- um objetivo terapêutico pode orientar diferentes estratégias.

Reutilização deve respeitar:

- contexto do paciente;
- aplicabilidade clínica;
- versão da evidência;
- qualidade da fonte;
- restrições individuais;
- rastreabilidade.

Conhecimento reutilizado nunca deve ser aplicado mecanicamente.

## 19. Limites

O Knowledge Graph:

- não prescreve;
- não decide pelo médico;
- não substitui avaliação clínica;
- não implementa banco de dados;
- não depende de tecnologia específica;
- não transforma associação em causalidade automática;
- não elimina incerteza;
- não dispensa evidência científica;
- não substitui o Clinical Operating Mind.

Sua função é organizar relações para apoiar raciocínio, explicabilidade, segurança e rastreabilidade.

## 20. Declaração Final

O Knowledge Graph do PsychRx é a arquitetura conceitual que conecta paciente, sintomas, síndromes, hipóteses, objetivos, restrições, estratégias, psicofármacos, resposta, monitorização e estabilização.

Ele permite que o sistema compreenda relações clínicas sem perder contexto, herança semântica, rastreabilidade e reutilização de conhecimento.

No PsychRx, nenhum elemento clínico deve ser interpretado isoladamente. Toda relação deve permanecer conectada ao paciente, ao contexto, à evidência e à trajetória longitudinal.
