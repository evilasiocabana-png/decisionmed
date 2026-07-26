# DecisionMEd

Plataforma clínica multiespecialidade derivada de uma cópia independente do PsychRx.

## Estado inicial

- `psychrx-baseline/`: cópia limpa e verificável do PsychRx, sem histórico Git, ambientes virtuais ou caches.
- `ANALISE_VIABILIDADE_DECISIONMED.md`: análise da arquitetura multiespecialidade proposta.
- `BASELINE_MANIFEST.md`: origem, integridade e validação da cópia.

O PsychRx original em `C:\Users\evcab\PsychRx` não deve ser alterado pelo desenvolvimento do DecisionMEd.

## Executar o MVP local

```powershell
python -m decisionmed.web
```

Se as portas estiverem ocupadas: `python -m decisionmed.web --port 8775 --psychiatry-port 8776`.

- Hub DecisionMEd: `http://127.0.0.1:8765/`
- Pacote de Psiquiatria: `http://127.0.0.1:8766/`

O hub está em modo `read-only`. Psiquiatria reutiliza o app local do baseline sem alterar o PsychRx original.

## Portas de entrada do formulário

- **Assistido:** conduz da queixa ao reconhecimento sindrômico e à diferenciação.
- **Direto:** começa pela síndrome clínica ou apresentação escolhida e confirma seus critérios.
- **Investigação:** compara de duas a três hipóteses por achados, perguntas e exames discriminadores.

As três portas usam o mesmo motor local e mantêm triagem de segurança, auditoria
e validação profissional. A expansão do catálogo para 50, 150 e 300 módulos está
definida em [DM-081](docs/DM-081_CLINICAL_REASONING_MODULE_ONTOLOGY.md).

O resumo também executa uma orquestração complementar e preserva o raciocínio
legado: Motor Sindrômico → Motor Diagnóstico → Motor Terapêutico → Gate de
Confiança. A rota sem LLM exige score calibrado e governança completa; como o
catálogo real continua em `draft`, a rota atual é “Caso complexo — LLM em
standby”. Nenhuma LLM é chamada e nenhum token é consumido. O contrato completo
está em [DM-309](docs/DM-309_CLINICAL_MOTOR_ORCHESTRATION.md).

## Catálogo científico separado

O conhecimento científico é versionado no repositório privado
[`decisionmed-knowledge`](https://github.com/evilasiocabana-png/decisionmed-knowledge),
conforme a separação exigida pela ADR-0002 do PsychRx.

A plataforma carrega e valida releases externas protegidas por manifesto e
hashes SHA-256. O catálogo atual possui sete campos cardiológicos e um registro
mestre com 300 módulos candidatos em status `draft`, exibidos apenas como
estrutura, 50 regras declarativas (30 de rota, oito de suporte diferencial e
12 de segurança) e 300 contratos estruturais de conteúdo em `partial`, todos
em `draft`; nenhum conteúdo está liberado para
execução clínica. Os 14 conteúdos anteriores foram preservados na migração. O
pacote inclui ainda 4.500 casos sintéticos determinísticos, 15 por módulo, para
cobertura técnica e auditoria. Quando o
repositório `DecisionMEd-Knowledge` está ao lado da plataforma, o comando padrão
o descobre automaticamente.

O primeiro lote de 50 módulos também possui uma fonte oficial candidata ligada
a cada pergunta e exame; isso é uma trilha de curadoria, não validação clínica.
O gate e suas limitações estão em [DM-307](docs/DM-307_ESSENTIAL_50_CURATION_GATE.md).
