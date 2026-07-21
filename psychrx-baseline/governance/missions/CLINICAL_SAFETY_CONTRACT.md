# Clinical Safety Contract

## 1. Proposito

Este documento define o contrato de seguranca clinica obrigatorio do PsychRx.

Seu objetivo e impedir que o sistema se torne um recomendador inseguro. Nenhuma estrategia terapeutica pode ser apresentada, comparada ou sugerida sem avaliacao previa de riscos clinicos essenciais.

O PsychRx e uma plataforma de apoio ao raciocinio medico. Ele nao prescreve, nao substitui o medico e nao deve transformar dados incompletos em conduta.

## 2. Regra Central de Seguranca

Antes de qualquer `TherapeuticStrategy`, o PsychRx deve avaliar obrigatoriamente:

- risco de suicidio;
- risco de agressividade;
- delirium;
- intoxicacao;
- abstinencia;
- gestacao;
- lactacao;
- insuficiencia renal;
- insuficiencia hepatica;
- doenca cardiovascular;
- QT prolongado;
- epilepsia;
- interacoes medicamentosas;
- alergias;
- reacoes adversas graves previas.

Se esses elementos nao forem avaliados, a estrategia deve ser considerada clinicamente insegura ou insuficientemente contextualizada.

## 3. Principios do Contrato

- seguranca clinica vem antes de eficacia;
- risco agudo vem antes de comparacao terapeutica;
- dado ausente relevante deve ser tratado como incerteza, nao como ausencia de risco;
- nenhuma estrategia deve ser apresentada sem rastreabilidade;
- nenhuma estrategia deve ignorar contraindicações, interacoes ou fatores de risco;
- alertas devem ser explicaveis;
- o medico permanece como decisor final;
- o sistema deve preferir cautela a falsa seguranca.

## 4. Itens Obrigatorios de Avaliacao

### Risco de Suicidio

Deve ser avaliado antes de qualquer estrategia. A presenca de risco suicida atual, plano, intencao, tentativa recente ou fatores agravantes deve gerar alerta critico e pode exigir encaminhamento imediato.

### Risco de Agressividade

Deve ser avaliado quando houver impulsividade, agitacao, ameaca, comportamento violento, psicose, intoxicacao, abstinencia ou risco para terceiros.

### Delirium

Suspeita de delirium deve bloquear raciocinio psicofarmacologico usual ate avaliacao clinica apropriada. Delirium pode indicar condicao medica aguda.

### Intoxicacao

Intoxicacao por substancias, medicamentos ou alcool deve ser tratada como fator de risco critico, pois altera estado mental, risco comportamental, interacoes e seguranca medicamentosa.

### Abstinencia

Abstinencia pode gerar risco autonomico, convulsivo, psiquiatrico ou comportamental. Deve ser avaliada antes de qualquer estrategia.

### Gestacao

Gestacao modifica risco-beneficio, seguranca fetal, escolha de agentes, monitorizacao e necessidade de decisao especializada.

### Lactacao

Lactacao modifica exposicao do lactente, seguranca, monitorizacao e adequacao de estrategias.

### Insuficiencia Renal

Insuficiencia renal pode alterar eliminacao, risco de toxicidade, dose usual, monitorizacao e escolha de agente.

### Insuficiencia Hepatica

Insuficiencia hepatica pode alterar metabolismo, risco de toxicidade, interacoes e tolerabilidade.

### Doenca Cardiovascular

Doenca cardiovascular pode modificar risco de arritmia, hipotensao, hipertensao, eventos cardiacos, interacoes e necessidade de monitorizacao.

### QT Prolongado

QT prolongado ou risco de prolongamento de QT deve ser tratado como restricao de seguranca relevante, especialmente diante de combinacoes medicamentosas ou fatores metabolicos.

### Epilepsia

Epilepsia ou risco convulsivo modifica a seguranca de varias estrategias psicofarmacologicas e deve ser avaliada antes de comparacao.

### Interacoes Medicamentosas

Interacoes devem ser avaliadas entre medicamentos atuais, psicofarmacos, substancias, fitoterapicos quando conhecidos e condicoes clinicas relevantes.

### Alergias

Alergias medicamentosas devem ser registradas e consideradas antes de qualquer estrategia.

### Reacoes Adversas Graves Previas

Historico de reacao adversa grave previa deve ter alto peso na avaliacao de seguranca e pode funcionar como bloqueio absoluto ou alerta critico.

## 5. Bloqueios Absolutos

Bloqueios absolutos sao situacoes em que o PsychRx nao deve apresentar uma estrategia como adequada.

Podem incluir:

- risco suicida agudo sem avaliacao ou manejo;
- risco grave de agressividade sem avaliacao;
- suspeita de delirium nao esclarecida;
- intoxicacao aguda clinicamente relevante;
- abstinencia com risco grave;
- contraindicação formal grave;
- alergia ou reacao adversa grave previa ao agente ou classe relevante;
- interacao de alto risco sem possibilidade segura de manejo;
- risco cardiaco critico, incluindo QT prolongado relevante em contexto de agente de risco;
- insuficiencia renal ou hepatica grave sem avaliacao apropriada;
- qualquer situacao em que dados ausentes impeçam avaliar risco essencial.

Bloqueio absoluto nao e decisao final de tratamento. E uma barreira de seguranca para impedir apresentacao insegura de estrategia.

## 6. Alertas Criticos

Alertas criticos indicam risco que pode exigir acao imediata, encaminhamento, avaliacao presencial ou decisao especializada.

Exemplos:

- ideacao suicida com plano ou intencao;
- comportamento agressivo iminente;
- delirium suspeito;
- intoxicacao relevante;
- abstinencia grave;
- reacao adversa grave previa;
- interacao potencialmente perigosa;
- QT prolongado com risco aumentado;
- epilepsia instavel;
- gestacao com exposicao de risco;
- insuficiencia renal ou hepatica importante.

Alertas criticos devem ser apresentados antes de qualquer comparacao estrategica.

## 7. Alertas Moderados

Alertas moderados indicam riscos que nao bloqueiam necessariamente uma estrategia, mas exigem cautela, justificativa, monitorizacao ou revisao medica.

Exemplos:

- comorbidade controlada que aumenta risco;
- historico de efeito adverso moderado;
- interacao manejavel;
- risco cardiovascular nao critico;
- funcao renal ou hepatica levemente alterada;
- risco convulsivo historico mas controlado;
- preferencia do paciente que reduz adesao provavel;
- dados incompletos que nao bloqueiam, mas reduzem confianca.

Alertas moderados devem modificar a forca de qualquer comparacao terapeutica.

## 8. Necessidade de Encaminhamento

O PsychRx deve sinalizar necessidade de encaminhamento ou avaliacao urgente quando houver:

- risco suicida agudo;
- risco de agressividade iminente;
- delirium;
- intoxicacao clinicamente relevante;
- abstinencia grave;
- sinais de emergencia medica;
- reacao adversa grave;
- instabilidade cardiovascular;
- convulsao recente ou epilepsia descompensada;
- gestacao ou lactacao com risco complexo;
- qualquer situacao fora do escopo seguro de apoio ao raciocinio.

Encaminhamento deve ser apresentado como necessidade de avaliacao humana apropriada, nao como conduta automatica definitiva.

## 9. Necessidade de Monitorizacao

Quando houver risco identificado, a estrategia so pode ser discutida com plano de monitorizacao conceitual.

Monitorizacao pode envolver:

- sintomas;
- risco suicida ou comportamental;
- sinais de delirium;
- uso de substancias;
- efeitos adversos;
- sinais vitais;
- parametros cardiacos;
- funcao renal;
- funcao hepatica;
- risco convulsivo;
- gestacao ou lactacao;
- adesao;
- funcionalidade;
- qualidade de vida.

Ausencia de monitorizacao adequada deve reduzir a seguranca da estrategia.

## 10. Dados Ausentes

Dados ausentes sobre itens obrigatorios de seguranca devem ser tratados como incerteza clinica.

O sistema deve indicar:

- qual dado falta;
- por que ele importa;
- qual risco nao pode ser excluido;
- como isso limita a comparacao;
- se a ausencia bloqueia ou apenas reduz confianca.

Ausencia de informacao nao equivale a seguranca.

## 11. Relacao com Estrategias Terapeuticas

Toda `TherapeuticStrategy` deve ser precedida por avaliacao de seguranca.

O contrato de seguranca pode gerar:

- bloqueio absoluto;
- alerta critico;
- alerta moderado;
- necessidade de encaminhamento;
- necessidade de monitorizacao;
- reducao da forca da comparacao;
- exigencia de dados adicionais;
- revisao de objetivo terapeutico.

Uma estrategia nao deve ser apresentada como favoravel se houver risco essencial nao avaliado.

## 12. Relacao com Explicabilidade

Todo alerta ou bloqueio deve gerar `ClinicalExplanation`.

A explicacao deve informar:

- qual risco foi identificado;
- quais dados sustentam o alerta;
- quais dados estao ausentes;
- qual restricao foi acionada;
- qual evidencia ou regra clinica sustenta a cautela quando aplicavel;
- qual impacto isso tem sobre a estrategia;
- por que a decisao final permanece com o medico.

## 13. Relacao com Rastreabilidade

Toda avaliacao de seguranca deve ser rastreavel.

Devem ser preservados:

- ClinicalSnapshot usado;
- itens de seguranca avaliados;
- dados presentes;
- dados ausentes;
- alertas gerados;
- bloqueios aplicados;
- evidencias ou fontes usadas;
- versao do conhecimento;
- saida apresentada;
- usuario ou contexto da avaliacao.

Sem rastreabilidade, a avaliacao de seguranca e incompleta.

## 14. Criterio de Aceite Clinico

O PsychRx nao deve apresentar estrategia terapeutica se nao houver avaliacao minima dos itens obrigatorios deste contrato.

Para aceitar uma saida estrategica, deve ser possivel confirmar:

- risco de suicidio avaliado;
- risco de agressividade avaliado;
- delirium considerado;
- intoxicacao considerada;
- abstinencia considerada;
- gestacao e lactacao consideradas quando aplicavel;
- funcao renal e hepatica consideradas quando relevante;
- doenca cardiovascular e QT considerados;
- epilepsia considerada;
- interacoes avaliadas;
- alergias consideradas;
- reacoes adversas graves previas consideradas;
- alertas e bloqueios explicados;
- monitorizacao indicada quando necessaria;
- rastreabilidade preservada.

## 15. Declaracao Final

O Clinical Safety Contract e uma barreira obrigatoria contra recomendacoes inseguras.

No PsychRx, nenhuma estrategia terapeutica deve aparecer antes da seguranca clinica. O sistema deve reconhecer risco, explicitar incerteza, indicar bloqueios e alertas, exigir monitorizacao quando necessario e manter o medico como decisor final.

Seguranca nao e etapa acessoria. Seguranca e a primeira condicao do raciocinio clinico.
