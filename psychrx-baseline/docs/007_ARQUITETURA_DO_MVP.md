# 007 - Arquitetura do MVP

## 1. Visão geral da arquitetura

O MVP do PsychRx deve ser uma plataforma modular de apoio ao raciocínio médico em psicofarmacologia. Sua arquitetura deve colocar o paciente no centro, organizar dados clínicos relevantes, aplicar camadas explícitas de segurança, consultar conhecimento científico rastreável e apresentar ao médico uma análise explicável.

O sistema não deve funcionar como prescritor automático. Sua finalidade é apoiar o julgamento clínico, não substituí-lo. Toda saída relevante deve deixar claro o caminho do raciocínio, as fontes utilizadas, as incertezas identificadas e os limites da análise.

A arquitetura inicial deve separar quatro domínios:

- dados clínicos do paciente;
- conhecimento científico versionado;
- motores de raciocínio e segurança;
- interface de revisão e decisão médica.

## 2. Objetivo do MVP

O objetivo do MVP é validar a capacidade do PsychRx de receber dados clínicos estruturados, organizar esses dados de forma clinicamente útil, identificar riscos psicofarmacológicos relevantes, comparar possibilidades de estratégia sem prescrever automaticamente e explicar o raciocínio com base em fontes rastreáveis.

O MVP deve demonstrar que o sistema consegue apoiar o médico em três dimensões centrais:

- compreensão organizada do caso;
- identificação de riscos e pontos de atenção;
- explicação transparente das relações entre dados do paciente, conhecimento científico e possibilidades terapêuticas.

## 3. O que o MVP deve fazer

O MVP deve:

- registrar dados clínicos essenciais de um paciente em formato estruturado;
- manter o paciente como unidade central de análise;
- organizar hipóteses, sintomas, diagnósticos, medicamentos, comorbidades, histórico terapêutico, riscos e objetivos clínicos;
- executar verificações iniciais de segurança clínica;
- identificar contraindicações, interações, alertas e fatores de risco conhecidos;
- comparar estratégias psicofarmacológicas em nível conceitual, sem converter comparação em prescrição;
- explicar por que determinado risco, alerta ou estratégia foi sinalizado;
- vincular cada informação científica a uma fonte;
- registrar versões de conhecimento, regras, algoritmos e resultados;
- produzir logs e trilhas de auditoria para cada análise;
- deixar claro que o médico é sempre o decisor final.

## 4. O que o MVP não deve fazer

O MVP não deve:

- prescrever medicamentos;
- indicar dose, posologia ou ajuste individual como decisão final;
- substituir avaliação médica;
- responder como ferramenta assistencial autônoma para pacientes;
- gerar conduta clínica sem justificativa;
- apresentar informação científica sem fonte;
- misturar conhecimento científico diretamente no código;
- ocultar incertezas, conflitos de evidência ou limitações;
- transformar alertas em decisões obrigatórias;
- automatizar trocas, suspensões ou combinações medicamentosas;
- criar funcionalidades clínicas fora do escopo de apoio ao raciocínio.

## 5. Camadas do sistema

A arquitetura do MVP deve ser organizada em camadas independentes:

1. Camada de apresentação: interface usada pelo médico para inserir, revisar e interpretar dados.
2. Camada de API: contrato de comunicação entre frontend, backend, motores e repositórios.
3. Camada de aplicação: coordena fluxos, valida entradas e organiza respostas.
4. Camada de segurança clínica: executa verificações obrigatórias antes de qualquer análise estratégica.
5. Camada de motores clínicos: aplica regras, modelos de comparação, checagens e raciocínios estruturados.
6. Camada de conhecimento científico: armazena conhecimento versionado, fontes, evidências e regras clínicas declarativas.
7. Camada de dados clínicos: armazena dados do paciente, episódios, análises, auditorias e histórico.
8. Camada de IA: auxilia explicação, síntese e navegação do conhecimento sob controle de rastreabilidade.
9. Camada de logs, auditoria e observabilidade: registra eventos, decisões, versões e falhas.

## 6. Módulos principais

O MVP deve conter os seguintes módulos principais:

- módulo de paciente;
- módulo de dados clínicos;
- módulo de medicamentos;
- módulo de diagnósticos e problemas clínicos;
- módulo de objetivos terapêuticos;
- módulo de riscos e contraindicações;
- módulo de interações;
- módulo de histórico terapêutico;
- módulo de análise psicofarmacológica;
- módulo de explicabilidade;
- módulo de fontes e evidências;
- módulo de auditoria;
- módulo de gestão de versões.

Cada módulo deve possuir fronteiras claras e contratos explícitos com os demais.

## 7. Motores clínicos necessários

O MVP deve prever motores clínicos especializados, sem transformá-los em prescritores automáticos:

- motor de segurança clínica;
- motor de interações medicamentosas;
- motor de contraindicações;
- motor de perfil farmacológico;
- motor de objetivos terapêuticos;
- motor de histórico de resposta e tolerabilidade;
- motor de risco clínico;
- motor de comparação de estratégias;
- motor de explicabilidade;
- motor de rastreabilidade científica.

O motor de segurança clínica deve ser a primeira camada executada em qualquer fluxo analítico. Nenhuma comparação estratégica deve ser apresentada antes da análise de segurança.

## 8. Fluxo de dados

O fluxo de dados do MVP deve seguir esta sequência lógica:

1. O médico registra ou atualiza os dados do paciente.
2. O sistema valida completude, consistência e formato dos dados.
3. A camada de segurança clínica identifica riscos críticos, contraindicações, interações e lacunas relevantes.
4. Os motores clínicos consultam o banco de conhecimento científico versionado.
5. O sistema organiza uma leitura estruturada do caso.
6. O sistema compara estratégias possíveis em nível de raciocínio, sem prescrever.
7. A camada de explicabilidade gera justificativas com fontes, regras e versões utilizadas.
8. A API entrega a resposta ao frontend.
9. Logs e auditoria registram entrada, versões, motores acionados, fontes consultadas e saída produzida.
10. O médico revisa a análise e decide fora do sistema ou com apoio não vinculante do sistema.

## 9. Separação entre conhecimento científico e algoritmo

O conhecimento científico deve permanecer separado do código e dos algoritmos executáveis. O código deve saber consultar, interpretar e aplicar conhecimento, mas não deve embutir conteúdo científico de forma rígida.

Essa separação é obrigatória para:

- permitir atualização científica sem reescrever o sistema;
- manter rastreabilidade entre resultado e fonte;
- auditar mudanças de evidência;
- comparar versões de conhecimento;
- reduzir risco de decisões opacas;
- permitir revisão científica independente da engenharia de software.

O algoritmo deve operar sobre estruturas de conhecimento declarativas, versionadas e auditáveis.

## 10. Banco de conhecimento

O banco de conhecimento deve armazenar informação científica e clínica estruturada, incluindo:

- classes de psicofármacos;
- perfis farmacodinâmicos e farmacocinéticos;
- indicações reconhecidas;
- contraindicações;
- interações;
- efeitos adversos;
- fatores de risco;
- objetivos terapêuticos;
- escalas e critérios clínicos;
- protocolos e diretrizes;
- níveis de evidência;
- fontes bibliográficas;
- versões e datas de revisão.

Nenhuma informação do banco de conhecimento deve existir sem fonte associada, nível de evidência quando aplicável e histórico de versão.

## 11. Banco clínico

O banco clínico deve armazenar dados relacionados ao paciente e ao uso operacional do sistema. Deve incluir:

- identificação mínima necessária do paciente;
- dados clínicos estruturados;
- diagnósticos, hipóteses e problemas ativos;
- medicamentos atuais e prévios;
- histórico de resposta, tolerabilidade e eventos adversos;
- comorbidades e fatores de risco;
- objetivos terapêuticos;
- análises realizadas;
- logs clínicos;
- trilhas de auditoria;
- versões de conhecimento utilizadas em cada análise.

O banco clínico não deve conter conhecimento científico como regra primária. Ele deve referenciar o banco de conhecimento quando uma análise depender de evidência científica.

## 12. API

A API deve funcionar como fronteira formal entre interface, backend, motores clínicos, IA e repositórios de dados. Ela deve expor contratos claros para:

- criação e atualização de dados do paciente;
- envio de dados para análise;
- consulta de resultados;
- recuperação de justificativas;
- consulta de fontes;
- registro de ações;
- auditoria;
- versionamento.

A API deve impedir que o frontend acesse diretamente motores clínicos ou bancos internos. Toda resposta de análise deve incluir estado de segurança, justificativas, fontes e versão dos componentes utilizados.

## 13. Frontend

O frontend deve ser a superfície de trabalho do médico. Ele deve priorizar clareza, revisão, comparação e rastreabilidade.

O frontend deve:

- apresentar o paciente como centro da tela e do fluxo;
- permitir inserção estruturada de dados clínicos;
- exibir lacunas de informação;
- diferenciar dados informados, inferências e conhecimento científico;
- apresentar alertas de segurança antes de comparações estratégicas;
- mostrar justificativas e fontes;
- permitir revisão médica;
- evitar linguagem prescritiva;
- deixar explícito que a decisão final é do médico.

O frontend não deve induzir o usuário a aceitar uma conduta automática.

## 14. Backend

O backend deve coordenar a aplicação, validar entradas, acionar motores, consultar conhecimento, consolidar respostas e registrar auditoria.

O backend deve:

- aplicar validações de consistência;
- controlar permissões;
- orquestrar a execução dos motores clínicos;
- garantir que segurança clínica seja avaliada primeiro;
- consultar o banco de conhecimento;
- registrar versões utilizadas;
- montar respostas explicáveis;
- gerar logs e trilhas de auditoria;
- impedir saídas sem justificativa ou fonte.

O backend não deve conter conhecimento científico fixo como lógica permanente. Seu papel é orquestrar, validar e aplicar conhecimento versionado.

## 15. IA

A IA no MVP deve ter papel auxiliar e controlado. Ela pode apoiar síntese, explicação, organização textual, busca semântica e comparação argumentativa, desde que suas respostas sejam ancoradas em dados estruturados e fontes rastreáveis.

A IA não deve:

- prescrever;
- inventar fonte;
- criar recomendação sem base rastreável;
- ocultar incerteza;
- sobrepor-se aos motores de segurança;
- decidir pelo médico.

Toda saída de IA deve ser marcada como síntese assistiva, e não como decisão clínica autônoma.

## 16. Logs

O MVP deve registrar logs técnicos e clínicos de forma separada, respeitando privacidade e finalidade.

Logs técnicos devem incluir:

- chamadas de API;
- erros;
- desempenho;
- eventos de integração;
- falhas de validação.

Logs clínicos devem incluir:

- dados usados na análise;
- motores acionados;
- alertas gerados;
- fontes consultadas;
- versões utilizadas;
- resposta entregue;
- usuário responsável pela ação.

Logs não devem expor dados sensíveis além do necessário para auditoria e suporte.

## 17. Auditoria

A auditoria deve permitir reconstruir qualquer análise do sistema. Para cada resultado, deve ser possível responder:

- quais dados do paciente foram usados;
- qual versão do conhecimento científico foi consultada;
- quais motores foram executados;
- quais regras ou evidências foram acionadas;
- quais fontes justificaram a resposta;
- quais alertas foram apresentados;
- qual usuário realizou a ação;
- quando a análise foi gerada;
- qual saída foi exibida ao médico.

A auditoria deve ser tratada como requisito central do MVP, não como complemento posterior.

## 18. Segurança

Segurança no PsychRx inclui segurança da informação e segurança clínica.

A segurança da informação deve prever:

- controle de acesso;
- proteção de dados sensíveis;
- segregação de permissões;
- registro de eventos;
- integridade dos dados;
- prevenção de acesso indevido.

A segurança clínica deve prever:

- alertas críticos antes de qualquer estratégia;
- identificação de contraindicações;
- identificação de interações relevantes;
- sinalização de dados ausentes;
- bloqueio de respostas sem justificativa;
- bloqueio de informação sem fonte;
- comunicação explícita de incertezas.

Segurança clínica deve ser a primeira camada de análise.

## 19. Rastreabilidade

Rastreabilidade total é requisito obrigatório. Cada saída do sistema deve apontar para:

- dados de entrada;
- regras acionadas;
- fontes científicas;
- versão do banco de conhecimento;
- versão dos motores clínicos;
- versão do algoritmo de orquestração;
- data e hora da análise;
- usuário ou contexto de execução.

Uma análise sem rastreabilidade suficiente deve ser considerada incompleta.

## 20. Explicabilidade

O MVP deve explicar o raciocínio antes de apresentar qualquer comparação estratégica. A explicabilidade deve responder:

- o que foi identificado;
- por que foi identificado;
- quais dados do paciente sustentam a análise;
- qual conhecimento científico foi usado;
- qual fonte sustenta a afirmação;
- qual é o nível de certeza ou limitação;
- o que permanece pendente para julgamento médico.

Nenhuma recomendação, alerta ou comparação deve aparecer sem justificativa.

## 21. Versionamento

O MVP deve versionar:

- banco de conhecimento;
- fontes científicas;
- regras clínicas;
- motores clínicos;
- modelos de IA utilizados;
- contratos de API;
- estrutura de dados clínicos;
- documentos de arquitetura;
- resultados de análises quando clinicamente relevante.

O versionamento deve permitir comparar resultados antigos com resultados gerados após atualização científica ou técnica.

## 22. Escalabilidade futura

A arquitetura do MVP deve permitir evolução futura para:

- novos motores clínicos;
- novos domínios da psicofarmacologia;
- ampliação do banco de conhecimento;
- integração com prontuários;
- revisão científica colaborativa;
- GPTs especializados de pesquisa;
- GPTs clínicos futuros sob governança estrita;
- camadas avançadas de explicabilidade;
- validação prospectiva;
- auditoria regulatória mais robusta.

Essa escalabilidade deve vir da modularidade, da separação entre conhecimento e algoritmo e da existência de contratos claros entre módulos.

## 23. Riscos arquiteturais

Os principais riscos arquiteturais do MVP são:

- misturar conhecimento científico com código;
- permitir saída sem fonte;
- permitir recomendação sem justificativa;
- transformar comparação em prescrição;
- tratar IA como decisor clínico;
- criar módulos fortemente acoplados;
- registrar dados sem auditoria adequada;
- gerar alertas sem explicar sua origem;
- não versionar conhecimento e motores;
- não diferenciar dados do paciente, inferência e evidência científica;
- priorizar estratégia antes de segurança;
- ocultar lacunas de informação clínica.

Cada risco deve ser tratado como restrição de arquitetura e não apenas como preocupação de produto.

## 24. Decisões pendentes

As seguintes decisões devem permanecer pendentes nesta etapa:

- linguagem de programação;
- framework de frontend;
- framework de backend;
- banco de dados;
- infraestrutura de deploy;
- provedor de autenticação;
- modelo específico de IA;
- formato final do banco de conhecimento;
- padrão formal de representação de regras clínicas;
- estrutura definitiva dos contratos de API;
- critérios de validação clínica do MVP;
- governança de atualização científica;
- política final de privacidade e retenção de dados;
- escopo regulatório inicial;
- processo de revisão médica das saídas.

Essas decisões devem ser tomadas apenas após validação da arquitetura conceitual, dos limites clínicos e dos requisitos de segurança, rastreabilidade e explicabilidade.
