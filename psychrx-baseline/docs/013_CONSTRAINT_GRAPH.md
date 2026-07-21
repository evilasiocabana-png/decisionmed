# 013 - Constraint Graph

## 1. Objetivo

Este documento define oficialmente o Constraint Graph do PsychRx.

O Constraint Graph representa a arquitetura conceitual das restrições que limitam, modificam, bloqueiam ou redirecionam a seleção de estratégias terapêuticas.

Este documento não cria regras computacionais, não implementa algoritmos, não prescreve e não define software. Ele descreve como restrições clínicas, individuais, ambientais e regulatórias devem ser consideradas no raciocínio clínico.

## 2. Conceito Geral

O Constraint Graph é a rede de limites que impede o PsychRx de tratar estratégias terapêuticas como escolhas abstratas.

Uma `TherapeuticStrategy` só pode ser analisada dentro de um contexto de:

- segurança;
- contraindicações;
- interações;
- comorbidades;
- fatores individuais;
- fatores ambientais;
- preferências do paciente;
- restrições regulatórias;
- capacidade de monitorização;
- evidência disponível.

O Constraint Graph responde:

> O que limita, reduz, bloqueia ou modifica esta estratégia para este paciente?

## 3. Restrições Absolutas

Restrições absolutas são condições que tornam uma estratégia inadequada, insegura ou não aceitável dentro de determinado contexto.

Elas podem bloquear uma estratégia ou impedir que ela seja apresentada como opção favorável.

Exemplos conceituais:

- contraindicação formal grave;
- alergia grave conhecida;
- reação adversa grave prévia;
- interação de alto risco;
- risco suicida ou agressivo agudo sem avaliação;
- delirium não esclarecido;
- intoxicação ou abstinência grave;
- condição médica aguda incompatível com a estratégia;
- restrição regulatória impeditiva.

Restrições absolutas devem prevalecer sobre benefício esperado.

## 4. Restrições Relativas

Restrições relativas não impedem necessariamente uma estratégia, mas exigem cautela, justificativa, monitorização ou comparação com alternativas.

Exemplos conceituais:

- comorbidade controlada;
- efeito adverso prévio moderado;
- interação manejável;
- risco cardiovascular não crítico;
- alteração renal ou hepática leve;
- adesão incerta;
- preferência do paciente contrária, mas discutível;
- evidência limitada para o perfil do paciente.

Restrições relativas reduzem a força de uma comparação, aumentam necessidade de monitorização e podem tornar outra estratégia mais coerente.

## 5. Contraindicações

Contraindicações são condições que tornam um psicofármaco, classe ou estratégia potencialmente inadequado.

Podem ser:

- absolutas;
- relativas;
- temporárias;
- contextuais;
- dependentes de gravidade;
- dependentes de monitorização;
- dependentes de avaliação médica especializada.

Toda contraindicação deve ser interpretada considerando:

- condição que a aciona;
- gravidade;
- evidência;
- aplicabilidade ao paciente;
- existência de alternativas;
- possibilidade ou impossibilidade de monitorização.

Contraindicação não deve ser tratada como detalhe lateral. Ela modifica diretamente o caminho decisório.

## 6. Fatores Individuais

Fatores individuais são características do paciente que alteram risco, benefício, tolerabilidade, adesão ou aplicabilidade de uma estratégia.

Incluem:

- idade;
- sexo biológico;
- gestação;
- lactação;
- peso;
- composição corporal;
- função renal;
- função hepática;
- histórico de resposta;
- histórico de efeitos adversos;
- alergias;
- sensibilidade medicamentosa;
- risco convulsivo;
- risco cardiovascular;
- cognição;
- rotina;
- capacidade de adesão;
- acesso a monitorização.

Fatores individuais impedem que o PsychRx aplique conhecimento científico de forma genérica.

## 7. Comorbidades

Comorbidades modificam o raciocínio psicofarmacológico.

Podem aumentar risco, alterar tolerabilidade, confundir sintomas, modificar objetivos terapêuticos ou exigir monitorização específica.

Exemplos:

- doença cardiovascular;
- diabetes;
- obesidade;
- epilepsia;
- doença renal;
- doença hepática;
- transtorno por uso de substâncias;
- transtorno bipolar;
- transtornos de ansiedade;
- dor crônica;
- distúrbios do sono;
- condições neurológicas.

Uma comorbidade pode transformar uma estratégia teoricamente adequada em estratégia de cautela, baixa prioridade ou bloqueio.

## 8. Interações

Interações são relações entre psicofármacos, outros medicamentos, substâncias, condições clínicas ou fatores individuais que modificam segurança, eficácia ou tolerabilidade.

Tipos conceituais:

- farmacocinéticas;
- farmacodinâmicas;
- clínicas;
- relacionadas a substâncias;
- relacionadas a comorbidades;
- relacionadas a vulnerabilidades individuais.

Interações podem:

- aumentar risco;
- reduzir eficácia;
- aumentar toxicidade;
- provocar efeitos adversos;
- exigir monitorização;
- bloquear combinações;
- reduzir força de uma estratégia.

Toda interação relevante deve ser rastreável a fonte ou justificativa científica.

## 9. Fatores Ambientais

Fatores ambientais são condições do contexto de vida ou cuidado que influenciam viabilidade, segurança e adesão de uma estratégia.

Podem incluir:

- suporte familiar;
- rede de cuidado;
- acesso a serviço de saúde;
- acesso a exames;
- condições de moradia;
- rotina de trabalho;
- exposição a estressores;
- uso de substâncias no ambiente;
- risco de violência;
- vulnerabilidade social;
- capacidade de comparecer a seguimento;
- disponibilidade de monitorização.

Fatores ambientais não substituem evidência científica, mas modificam aplicabilidade clínica.

Uma estratégia que exige monitorização frequente pode ser inadequada se o paciente não tem acesso real a acompanhamento.

## 10. Preferências do Paciente

Preferências do paciente são restrições relevantes para adesão, qualidade de vida e aceitabilidade.

Podem envolver:

- preferência por evitar sedação;
- preocupação com ganho de peso;
- preocupação com sexualidade;
- medo de efeitos adversos;
- recusa a determinados medicamentos;
- preferência por simplicidade;
- experiências negativas anteriores;
- prioridades funcionais;
- valores pessoais;
- disponibilidade para monitorização.

Preferências não substituem segurança clínica, mas devem ser consideradas no raciocínio.

Ignorar preferências pode reduzir adesão e comprometer estabilização.

## 11. Restrições Regulatórias

Restrições regulatórias são limites definidos por órgãos reguladores, legislação, bula, disponibilidade, aprovação formal, alertas sanitários ou normas institucionais.

Podem incluir:

- indicação aprovada;
- contraindicação formal;
- faixa etária autorizada;
- advertências de bula;
- exigência de monitorização;
- restrição de uso em gestação ou lactação;
- alerta de agência regulatória;
- disponibilidade no sistema de saúde;
- exigência institucional;
- restrição por jurisdição.

Restrições regulatórias não esgotam o raciocínio clínico, mas devem ser explicitadas quando impactam uma estratégia.

## 12. Influência sobre Estratégias Terapêuticas

O Constraint Graph influencia a seleção de `TherapeuticStrategy` de várias formas.

### Bloqueio

Uma restrição absoluta pode impedir que uma estratégia seja apresentada como adequada.

### Cautela

Uma restrição relativa pode permitir discussão da estratégia, mas com ressalvas, monitorização e explicação.

### Repriorização

Uma restrição pode tornar outra estratégia mais coerente com segurança, tolerabilidade ou adesão.

### Redução de Força

Conflitos, comorbidades, interações ou evidência limitada podem reduzir a força da comparação.

### Redefinição de Objetivo

Uma restrição pode mostrar que o objetivo inicial precisa ser ajustado.

### Necessidade de Monitorização

Uma estratégia pode depender de acompanhamento específico para ser clinicamente aceitável.

### Necessidade de Encaminhamento

Algumas restrições podem indicar necessidade de avaliação urgente, especializada ou presencial.

## 13. Relação com o Decision Graph

O Decision Graph mostra caminhos possíveis. O Constraint Graph define quais caminhos são seguros, limitados, bloqueados ou dependentes de cautela.

Toda bifurcação estratégica deve considerar restrições antes de avançar.

Se o Decision Graph pergunta "qual caminho pode ser seguido?", o Constraint Graph responde "sob quais limites esse caminho pode ou não ser seguido?".

## 14. Relação com Segurança Clínica

O Constraint Graph é parte essencial da segurança clínica.

Ele alimenta:

- bloqueios absolutos;
- alertas críticos;
- alertas moderados;
- necessidade de monitorização;
- necessidade de encaminhamento;
- redução de força da comparação;
- explicação clínica.

Nenhuma estratégia terapêutica deve ser apresentada ignorando restrições clinicamente relevantes.

## 15. Limites

O Constraint Graph:

- não prescreve;
- não decide conduta final;
- não implementa regras computacionais;
- não substitui avaliação médica;
- não resolve conflitos sozinho;
- não transforma preferência em decisão automática;
- não elimina incerteza;
- não deve operar sem rastreabilidade.

Sua função é explicitar limites para que a seleção de estratégias terapêuticas seja segura, contextual e explicável.

## 16. Declaração Final

O Constraint Graph do PsychRx é a arquitetura conceitual das restrições que protegem o raciocínio clínico.

Ele organiza restrições absolutas, restrições relativas, contraindicações, fatores individuais, comorbidades, interações, fatores ambientais, preferências do paciente e restrições regulatórias para mostrar como cada uma delas modifica, limita ou bloqueia estratégias terapêuticas.

No PsychRx, uma estratégia só pode ser considerada depois que suas restrições forem reconhecidas, explicadas e rastreadas.
