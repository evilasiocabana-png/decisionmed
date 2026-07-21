# DecisionMEd — análise de viabilidade para fluxos por especialidade

## Conclusão executiva

É tecnicamente possível construir o DecisionMEd como uma plataforma de apoio à decisão com um fluxo próprio para cada especialidade, usando o PsychRx como primeiro pacote clínico.

A estratégia correta não é duplicar o PsychRx para cada área. O caminho escalável é:

```text
Plataforma clínica comum
  + contrato único de pacote de especialidade
  + conhecimento científico versionado
  + módulos e regras específicos de cada especialidade
```

O maior risco não é programação. Os gargalos são validação científica, manutenção editorial, segurança clínica, rastreabilidade e revisão por especialistas.

## O que o PsychRx já prova

O PsychRx já implementa o esqueleto de um fluxo clínico progressivo:

1. contexto da consulta;
2. população e condições especiais;
3. condição ou hipótese de referência;
4. fenótipo atual;
5. sintomas predominantes;
6. objetivos terapêuticos;
7. medicação atual;
8. segurança essencial;
9. segurança aguda;
10. perfil farmacológico desejado;
11. restrições;
12. decisão do médico;
13. monitorização e reavaliação.

O repositório também já contém:

- separação conceitual entre domínio, conhecimento, evidência, raciocínio, segurança, aplicação, interface e auditoria;
- motor de segurança e bloqueios;
- rastreabilidade de evidências;
- contratos de explicação e monitorização;
- 83 registros na matriz farmacológica principal;
- 1.444 combinações na matriz de estratégia/dose/contexto;
- 332 registros de evidência por população;
- 347 relações entre medicamentos e contextos clínicos;
- 249 testes automatizados passando;
- matriz de cobertura psiquiátrica com 51 tópicos: 17 cobertos estruturalmente, 13 parciais, 12 lacunas relevantes e 9 apenas contextuais.

Isso demonstra uma base técnica real, mas ainda não um produto clínico liberado. A própria governança registra o aplicativo como read-only, sem banco de dados e sem autorização para prescrição, runtime clínico ou IA clínica.

## Problema que precisa ser corrigido antes de escalar

O protótipo atual tem parte do conhecimento e do comportamento clínico no frontend:

- listas de medicamentos preferidos por eixo;
- teoria resumida por doença;
- ramificações de casos por texto do diagnóstico;
- opções clínicas e parte da lógica de apresentação.

O arquivo `interfaces/web/static/app.js` tem aproximadamente 3.966 linhas. Replicar esse arquivo por especialidade produziria divergência científica, bugs e manutenção impossível.

Antes de criar a segunda especialidade, esses elementos precisam virar dados versionados e contratos consumidos pela interface.

## Arquitetura recomendada

```text
DecisionMEd Platform
├── Identidade, usuários e permissões
├── Clinical Case / Snapshot
├── Orquestrador de fluxo
├── Motor de perguntas e dados ausentes
├── Motor diagnóstico não autônomo
├── Motor de segurança e red flags
├── Motor de restrições e interações
├── Motor de estratégias
├── Motor de evidência e citações
├── Motor de explicação
├── Monitorização longitudinal
├── Auditoria e versionamento
├── Busca clínica universal
└── Specialty Pack Registry
    ├── Psychiatry Pack (PsychRx)
    ├── Cardiology Pack
    ├── Endocrinology Pack
    ├── Pediatrics Pack
    └── ...
```

### Contrato de um Specialty Pack

Cada especialidade deve fornecer o mesmo conjunto de objetos:

```text
specialty_manifest
scope_and_exclusions
intake_schema
red_flag_rules
clinical_axes
condition_catalog
diagnostic_criteria
differential_graph
test_and_exam_catalog
scores_and_calculators
treatment_strategy_catalog
medication_and_procedure_links
referral_and_admission_rules
monitoring_plans
patient_guidance
evidence_sources
editorial_review
version_and_expiry
clinical_test_scenarios
```

A interface monta o fluxo com esses contratos. Ela não contém conhecimento clínico próprio.

## Fluxo clínico comum a todas as especialidades

```text
Entrada do caso
  -> triagem e risco imediato
  -> contexto populacional
  -> queixa e trajetória temporal
  -> exame e dados objetivos
  -> lacunas que precisam ser perguntadas
  -> hipóteses e diferenciais
  -> critérios e exames necessários
  -> objetivos clínicos
  -> restrições e contraindicações
  -> opções comparáveis
  -> decisão confirmada pelo médico
  -> plano e monitorização
  -> evolução longitudinal e reavaliação
```

O fluxo deve poder parar quando houver emergência, dado essencial ausente, conflito de evidência ou risco não avaliado.

## Mapa inicial das especialidades

| Especialidade/pacote | Núcleo específico do fluxo | Segurança crítica | Prioridade sugerida |
| --- | --- | --- | --- |
| Psiquiatria | fenótipo, risco, psicofarmacologia, resposta, tolerabilidade | suicídio, mania, psicose, intoxicação, interações | Onda 1 — já existe |
| Medicina de família | motivo principal, prevenção, multimorbidade, coordenação | sinais de alarme e encaminhamento | Onda 1 |
| Cardiologia | dor/dispneia/palpitação, ECG, risco, função ventricular | síndrome coronariana, arritmia instável, choque | Onda 2 |
| Endocrinologia | sintomas, metabolismo, hormônios, metas e complicações | crise adrenal, cetoacidose, hipoglicemia | Onda 2 |
| Neurologia | início/tempo, topografia, exame neurológico, imagem | AVC, estado de mal, meningismo | Onda 2 |
| Pediatria | idade/peso, desenvolvimento, dose, hidratação, vacinação | deterioração rápida, sepse, abuso | Onda 2 |
| Infectologia | foco, gravidade, hospedeiro, exposição, resistência | sepse, isolamento, antimicrobiano inadequado | Onda 3 |
| Pneumologia | dispneia/tosse, espirometria, oxigenação, imagem | insuficiência respiratória, TEP | Onda 3 |
| Nefrologia | volume, função renal, eletrólitos, urina e diálise | hipercalemia, edema pulmonar, lesão renal aguda | Onda 3 |
| Gastro/Hepatologia | dor, sangramento, função hepática, endoscopia/imagem | hemorragia, abdome agudo, encefalopatia | Onda 3 |
| Ginecologia | ciclo, dor, sangramento, sexualidade, rastreamento | hemorragia, torção, gravidez ectópica | Onda 3 |
| Obstetrícia | idade gestacional, bem-estar materno-fetal, trabalho de parto | eclâmpsia, hemorragia, sepse obstétrica | Onda 4 |
| Geriatria | funcionalidade, cognição, fragilidade, polifarmácia | delirium, quedas, iatrogenia | Onda 3 |
| Reumatologia | padrão inflamatório, articulações, autoanticorpos, órgãos | vasculite e acometimento orgânico grave | Onda 4 |
| Hematologia | hemograma, coagulação, citopenias, trombose | sangramento, neutropenia febril, trombose grave | Onda 4 |
| Dermatologia | morfologia, distribuição, tempo, exposição | necrose, anafilaxia, reação medicamentosa grave | Onda 3 |
| Urologia | dor, obstrução, infecção, função sexual, imagem | retenção, torção, sepse urinária | Onda 4 |
| Ortopedia | mecanismo, exame neurovascular, imagem, função | síndrome compartimental, fratura exposta | Onda 4 |
| Cirurgia geral | dor, estabilidade, exame abdominal, imagem | abdome agudo, sepse e hemorragia | Onda 4 |
| Emergência | ABCDE, síndrome, gravidade, intervenção e destino | todo risco tempo-dependente | Onda 5 |
| Terapia intensiva | suporte orgânico, tendências, ventilação, drogas vasoativas | falência orgânica e deterioração contínua | Onda 5 |
| Anestesiologia | risco pré-operatório, via aérea, plano anestésico | via aérea difícil, hipertermia, instabilidade | Onda 5 |
| Oncologia | tumor/estágio, tratamento, toxicidades, objetivo de cuidado | neutropenia, lise tumoral, compressão medular | Onda 5 |
| Cuidados paliativos | sintomas, prognóstico, valores, capacidade, família | sofrimento refratário e conflitos de decisão | Onda 3 |
| Oftalmologia | acuidade, dor, olho vermelho, fundo e pressão | perda visual aguda, glaucoma agudo | Onda 4 |
| Otorrinolaringologia | via aérea, ouvido, nariz, garganta, equilíbrio | obstrução de via aérea e complicações infecciosas | Onda 4 |

As ondas indicam ordem de desenvolvimento, não importância clínica. Emergência e UTI aparecem mais tarde porque exigem validação, integração e segurança muito superiores.

## Componentes que devem ser globais, não repetidos

- cadastro e identidade do paciente;
- idade, peso, gestação, lactação, função renal e hepática;
- alergias;
- medicamentos em uso;
- interações;
- sinais vitais e exames laboratoriais;
- mecanismos de red flag;
- favoritos, anotações e histórico;
- busca;
- referências e evidência;
- controle editorial;
- auditoria;
- autenticação, cobrança e permissões;
- funcionamento offline e sincronização;
- consentimento, privacidade e proteção de dados.

## Dois produtos que não devem ser confundidos

### DecisionMEd Reference

Biblioteca, bulas, calculadoras, scores, protocolos, pesquisa e conteúdo educacional. Pode chegar ao mercado antes, desde que o conteúdo seja próprio, licenciado e revisado.

### DecisionMEd Flow

Fluxo interativo dependente do caso, com segurança, comparação de opções e monitorização. Tem risco maior e deve passar por validação clínica, testes de cenários, avaliação regulatória e implantação controlada.

O Reference pode sustentar comercialmente a construção gradual do Flow.

## Limite regulatório e de dados

O enquadramento depende da finalidade pretendida e das alegações comerciais do produto. Uma biblioteca de referência não é automaticamente equivalente a um sistema que sugere diagnóstico, tratamento ou conduta individualizada. A Anvisa informa que softwares de auxílio, sugestão ou realização de diagnóstico ou tratamento podem ser passíveis de regularização como Software as a Medical Device, sob a RDC 657/2022 e normas relacionadas. Essa classificação deve ser avaliada formalmente antes de liberar o DecisionMEd Flow.

Se forem armazenados casos identificáveis, o projeto também tratará dados pessoais sensíveis de saúde. Arquitetura, consentimento/base legal, minimização, controle de acesso, retenção, auditoria e resposta a incidentes precisam nascer na fundação — não ser adicionados depois.

## Viabilidade por dimensão

| Dimensão | Avaliação | Motivo |
| --- | --- | --- |
| Engenharia | Alta | o PsychRx já prova contratos, motores e fluxo progressivo |
| Reutilização do PsychRx | Alta após refatoração | domínio e segurança são reaproveitáveis; frontend monolítico não é |
| Conteúdo científico | Média/baixa no início | é o maior volume de trabalho e exige especialistas |
| Segurança clínica | Possível, mas exigente | requer bloqueios, validação e auditoria por pacote |
| Escala para todas as áreas | Possível por ondas | inviável tentar liberar todas simultaneamente |
| Cópia literal do WeMeds | Não recomendada | risco autoral, marcário, de banco de dados e de confiança |
| Produto próprio superior | Viável | fluxo por caso, longitudinalidade e explicação são diferenciais reais |

## Sequência recomendada

### Fase 0 — fundação DecisionMEd

1. Criar o contrato `SpecialtyPack`.
2. Separar plataforma e conhecimento.
3. Remover conhecimento hardcoded do frontend.
4. Criar registro de versões e compatibilidade de pacotes.
5. Criar suíte comum de segurança, auditoria e cenários.

### Fase 1 — transformar PsychRx no primeiro pacote

1. Migrar catálogo, eixos, doenças e regras para o pacote de psiquiatria.
2. Preservar o mesmo fluxo visual.
3. Validar os 51 tópicos já mapeados.
4. Liberar inicialmente apenas conteúdos com revisão científica concluída.

### Fase 2 — provar a arquitetura com uma segunda especialidade

Escolher Medicina de Família ou Cardiologia ambulatorial. A segunda especialidade é o verdadeiro teste: se exigir copiar código, o contrato ainda está errado.

### Fase 3 — ampliar por famílias clínicas

- clínica ambulatorial;
- pediatria;
- saúde da mulher;
- especialidades procedimentais;
- urgência e terapia intensiva por último.

## Critérios para dizer que uma especialidade está pronta

Um pacote só deve ser publicado quando tiver:

- escopo e exclusões explícitos;
- todas as red flags críticas testadas;
- fontes rastreáveis e vigentes;
- revisão por especialista;
- conflitos de diretrizes documentados;
- cálculos validados com casos-limite;
- testes de casos comuns, raros e perigosos;
- linguagem não prescritiva quando aplicável;
- data de revisão e expiração;
- processo de retirada ou atualização urgente;
- auditoria de todas as saídas apresentadas ao médico.

## Decisão recomendada

Prosseguir com o DecisionMEd como plataforma independente e usar o PsychRx como pacote fundador.

Não iniciar várias especialidades em paralelo antes de concluir a Fase 0 e provar uma segunda especialidade. O primeiro objetivo arquitetural deve ser conseguir instalar dois pacotes no mesmo núcleo sem duplicar motores, segurança, busca, interface ou infraestrutura editorial.

## Evidências locais examinadas

- `C:\Users\evcab\PsychRx\interfaces\web\static\index.html`
- `C:\Users\evcab\PsychRx\interfaces\web\static\app.js`
- `C:\Users\evcab\PsychRx\interfaces\web\server.py`
- `C:\Users\evcab\PsychRx\docs\029_CLINICAL_DECISION_ORCHESTRATOR.md`
- `C:\Users\evcab\PsychRx\docs\040_KNOWLEDGE_COMPUTING_ARCHITECTURE.md`
- `C:\Users\evcab\PsychRx\docs\045_DATA_FLOW_SPECIFICATION.md`
- `C:\Users\evcab\PsychRx\docs\050_ENGINEERING_BLUEPRINT.md`
- `C:\Users\evcab\PsychRx\governance\adr\docs_adr\0002_SEPARACAO_PLATFORM_KNOWLEDGE.md`
- `C:\Users\evcab\PsychRx\governance\adr\docs_adr\0012_PRESENTATION_CLINICAL_WIDGET_ARCHITECTURE.md`
- `C:\Users\evcab\PsychRx\knowledge_base\coverage\wemeds_psychiatry_coverage_matrix.csv`
- `C:\Users\evcab\PsychRx\governance\execution\PROJECT_STATUS.md`
