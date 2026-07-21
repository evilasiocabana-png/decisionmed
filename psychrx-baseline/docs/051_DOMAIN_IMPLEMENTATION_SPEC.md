# 051 - Domain Implementation Spec

## 1. Objetivo

Este documento converte a arquitetura do domínio do PsychRx em especificações de implementação para futuras missões do Codex.

Ele não implementa código, não define linguagem, não cria classes e não escolhe framework. Ele descreve o que deverá ser implementado no futuro, quais contratos devem ser preservados, quais dependências são permitidas ou proibidas, quais validações são obrigatórias e quais testes deverão existir.

Esta especificação deve ser usada como contrato executável para o Codex: qualquer implementação futura do domínio deve obedecer a este documento.

## 2. Regras Gerais de Implementação

Toda implementação futura do domínio deve respeitar:

- Domain Layer independente de Application e Interface;
- nenhuma entidade clínica sem Ontologia;
- nenhuma regra terapêutica sem evidência rastreável;
- nenhuma estratégia sem objetivo terapêutico;
- nenhuma estratégia sem avaliação de segurança;
- nenhuma saída clínica sem explicabilidade;
- nenhum conhecimento científico hardcoded em motores;
- nenhuma interface decidindo lógica clínica;
- testes proporcionais ao risco;
- rastreabilidade de eventos e decisões.

## 3. Entidades

### Patient

Responsabilidade:

- representar a unidade clínica longitudinal central do PsychRx;
- agrupar trajetória clínica, snapshots, sintomas, hipóteses, objetivos, restrições, respostas e monitorização;
- servir como eixo de rastreabilidade de todo dado clínico individual.

Dependências permitidas:

- value objects clínicos;
- eventos de domínio relacionados ao paciente;
- conceitos do Domain Model.

Dependências proibidas:

- Application Layer;
- Interface Layer;
- banco de dados;
- API;
- evidência científica hardcoded;
- regra terapêutica executável.

Contratos:

- deve possuir identidade interna;
- deve permitir associação a múltiplos `ClinicalSnapshot`;
- deve preservar continuidade longitudinal;
- não deve conter decisão clínica final.

Validações:

- identidade obrigatória;
- consistência mínima dos dados demográficos quando presentes;
- proibição de dados clínicos sem vínculo com paciente.

Testes esperados:

- criação conceitual de paciente válido;
- rejeição de paciente sem identidade;
- associação de snapshots ao paciente;
- preservação de trajetória longitudinal;
- ausência de dependência com interface ou aplicação.

### ClinicalSnapshot

Responsabilidade:

- representar o estado clínico atual do paciente;
- organizar sintomas, síndromes, hipóteses, objetivos, restrições, riscos, dados ausentes e incertezas;
- ancorar raciocínio clínico, segurança e comparação estratégica.

Dependências permitidas:

- Patient;
- Symptom;
- Syndrome;
- DiagnosticHypothesis;
- TherapeuticObjective;
- TherapeuticRestriction;
- SafetyAlert;
- value objects clínicos.

Dependências proibidas:

- Interface Layer;
- Application Layer como fonte de significado;
- banco de dados;
- regras terapêuticas executáveis;
- prescrição.

Contratos:

- deve estar vinculado a um `Patient`;
- deve possuir momento de referência;
- deve declarar dados ausentes relevantes;
- deve diferenciar dado informado, hipótese, incerteza e alerta.

Validações:

- vínculo obrigatório com paciente;
- momento de referência obrigatório;
- dados ausentes críticos devem ser explicitados;
- não pode conter decisão clínica final.

Testes esperados:

- snapshot válido com paciente e data;
- snapshot identifica lacunas;
- snapshot aceita sintomas e hipóteses sem fechar diagnóstico;
- snapshot bloqueia estratégia se segurança mínima estiver ausente;
- snapshot não contém lógica de interface.

### Symptom

Responsabilidade:

- representar manifestação clínica observada, relatada ou monitorada;
- sustentar síndromes, hipóteses, objetivos e monitorização.

Dependências permitidas:

- Patient;
- ClinicalSnapshot;
- value objects de intensidade, duração, período e escore clínico.

Dependências proibidas:

- diagnóstico automático;
- estratégia terapêutica direta;
- interface;
- evidência hardcoded.

Contratos:

- deve ter nome ou descrição clínica;
- pode ter intensidade, frequência, duração e curso temporal;
- pode estar ativo, residual, remitido ou recorrente.

Validações:

- descrição obrigatória;
- intensidade, se presente, deve ser interpretável;
- curso temporal não pode contradizer momento do snapshot.

Testes esperados:

- registro de sintoma válido;
- sintoma sem descrição é inválido;
- sintoma não gera diagnóstico automaticamente;
- sintoma pode ser associado a monitorização.

### Syndrome

Responsabilidade:

- representar agrupamento clínico de sintomas;
- funcionar como ponte entre sintomas e hipóteses diagnósticas.

Dependências permitidas:

- Symptom;
- ClinicalSnapshot;
- DiagnosticHypothesis.

Dependências proibidas:

- diagnóstico definitivo automático;
- prescrição;
- regra terapêutica.

Contratos:

- deve ser composta por sintomas;
- deve informar incerteza quando aplicável;
- pode sustentar múltiplas hipóteses.

Validações:

- não deve existir sem sintomas associados;
- não deve ser tratada como diagnóstico final.

Testes esperados:

- síndrome formada por sintomas;
- síndrome sem sintomas é inválida;
- síndrome pode sustentar hipótese;
- síndrome não fecha diagnóstico.

### DiagnosticHypothesis

Responsabilidade:

- representar hipótese diagnóstica em avaliação;
- organizar critérios favoráveis, contrários, diferenciais, incertezas e nível de confiança.

Dependências permitidas:

- ClinicalSnapshot;
- Symptom;
- Syndrome;
- ConfidenceLevel.

Dependências proibidas:

- estratégia terapêutica automática;
- fechamento diagnóstico sem médico;
- interface;
- evidência hardcoded.

Contratos:

- deve possuir descrição;
- deve possuir nível de confiança;
- deve declarar critérios favoráveis e incertezas;
- pode possuir diferenciais.

Validações:

- descrição obrigatória;
- nível de confiança obrigatório;
- não pode ser convertida em diagnóstico final sem decisão médica documentada.

Testes esperados:

- hipótese válida com confiança;
- hipótese sem confiança é inválida;
- hipótese registra critérios favoráveis e contrários;
- hipótese pode ser revisada longitudinalmente.

### TherapeuticObjective

Responsabilidade:

- representar alvo clínico que orienta raciocínio e comparação estratégica;
- organizar objetivos primários, secundários, concorrentes, conflitos e critérios de sucesso.

Dependências permitidas:

- ClinicalSnapshot;
- DiagnosticHypothesis;
- Symptom;
- TherapeuticRestriction;
- MonitoringPlan.

Dependências proibidas:

- prescrição;
- escolha automática de estratégia;
- interface;
- regra terapêutica sem fonte.

Contratos:

- deve possuir descrição;
- deve ter prioridade;
- deve ter critério de sucesso;
- deve estar vinculado ao estado clínico.

Validações:

- objetivo sem vínculo clínico é inválido;
- objetivo sem critério de sucesso é incompleto;
- conflitos entre objetivos devem ser explicitados.

Testes esperados:

- objetivo primário válido;
- objetivo secundário subordinado;
- conflito entre objetivos identificado;
- estratégia sem objetivo deve ser rejeitada.

### TherapeuticRestriction

Responsabilidade:

- representar restrição clínica, farmacológica, contextual ou individual;
- modificar, reduzir ou bloquear estratégias terapêuticas.

Dependências permitidas:

- ClinicalSnapshot;
- Patient;
- EvidenceSource quando houver base científica;
- SafetyAlert.

Dependências proibidas:

- interface;
- decisão final;
- regra sem fonte quando terapêutica;
- conhecimento hardcoded.

Contratos:

- deve possuir tipo;
- deve possuir severidade ou impacto;
- deve indicar se é absoluta, relativa ou contextual;
- deve possuir justificativa.

Validações:

- restrição sem justificativa é inválida;
- restrição terapêutica baseada em ciência exige evidência rastreável;
- restrição crítica deve gerar ou alimentar SafetyAlert.

Testes esperados:

- restrição absoluta bloqueia estratégia;
- restrição relativa gera cautela;
- restrição sem fonte científica fica incompleta;
- dados ausentes críticos podem gerar restrição.

### TherapeuticStrategy

Responsabilidade:

- representar caminho terapêutico conceitual comparável;
- organizar benefícios, riscos, restrições, evidências, explicação e monitorização;
- nunca representar prescrição automática.

Dependências permitidas:

- TherapeuticObjective;
- TherapeuticRestriction;
- SafetyAlert;
- EvidenceSource;
- ClinicalExplanation;
- MonitoringPlan.

Dependências proibidas:

- existir sem objetivo;
- existir sem avaliação de segurança;
- prescrever;
- interface decidir conteúdo;
- evidência hardcoded.

Contratos:

- deve estar vinculada a objetivo terapêutico;
- deve registrar restrições consideradas;
- deve possuir justificativa;
- deve possuir rastreabilidade de evidência quando houver regra terapêutica;
- deve indicar incertezas.

Validações:

- estratégia sem objetivo é inválida;
- estratégia sem segurança avaliada é inválida;
- estratégia sem explicação não pode ser apresentada;
- estratégia com risco crítico deve ser bloqueada ou marcada como insegura.

Testes esperados:

- estratégia válida com objetivo, segurança e explicação;
- rejeição de estratégia sem objetivo;
- rejeição de estratégia sem avaliação de segurança;
- estratégia com conflito de evidência reduz força da conclusão.

### PsychopharmacologicalAgent

Responsabilidade:

- representar agente psicofarmacológico oficial;
- conectar classe, mecanismo, efeitos adversos, interações, contraindicações, evidências e monitorização.

Dependências permitidas:

- EvidenceSource;
- Knowledge Module;
- MonitoringPlan;
- TherapeuticRestriction.

Dependências proibidas:

- uso do termo `Drug` como nome canônico;
- prescrição automática;
- inclusão sem modelo oficial;
- inclusão sem fonte quando houver afirmação científica.

Contratos:

- deve possuir nome oficial;
- deve possuir classe ou categoria;
- deve possuir fonte para propriedades clínicas;
- deve registrar contraindicações e efeitos adversos quando conhecidos.

Validações:

- agente sem identidade é inválido;
- agente com afirmação clínica sem fonte é incompleto;
- agente não pode ser usado para prescrever por si só.

Testes esperados:

- agente válido com fonte;
- rejeição de agente sem identificação;
- propriedade clínica sem fonte é sinalizada;
- agente se conecta a restrições e monitorização.

### EvidenceSource

Responsabilidade:

- representar fonte científica rastreável;
- sustentar conhecimento, regras, alertas, estratégias e explicações.

Dependências permitidas:

- metadados de evidência;
- Evidence Traceability Policy.

Dependências proibidas:

- interface;
- decisão individual;
- application como origem de evidência.

Contratos:

- deve conter fonte, ano, tipo, qualidade, força da recomendação, data de revisão, status, conflitos e aplicabilidade.

Validações:

- ausência de qualquer campo obrigatório torna a evidência incompleta;
- status deve ser um dos oficiais;
- evidência `deprecated` não pode sustentar nova regra;
- `conflicting evidence` exige incerteza explícita.

Testes esperados:

- evidência válida com todos os metadados;
- evidência sem fonte é inválida;
- evidência deprecated não sustenta nova regra;
- conflito reduz força da recomendação.

### SafetyAlert

Responsabilidade:

- representar alerta de segurança clínica;
- sinalizar risco, bloqueio, cautela, encaminhamento ou monitorização.

Dependências permitidas:

- TherapeuticRestriction;
- ClinicalSnapshot;
- EvidenceSource;
- ClinicalExplanation.

Dependências proibidas:

- interface como origem;
- alerta sem justificativa;
- alerta sem rastreabilidade quando baseado em evidência.

Contratos:

- deve possuir severidade;
- deve possuir justificativa;
- deve indicar impacto sobre estratégia;
- deve indicar se bloqueia, alerta ou exige monitorização.

Validações:

- alerta crítico deve preceder comparação estratégica;
- alerta sem justificativa é inválido;
- alerta baseado em ciência exige fonte.

Testes esperados:

- alerta crítico bloqueia estratégia;
- alerta moderado reduz força da comparação;
- alerta sem fonte é incompleto quando científico;
- alerta gera ClinicalExplanation.

### ClinicalResponse

Responsabilidade:

- representar mudança clínica observada ao longo do tempo;
- alimentar monitorização e estabilização.

Dependências permitidas:

- Patient;
- ClinicalSnapshot;
- TherapeuticStrategy;
- MonitoringPlan.

Dependências proibidas:

- decisão automática;
- conclusão sem monitorização;
- interface.

Contratos:

- deve possuir momento de observação;
- deve indicar dimensão afetada;
- pode representar melhora, piora, resposta parcial, remissão, recaída, recorrência ou deterioração.

Validações:

- resposta sem referência temporal é incompleta;
- resposta não deve ser confundida automaticamente com estabilidade.

Testes esperados:

- resposta com data e dimensão;
- resposta parcial não vira estabilidade sustentada;
- recaída e recorrência são diferenciadas;
- deterioração gera necessidade de revisão.

### MonitoringPlan

Responsabilidade:

- representar acompanhamento necessário para avaliar segurança, resposta e estabilização.

Dependências permitidas:

- TherapeuticObjective;
- SafetyAlert;
- TherapeuticStrategy;
- ClinicalResponse.

Dependências proibidas:

- ordem clínica automática;
- prescrição;
- interface como fonte de conteúdo.

Contratos:

- deve indicar o que acompanhar;
- deve indicar por que acompanhar;
- deve estar vinculado a objetivo, risco, estratégia ou resposta.

Validações:

- monitorização sem justificativa é incompleta;
- risco identificado deve gerar monitorização quando aplicável;
- estabilidade sustentada exige acompanhamento suficiente.

Testes esperados:

- plano válido com parâmetro e justificativa;
- risco sem monitorização é sinalizado;
- estabilidade sem monitorização é rejeitada.

### ClinicalExplanation

Responsabilidade:

- representar justificativa rastreável de saída clínica;
- conectar dados, hipóteses, objetivos, restrições, evidências, riscos, incertezas e limites.

Dependências permitidas:

- ClinicalSnapshot;
- TherapeuticObjective;
- SafetyAlert;
- EvidenceSource;
- TherapeuticStrategy.

Dependências proibidas:

- texto decorativo sem rastreabilidade;
- decisão final;
- fonte inexistente;
- ocultar incerteza.

Contratos:

- deve indicar dados usados;
- deve indicar evidências;
- deve indicar incertezas;
- deve indicar limites;
- deve indicar papel do médico.

Validações:

- explicação sem dados usados é inválida;
- explicação baseada em ciência sem fonte é inválida;
- incerteza relevante deve ser declarada.

Testes esperados:

- explicação completa para estratégia;
- explicação inclui evidência e incerteza;
- ausência de explicação bloqueia saída clínica;
- explicação não prescreve.

### AuditRecord

Responsabilidade:

- representar registro auditável de uma análise, evento ou saída;
- permitir reconstrução do caminho clínico e científico.

Dependências permitidas:

- eventos de domínio;
- EvidenceSource;
- ClinicalSnapshot;
- ClinicalExplanation;
- versões.

Dependências proibidas:

- decidir conduta;
- alterar resultado;
- depender de interface como fonte de verdade.

Contratos:

- deve registrar evento, momento, origem, dados relevantes, versões, evidências e saída;
- deve ser preservável para reconstrução.

Validações:

- saída clínica sem audit record é incompleta;
- evento sem momento é inválido;
- versão de evidência deve ser registrada quando aplicável.

Testes esperados:

- registro auditável criado para saída clínica;
- reconstrução de decisão a partir do registro;
- audit não altera decisão;
- audit não depende da interface.

## 4. Value Objects

Value objects devem ser usados para medidas, classificações e descritores sem identidade própria.

### Contrato geral

Responsabilidade:

- representar valor clínico ou científico com significado preciso.

Dependências permitidas:

- entidades do domínio que os utilizam.

Dependências proibidas:

- application;
- interface;
- infraestrutura;
- regra executável externa ao domínio.

Validações gerais:

- valor obrigatório quando o objeto existir;
- unidade obrigatória quando aplicável;
- momento de aferição obrigatório quando clinicamente relevante;
- faixa ou categoria deve ser válida quando definida.

Testes esperados:

- criação de valor válido;
- rejeição de valor sem unidade quando unidade for obrigatória;
- comparação por valor e não por identidade;
- imutabilidade conceitual no momento registrado.

Value objects mínimos:

- `Dose`;
- `Weight`;
- `Height`;
- `BMI`;
- `QTInterval`;
- `ClinicalScore`;
- `RenalFunction`;
- `HepaticFunction`;
- `BloodPressure`;
- `HeartRate`;
- `EvidenceQuality`;
- `RecommendationStrength`;
- `RiskSeverity`;
- `ConfidenceLevel`;
- `ClinicalPeriod`;
- `EvidenceStatus`;
- `ClinicalJustification`;
- `SourceReference`.

## 5. Aggregates

### Patient Aggregate

Responsabilidade:

- preservar consistência longitudinal do paciente.

Dependências permitidas:

- Patient;
- ClinicalSnapshot;
- eventos clínicos.

Dependências proibidas:

- interface;
- application como regra de domínio;
- persistência concreta.

Contratos:

- todo dado individual deve retornar ao Patient;
- snapshots pertencem à trajetória do Patient.

Validações:

- Patient obrigatório para dados clínicos;
- trajetória não pode perder histórico relevante.

Testes esperados:

- paciente agrega snapshots;
- evento clínico se vincula ao paciente;
- ausência de paciente invalida dado clínico individual.

### ClinicalSnapshot Aggregate

Responsabilidade:

- preservar consistência do estado clínico atual.

Contratos:

- deve consolidar sintomas, síndromes, hipóteses, objetivos, restrições e incertezas.

Validações:

- snapshot incompleto deve declarar lacunas;
- estratégia não pode usar snapshot desatualizado sem validação.

Testes esperados:

- snapshot completo;
- snapshot com lacunas explícitas;
- comparação bloqueada por snapshot inseguro.

### TherapeuticObjective Aggregate

Responsabilidade:

- preservar direção clínica da estratégia.

Contratos:

- objetivos primários e secundários devem ser distinguíveis;
- conflitos devem ser registrados;
- critério de sucesso obrigatório.

Validações:

- estratégia sem objetivo é inválida;
- objetivo sem critério de sucesso é incompleto.

Testes esperados:

- objetivo primário válido;
- conflito entre objetivos detectado;
- estratégia rejeitada sem objetivo.

### Safety Aggregate

Responsabilidade:

- preservar avaliação de segurança antes da estratégia.

Contratos:

- alertas críticos devem bloquear ou limitar comparação;
- restrições devem possuir justificativa.

Validações:

- segurança obrigatória antes de estratégia;
- alerta sem justificativa inválido.

Testes esperados:

- risco crítico bloqueia estratégia;
- alerta moderado permite cautela;
- segurança ausente bloqueia comparação.

### Strategy Aggregate

Responsabilidade:

- preservar coerência de uma estratégia conceitual.

Contratos:

- estratégia exige objetivo, segurança, evidência quando aplicável e explicação.

Validações:

- ausência de qualquer item obrigatório impede apresentação.

Testes esperados:

- estratégia válida completa;
- estratégia sem explicação é rejeitada;
- estratégia com evidência conflitante explicita incerteza.

### Evidence Aggregate

Responsabilidade:

- preservar integridade científica de fontes.

Contratos:

- metadados obrigatórios completos;
- status oficial.

Validações:

- fonte sem metadados é inválida;
- deprecated não sustenta regra nova.

Testes esperados:

- fonte validada;
- fonte conflitante reduz recomendação;
- fonte sem ano rejeitada.

### Monitoring Aggregate

Responsabilidade:

- preservar acompanhamento longitudinal.

Contratos:

- monitorização vinculada a objetivo, risco, estratégia ou resposta.

Validações:

- estabilidade sustentada exige monitorização suficiente.

Testes esperados:

- monitorização acompanha resposta;
- ausência de monitorização impede estabilidade sustentada.

## 6. Domain Services

### Contrato geral

Domain services devem coordenar regras conceituais que envolvem múltiplas entidades.

Dependências permitidas:

- Domain;
- Knowledge;
- Evidence;
- Safety, quando aplicável.

Dependências proibidas:

- Interface;
- dashboard;
- infraestrutura;
- evidência hardcoded;
- prescrição.

Validações:

- não podem violar invariantes;
- devem produzir explicação ou evento quando gerarem saída clínica relevante.

Testes esperados:

- serviço respeita dependências permitidas;
- serviço não acessa interface;
- serviço não contém evidência hardcoded;
- serviço preserva rastreabilidade.

Serviços previstos:

- `ClinicalSnapshotCoordination`;
- `DiagnosticReasoningService`;
- `TherapeuticObjectiveService`;
- `ConstraintEvaluationService`;
- `ClinicalSafetyService`;
- `StrategyReasoningService`;
- `EvidenceTraceabilityService`;
- `ClinicalExplanationService`;
- `MonitoringAndStabilizationService`;
- `AuditTraceService`.

## 7. Domain Events

### Contrato geral

Eventos de domínio devem registrar mudanças relevantes sem decidir conduta.

Dependências permitidas:

- entidades e aggregates envolvidos;
- metadados de tempo e versão.

Dependências proibidas:

- interface;
- comandos de aplicação;
- ações terapêuticas automáticas.

Validações:

- todo evento deve ter momento;
- todo evento deve ter origem conceitual;
- eventos clínicos relevantes devem ser auditáveis.

Testes esperados:

- evento emitido em mudança relevante;
- evento auditável;
- evento não altera conduta;
- evento preserva vínculo com Patient quando aplicável.

Eventos previstos:

- `PatientUpdated`;
- `ClinicalSnapshotCreated`;
- `ClinicalSnapshotUpdated`;
- `SymptomRegistered`;
- `SyndromeIdentified`;
- `DiagnosticHypothesisCreated`;
- `DiagnosticHypothesisRevised`;
- `TherapeuticObjectiveDefined`;
- `TherapeuticObjectiveReprioritized`;
- `TherapeuticRestrictionIdentified`;
- `SafetyAlertIssued`;
- `EvidenceSourceLinked`;
- `EvidenceStatusChanged`;
- `TherapeuticStrategyGenerated`;
- `TherapeuticStrategyCompared`;
- `ClinicalExplanationGenerated`;
- `MonitoringPlanDefined`;
- `ClinicalResponseObserved`;
- `RemissionObserved`;
- `RelapseDetected`;
- `RecurrenceDetected`;
- `ClinicalDeteriorationDetected`;
- `StabilizationStatusUpdated`;
- `AuditRecordCreated`.

## 8. Invariantes

Invariantes devem ser tratadas como critérios obrigatórios de implementação e teste.

### Invariantes clínicas

- nenhum dado clínico individual sem Patient;
- nenhum raciocínio sem ClinicalSnapshot;
- nenhuma hipótese sem ConfidenceLevel;
- nenhuma estratégia sem TherapeuticObjective;
- nenhuma estratégia sem Safety;
- nenhuma regra terapêutica sem EvidenceSource;
- nenhuma recomendação sem ClinicalExplanation;
- nenhuma estabilidade sustentada sem MonitoringPlan suficiente;
- nenhuma saída clínica sem AuditRecord.

### Invariantes arquiteturais

- Domain não depende de Application;
- Domain não depende de Interface;
- Interface não decide lógica clínica;
- Knowledge não contém regra executável;
- motores clínicos não contêm evidência hardcoded;
- Evidence não depende de Interface;
- Audit registra, mas não decide.

### Testes esperados para invariantes

- testes unitários de invariantes;
- testes de contrato entre módulos;
- testes de cenário clínico simulado;
- testes de segurança;
- testes de rastreabilidade de evidência;
- testes de não-regressão para violações corrigidas.

## 9. Checklist para Codex

Antes de implementar qualquer elemento deste domínio, Codex deve confirmar:

- o elemento existe na Ontologia ou foi aprovado;
- o nome segue `NAMING_CONVENTIONS.md`;
- as dependências respeitam `LAYER_DEPENDENCY_RULES.md`;
- o módulo respeita `MODULE_BOUNDARIES.md`;
- evidência necessária segue `EVIDENCE_TRACEABILITY_POLICY.md`;
- segurança segue `CLINICAL_SAFETY_CONTRACT.md`;
- testes seguem `TESTING_POLICY.md`;
- a missão respeita `CODEX_DEFINITION_OF_DONE.md`;
- mudança estrutural possui ADR quando aplicável.

## 10. Critério de Aceite Futuro

Uma implementação futura do domínio só deve ser aceita se:

- entidades possuem contratos e validações implementados;
- value objects preservam significado e validação;
- aggregates preservam invariantes;
- domain services não violam dependências;
- domain events são auditáveis;
- todos os elementos possuem testes esperados;
- nenhuma evidência clínica está hardcoded;
- nenhuma interface decide conduta;
- rastreabilidade e explicabilidade são preservadas.

## 11. Declaração Final

Esta especificação transforma o Domain Model do PsychRx em contrato de implementação para o Codex.

Ela não cria software, mas define o que qualquer software futuro deverá respeitar: responsabilidades claras, dependências controladas, contratos explícitos, validações obrigatórias, testes proporcionais e invariantes clínicas preservadas.

No PsychRx, implementar o domínio não é apenas criar estruturas. É proteger o raciocínio clínico, a segurança, a evidência, a explicabilidade e a decisão médica final.
