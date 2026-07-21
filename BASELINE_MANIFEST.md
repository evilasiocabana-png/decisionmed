# Baseline importado do PsychRx

## Origem

- Repositório: `C:\Users\evcab\PsychRx`
- Branch de origem: `codex/p0-p5-clinical-coverage`
- Commit de origem: `21493f921b04b386e68cef7942bdd9006ef3f620`
- Destino: `C:\Users\evcab\DecisionMEd\psychrx-baseline`
- Data da cópia: 2026-07-20

## Exclusões deliberadas

- `.git/`
- `__pycache__/`
- `.venv/` e `venv/`
- arquivos `*.pyc` e `*.pyo`
- dependências externas alcançadas por junction em `tmp/spreadsheets/node_modules`

## Validação

Comando executado na cópia:

```powershell
python -m unittest discover -s tests -t .
```

Resultado:

```text
Ran 249 tests in 12.710s
OK
```

O repositório de origem permaneceu sem alterações e apontando para o commit registrado acima.

## Regra de proteção

Toda evolução multiespecialidade deve ocorrer dentro de `C:\Users\evcab\DecisionMEd`. O diretório original `C:\Users\evcab\PsychRx` é somente fonte de referência e não faz parte do novo histórico.

