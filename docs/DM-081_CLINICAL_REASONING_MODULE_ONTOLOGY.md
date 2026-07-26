# DM-081 — Ontologia de módulos de raciocínio clínico

## Objetivo

Permitir que o DecisionMEd cresça de um catálogo inicial para 50, 150 e 300
módulos clínicos sem duplicar os motores de entrevista, comparação, auditoria
ou conduta.

## Portas de entrada

- **Assistido:** manifestação → fenótipo → reconhecimento sindrômico →
  diferenciação → impressão profissional → gate de conduta.
- **Direto:** síndrome clínica ou apresentação escolhida → triagem → confirmação de critérios →
  impressão profissional → gate de conduta.
- **Investigação:** duas ou três hipóteses → triagem → critérios compartilhados
  → perguntas discriminadoras → comparação qualitativa → gate de conduta.

As três portas usam o mesmo catálogo e o mesmo motor. A porta define apenas o
ponto de entrada e a apresentação.

## Separação entre motor e conteúdo

O motor é responsável por sequência, seleção, comparação, rastreabilidade,
reavaliação e gates. Cada módulo clínico é conteúdo governado e segue
`docs/schemas/clinical-reasoning-module.schema.json`.

O objeto clínico mantém as camadas:

`manifestação → fenótipo → síndrome inicial ou apresentação clínica →
diagnósticos possíveis → critérios →
exames → tratamento → acompanhamento`.

## Terminologia clínica

O nome exibido deve corresponder ao tipo ontológico real. Uma apresentação
ampla não pode receber artificialmente o rótulo de síndrome. O identificador
interno permanece estável para preservar auditoria, enquanto `entity_type` e o
nome clínico podem evoluir por versão.

No primeiro módulo torácico:

`Síndrome torácica aguda → hipóteses principais → confirmação diagnóstica`.

As hipóteses iniciais catalogadas são síndrome coronariana aguda (SCA),
isquemia miocárdica sem infarto (angina; ANOCA/INOCA conforme investigação),
dissecção aguda de aorta, embolia pulmonar, pericardite aguda, tamponamento
cardíaco, pneumotórax hipertensivo, dor musculoesquelética da parede torácica,
doença esofágica e ansiedade ou síndrome de hiperventilação.

Referências terminológicas oficiais usadas nesta versão:

- Diretriz Brasileira de Atendimento à Dor Torácica na Unidade de Emergência
  – 2025 (SBC/Arquivos Brasileiros de Cardiologia):
  <https://abccardiol.org/article/diretriz-brasileira-de-atendimento-a-dor-toracica-na-unidade-de-emergencia-2025/>
- 2025 Guideline for the Management of Patients With Acute Coronary Syndromes
  (ACC/AHA):
  <https://professional.heart.org/en/science-news/2025-guideline-for-the-management-of-patients-with-acute-coronary-syndromes>
- 2024 Guidelines for the Management of Chronic Coronary Syndromes
  (ESC; terminologia ANOCA/INOCA):
  <https://www.escardio.org/guidelines/clinical-practice-guidelines/all-esc-practice-guidelines/chronic-coronary-syndromes/>

## Expansão

1. **Fase 1:** até 50 módulos essenciais, após curadoria e validação.
2. **Fase 2:** até 150 módulos, ampliando especialidades.
3. **Fase 3:** até 300 módulos, sem alterar o contrato do motor.

Quantidade não libera execução clínica. Cada módulo precisa de referências,
revisão, versão, estado de curadoria e gates de segurança antes de sair de
`draft`.

## Limites atuais

O formulário local contém famílias sindrômicas de protótipo para validar
interação e arquitetura. Compatibilidade é uma classificação qualitativa, não
uma probabilidade calibrada. O sistema não confirma diagnóstico, não interpreta
arquivos e não libera conduta sem validação profissional e readiness técnico.
