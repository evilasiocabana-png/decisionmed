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

## Catálogo científico separado

O conhecimento científico é versionado no repositório privado
[`decisionmed-knowledge`](https://github.com/evilasiocabana-png/decisionmed-knowledge),
conforme a separação exigida pela ADR-0002 do PsychRx.

A plataforma carrega e valida releases externas protegidas por manifesto e
hashes SHA-256. O catálogo atual possui o primeiro campo cardiológico em status
`draft`, exibido apenas como referência; nenhum conteúdo está liberado para
execução clínica. Quando o repositório `DecisionMEd-Knowledge` está ao lado da
plataforma, o comando padrão o descobre automaticamente.
