# 009 - Clinical Snapshot

## 1. Definicao

O Clinical Snapshot e a representacao dinamica, contextual e rastreavel do estado clinico atual do paciente dentro do PsychRx.

Ele nao e o paciente inteiro, nem substitui sua historia longitudinal. E uma leitura organizada de um momento clinico especifico, construida a partir dos dados disponiveis, sintomas atuais, sindromes possiveis, hipoteses diagnosticas, objetivos terapeuticos, restricoes, riscos, incertezas e informacoes relevantes para o raciocinio psicofarmacologico.

O Clinical Snapshot responde a pergunta:

> Qual e o estado clinico relevante deste paciente agora para fins de raciocinio, seguranca, objetivos terapeuticos, comparacao de estrategias e monitorizacao?

## 2. Objetivo

O objetivo do Clinical Snapshot e oferecer ao Clinical Operating Mind uma base clinica organizada antes de qualquer raciocinio diagnostico, terapeutico ou estrategico.

Ele deve:

- organizar dados clinicos dispersos;
- separar dados conhecidos, dados ausentes e incertezas;
- representar o estado atual do paciente;
- sustentar perguntas clinicas;
- orientar hipoteses diagnosticas;
- apoiar definicao de objetivos terapeuticos;
- explicitar restricoes e riscos;
- permitir comparacao longitudinal;
- preparar a avaliacao de seguranca;
- apoiar explicabilidade e rastreabilidade.

O Snapshot existe para impedir que o PsychRx raciocine a partir de dados soltos, incompletos ou descontextualizados.

## 3. Momento de Criacao

O Clinical Snapshot deve ser criado sempre que o sistema precisar organizar o estado clinico atual do paciente.

Momentos principais:

- primeira avaliacao do paciente no sistema;
- nova avaliacao clinica relevante;
- mudanca importante de sintomas;
- surgimento de novo risco;
- registro de efeito adverso;
- mudanca de funcionalidade;
- mudanca de qualidade de vida;
- inclusao, retirada ou alteracao relevante de psicofarmaco;
- formulacao ou revisao de hipotese diagnostica;
- definicao ou revisao de objetivo terapeutico;
- identificacao de restricao terapeutica;
- comparacao de estrategias;
- avaliacao de resposta clinica;
- avaliacao de estabilidade, remissao, recaida ou recorrencia.

Nenhuma comparacao de `TherapeuticStrategy` deve ocorrer sem Clinical Snapshot atualizado ou explicitamente validado.

## 4. Atualizacao Longitudinal

O Clinical Snapshot representa um momento, mas so ganha sentido dentro da trajetoria do paciente.

Cada novo Snapshot deve poder ser comparado com Snapshots anteriores para identificar:

- melhora ou piora sintomatica;
- mudanca de intensidade, frequencia ou duracao dos sintomas;
- aparecimento de nova sindrome;
- mudanca de hipotese diagnostica;
- mudanca de objetivo terapeutico;
- surgimento ou resolucao de restricoes;
- resposta clinica;
- efeitos adversos;
- mudanca funcional;
- mudanca de qualidade de vida;
- risco de recaida;
- recorrencia;
- remissao;
- estabilidade parcial ou sustentada.

O Snapshot nao deve apagar o passado. Ele deve atualizar o presente preservando a possibilidade de reconstruir a trajetoria.

## 5. Informacoes Obrigatorias

Um Clinical Snapshot minimo deve conter:

- identificacao clinica do paciente no sistema;
- data ou momento de referencia;
- sintomas atuais relevantes;
- intensidade, duracao, frequencia ou curso dos sintomas quando disponivel;
- sindromes possiveis ou padroes sintomaticos relevantes;
- funcionalidade atual;
- qualidade de vida ou impacto subjetivo quando disponivel;
- medicamentos ou psicofarmacos em uso;
- historico terapeutico relevante;
- efeitos adversos conhecidos;
- comorbidades relevantes;
- fatores de risco;
- restricoes terapeuticas conhecidas;
- dados ausentes clinicamente importantes;
- hipoteses diagnosticas em avaliacao;
- nivel de confianca das hipoteses quando aplicavel;
- objetivos terapeuticos ativos;
- alertas de seguranca;
- incertezas;
- fontes quando houver informacao cientifica associada.

Se uma informacao obrigatoria estiver ausente, o Snapshot deve declarar a lacuna em vez de ocultá-la.

## 6. Relacao com Sintomas

Sintomas sao uma das entradas centrais do Clinical Snapshot.

O Snapshot deve organizar sintomas por:

- presenca ou ausencia;
- intensidade;
- frequencia;
- duracao;
- curso temporal;
- impacto funcional;
- relacao com medicamentos;
- relacao com eventos clinicos ou psicossociais;
- evolucao em relacao a Snapshots anteriores.

O Snapshot nao deve transformar sintoma isolado em diagnostico. Sintomas precisam ser interpretados em contexto, agrupados quando apropriado e relacionados a sindromes, hipoteses, riscos e objetivos.

## 7. Relacao com Sindromes

Sindromes sao agrupamentos clinicos de sintomas que ajudam a organizar padroes psicopatologicos ou estados clinicos.

O Clinical Snapshot deve indicar quando um conjunto de sintomas sugere uma sindrome relevante.

Ele deve diferenciar:

- sintoma isolado;
- agrupamento sintomatico;
- sindrome possivel;
- hipotese diagnostica;
- diagnostico estabelecido.

Uma sindrome no Snapshot nao deve ser tratada como diagnostico final. Ela e uma estrutura intermediaria para orientar perguntas, hipoteses e objetivos.

## 8. Relacao com Hipoteses Diagnosticas

O Clinical Snapshot sustenta, limita e atualiza hipoteses diagnosticas.

Ele deve indicar:

- quais dados favorecem uma hipotese;
- quais dados contradizem uma hipotese;
- quais sindromes apoiam a formulacao;
- quais diagnosticos diferenciais permanecem abertos;
- quais informacoes faltam;
- qual o nivel de confianca atual;
- se houve mudanca em relacao a Snapshots anteriores.

Hipoteses diagnosticas nao devem surgir fora do Snapshot. Quando o Snapshot muda, as hipoteses devem poder ser revistas.

## 9. Relacao com Objetivos Terapeuticos

O Clinical Snapshot ajuda a definir e revisar `TherapeuticObjective`.

Objetivos terapeuticos devem nascer do estado clinico atual, e nao de uma estrategia previamente escolhida.

O Snapshot deve ajudar a responder:

- quais sintomas precisam ser reduzidos;
- qual risco precisa ser controlado;
- qual dimensao funcional precisa ser preservada ou recuperada;
- qual efeito adverso precisa ser evitado ou monitorado;
- qual aspecto de qualidade de vida e prioritario;
- qual nivel de estabilidade e clinicamente realista neste momento.

Sem Snapshot, o objetivo terapeutico fica abstrato e menos rastreavel.

## 10. Relacao com Restricoes

O Clinical Snapshot deve registrar restricoes terapeuticas relevantes para o caso.

Restricoes podem incluir:

- contraindicações;
- interacoes medicamentosas;
- alergias;
- reacoes adversas graves previas;
- comorbidades;
- gestacao;
- lactacao;
- insuficiencia renal;
- insuficiencia hepatica;
- doenca cardiovascular;
- QT prolongado;
- epilepsia;
- risco suicida;
- risco de agressividade;
- delirium;
- intoxicacao;
- abstinencia;
- preferencias do paciente;
- limites de adesao ou monitorizacao.

Essas restricoes devem modificar ou bloquear comparacoes estrategicas quando necessario.

## 11. Papel no Clinical Operating Mind

O Clinical Snapshot e o ponto de partida do Clinical Operating Mind.

Ele alimenta:

- `Question Engine`, ao indicar perguntas e lacunas;
- `Diagnostic Reasoning`, ao organizar sintomas, sindromes e hipoteses;
- `Therapeutic Objective Engine`, ao situar objetivos;
- `Constraint Engine`, ao registrar limites;
- `Safety First Engine`, ao expor riscos obrigatorios;
- `Strategy Generation`, ao definir o contexto de possibilidades;
- `Strategy Comparison`, ao permitir comparacao situada;
- `Evidence Evaluation`, ao indicar quais evidencias sao aplicaveis;
- `Clinical Explanation`, ao oferecer dados rastreaveis;
- `Monitoring Engine`, ao definir o que acompanhar;
- `Longitudinal Follow-up`, ao permitir comparacao no tempo.

Sem Clinical Snapshot, o Clinical Operating Mind perde seu ponto de ancoragem clinica.

## 12. O que Nao Pertence ao Snapshot

O Clinical Snapshot nao deve conter:

- codigo;
- classes;
- APIs;
- estruturas de banco de dados;
- implementacao de motor;
- regras terapeuticas executaveis;
- prescricoes;
- decisoes finais do medico;
- recomendacoes automaticas;
- conhecimento cientifico completo;
- revisoes bibliograficas extensas;
- dados irrelevantes para o estado clinico atual;
- conclusoes sem justificativa;
- afirmacoes cientificas sem fonte;
- historico longitudinal completo sem sintese clinica.

O Snapshot nao e banco de conhecimento, prontuario completo, motor de decisao ou plano terapeutico final. Ele e a representacao clinica atual que permite raciocinar com seguranca.

## 13. Declaracao Final

O Clinical Snapshot e a fotografia clinica dinamica que ancora o raciocinio do PsychRx.

Ele organiza o estado atual do paciente, explicita sintomas, sindromes, hipoteses, objetivos, restricoes, riscos e incertezas, e permite que o Clinical Operating Mind pense de forma contextual, longitudinal, segura, explicavel e rastreavel.

No PsychRx, nenhuma estrategia deve ser comparada sem antes saber qual paciente, em qual estado clinico, com quais sintomas, quais hipoteses, quais objetivos e quais restricoes esta diante do sistema.
