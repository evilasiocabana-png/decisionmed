# MOTOR_FARMACOLOGICO_EVOLUTION_PHASE2

## Missao

Executar a Phase 2 da evolucao do Motor Farmacologico do PsychRx.

Esta missao deve partir da auditoria:

```text
docs/MOTOR_FARMACOLOGICO_EVOLUTION_AUDIT.md
```

## Objetivo

Implementar a camada de avaliacao da medicacao atual, preservando a arquitetura ja existente do Motor Farmacologico.

O motor deve passar a considerar:

- medicamento atual;
- dose atual;
- unidade;
- frequencia;
- tempo de uso;
- adesao;
- resposta percebida;
- tolerabilidade;
- efeitos adversos;
- possibilidade de otimizacao antes de troca;
- adequacao da dose em relacao a faixa cadastrada.

## Escopo permitido

Pode alterar ou criar arquivos em:

```text
application/
interfaces/web/static/
knowledge_base/decision_support_engine/tables/
tests/
docs/
```

## Escopo esperado

1. Ler a arquitetura atual:

```text
application/clinical_decision_support_contract.py
application/clinical_decision_support_service.py
application/decision_support_rule_table.py
application/pharmacological_decision_matrix.py
application/medication_strategy_table.py
interfaces/web/static/app.js
interfaces/web/static/index.html
```

2. Reutilizar `CurrentMedicationPayload`.

3. Criar uma avaliacao estruturada da medicacao atual, preferencialmente na application layer.

4. Produzir campos calculados como:

```text
current_dose_status
duration_status
response_status
tolerability_status
optimization_possible
```

5. Fazer o app enviar a receita atual real ao endpoint `/api/decision-support`.

6. Fazer a resposta do motor explicar:

- dose atual informada;
- faixa cadastrada;
- se a dose parece abaixo/dentro/acima/indeterminada;
- se tempo de uso parece suficiente/insuficiente/indeterminado;
- se a resposta favorece manter, otimizar, substituir, associar ou investigar;
- quando a informacao for insuficiente, perguntar o que falta.

## Regras obrigatorias

Nao apagar as oito tabelas originais.

Nao alterar o conteudo cientifico original das tabelas 1-8.

Nao criar prescricao autonoma.

Nao escolher medicamento como decisao final.

Nao sugerir dose como prescricao.

Nao ativar runtime clinico decisorio.

Nao remover o limite de que a decisao final e do medico.

Nao depender de GPT externo.

Nao criar nova arquitetura paralela.

## Comportamento esperado

O motor deve continuar funcionando como apoio a decisao medica.

Ele pode dizer, por exemplo:

```text
Receita atual: Sertralina 50 mg 1x/dia.
Faixa cadastrada: 50-200 mg/dia.
Dose atual: dentro da faixa inicial.
Tempo de uso: insuficiente para concluir falha, se menor que periodo minimo informado.
Resposta: parcial.
Tolerabilidade: boa.
Direcao estrutural: considerar otimizacao antes de substituicao, com revisao medica.
```

Isso nao deve aparecer como prescricao.

Deve aparecer como raciocinio estruturado para revisao do medico.

## Criterios de aceite

- O app permite informar receita atual de modo estruturado.
- A receita atual e enviada ao endpoint `/api/decision-support`.
- O backend avalia dose, tempo, resposta e tolerabilidade.
- A resposta do motor mostra adequacao da medicacao atual.
- O ranking farmacologico continua funcionando.
- O motor nao prescreve.
- O motor nao remove a decisao final do medico.
- Testes unitarios cobrem a avaliacao da medicacao atual.
- Testes de interface cobrem os novos campos essenciais.
- Todos os testes passam.

## Validacao obrigatoria

Executar:

```bash
python -m unittest discover -s tests -t .
```

## Saida esperada

Ao final, informar:

1. arquivos criados;
2. arquivos alterados;
3. como a medicacao atual entrou no motor;
4. quais campos sao calculados;
5. como o app exibe a adequacao da dose atual;
6. resultado dos testes;
7. confirmacao de que nao houve prescricao autonoma.

