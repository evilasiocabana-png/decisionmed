# MISSÃO FINAL — COMPLEMENTAR O MOTOR FARMACOLÓGICO SEM REESTRUTURAR O APP

## Objetivo

Complementar o PsychRx preservando integralmente a interface, o fluxo e a arquitetura atuais que já foram aprovados.

Esta missão não autoriza crescimento arquitetural amplo, criação de novos núcleos, reescrita do motor, refatoração geral ou inclusão de funcionalidades além das descritas neste documento.

O objetivo é apenas acrescentar ao aplicativo atual:

1. medicação em uso;
2. dose, tempo, adesão, resposta e tolerabilidade;
3. perguntas de risco;
4. comparação da dose atual com o alvo terapêutico;
5. explicação do resultado usando os dados já existentes nas oito abas;
6. rastreabilidade por fontes oficiais já armazenadas no projeto.

---

## 1. Preservar o que já existe

Manter sem reestruturação:

- as oito abas atuais como base de conhecimento farmacológico curada;
- a Aba 9 como perfil farmacológico desejado;
- a Aba 10 como motor atual de ranking e resposta;
- a interface atual do aplicativo;
- o fluxo atual de uso;
- os componentes e contratos já funcionais;
- o comportamento já aprovado pelo usuário.

Não substituir nem duplicar as Abas 9 e 10.

Não criar novo motor paralelo.

Não transformar esta missão em uma nova arquitetura clínica completa.

---

## 2. Medicação atual

Adicionar ao fluxo atual a possibilidade de informar uma ou mais medicações em uso.

Campos mínimos por medicação:

```text
medicamento
indicação atual
formulação
via
frequência
horário
dose prescrita
dose realmente utilizada
unidade
data de início
data da última alteração de dose
tempo total de uso
tempo na dose atual
adesão
benefício percebido
resposta clínica
efeitos adversos
tolerabilidade
motivo do uso
```

Quando algum campo importante não estiver disponível, registrar explicitamente:

```text
INFORMAÇÃO_INSUFICIENTE
```

A ausência de informação não deve ser preenchida por inferência silenciosa.

---

## 3. Avaliação simples do tratamento atual

Antes de apresentar o ranking, o sistema deve classificar o tratamento atual usando somente os dados disponíveis e as faixas terapêuticas cadastradas.

Saídas mínimas:

```text
DOSE_ABAIXO_DA_FAIXA_CADASTRADA
DOSE_DENTRO_DA_FAIXA_CADASTRADA
DOSE_ACIMA_DA_FAIXA_CADASTRADA
TEMPO_POSSIVELMENTE_INSUFICIENTE
RESPOSTA_PARCIAL
SEM_RESPOSTA
BOA_RESPOSTA
INTOLERANCIA
ADESAO_INSUFICIENTE
DADOS_INSUFICIENTES
```

Regras obrigatórias:

- não classificar falha terapêutica sem considerar dose, tempo e adesão;
- não afirmar adequação individual de dose como prescrição;
- apresentar a comparação como apoio à decisão médica;
- manter a decisão final com o profissional.

---

## 4. Perguntas de risco

Adicionar um bloco de perguntas de risco antes do resultado do motor.

Aproveitar o que já existe no aplicativo e nas oito abas, acrescentando apenas os campos ausentes necessários para segurança.

Domínios mínimos:

```text
alergias ou reação grave anterior
gestação ou lactação
história de mania ou hipomania
psicose ou agitação importante
risco de suicídio ou autoagressão
convulsão ou epilepsia
glaucoma
retenção urinária
doença renal
doença hepática
risco cardiovascular
arritmia ou QT prolongado
risco metabólico
uso de álcool ou outras substâncias
outros medicamentos
fitoterápicos e suplementos
interações relevantes
```

As perguntas devem ser condicionais quando possível, para não tornar a interface excessivamente longa.

Cada risco deve produzir uma das seguintes consequências:

```text
INFORMAR
CAUTELA
REDUZIR_COMPATIBILIDADE
EXIGIR_REVISÃO_MÉDICA
BLOQUEAR_OPÇÃO
AVALIAÇÃO_URGENTE
```

Riscos graves não podem ser tratados apenas como pequena redução de score.

---

## 5. Alvo terapêutico e faixa de dose no resultado

O resultado deve mostrar, quando os dados existirem:

```text
medicação atual
dose atual
unidade e frequência
indicação considerada
faixa terapêutica cadastrada para a indicação
posição da dose atual em relação à faixa
tempo de uso
tempo na dose atual
resposta
tolerabilidade
adesão
```

Separar explicitamente:

```text
alvo clínico
faixa de dose terapêutica cadastrada
alvo sérico, quando aplicável
```

Dose administrada e concentração sérica não podem ser exibidas como se fossem a mesma informação.

O sistema deve informar a fonte e o contexto da faixa cadastrada, sem transformar essa faixa em prescrição automática individual.

---

## 6. Aproveitamento das oito abas

A resposta da Aba 10 deve aproveitar os dados já existentes nas oito abas para explicar, de forma resumida:

- compatibilidade com o perfil farmacológico desejado;
- efeitos favoráveis;
- efeitos desfavoráveis;
- riscos relevantes;
- contraindicações ou cautelas;
- impacto esperado em sono, energia, ansiedade, peso, libido, dor, cognição e outros campos já modelados;
- alvo clínico;
- faixa terapêutica cadastrada;
- monitorização relevante já disponível na base.

Não copiar grandes blocos das oito abas para a tela.

Produzir uma síntese clara e auditável.

---

## 7. Formato do resultado

Preservar o ranking atual e apenas enriquecê-lo.

O resultado deve conter três blocos:

### 7.1 Tratamento atual

```text
medicação e dose atuais
adequação em relação à faixa cadastrada
tempo de exposição
adesão
resposta
tolerabilidade
riscos e interações identificados
dados ausentes
```

### 7.2 Perfil farmacológico desejado

Exibir os objetivos já selecionados na Aba 9.

### 7.3 Resultado do motor

Para cada opção apresentada:

```text
posição no ranking
compatibilidade
principais vantagens
principais limitações
riscos e alertas
relação com a medicação atual
alvo clínico
faixa terapêutica cadastrada
justificativa resumida
fontes utilizadas
```

O motor deve poder concluir também que o tratamento atual precisa ser reavaliado antes de sugerir troca, sem transformar isso em prescrição.

---

## 8. Fontes e rastreabilidade

Usar exclusivamente as fontes oficiais e científicas já armazenadas nas pastas do projeto.

É proibido usar Wikipedia ou fontes abertas não validadas como base clínica.

Cada dado clínico ativo relevante deve, quando disponível, possuir:

```text
source_id
documento
instituição ou sociedade
seção
página
ano
status de validação
observação
```

Quando uma informação não possuir fonte oficial validada:

```text
PENDENTE_DE_VALIDACAO
```

Ela não deve ser transformada silenciosamente em regra ativa de bloqueio, dose ou contraindicação.

Não é necessário criar uma nova tela complexa nesta missão. A rastreabilidade pode ser incorporada à estrutura já existente e apresentada de forma simples no resultado ou em detalhe expansível.

---

## 9. Limites de escopo

Não fazer nesta missão:

- nova arquitetura geral;
- novo Clinical Snapshot;
- novo núcleo clínico;
- novo motor paralelo;
- reescrita das oito abas;
- substituição das Abas 9 ou 10;
- criação de múltiplas novas abas sem necessidade técnica comprovada;
- prescrição automática;
- geração automática de dose individual;
- troca, associação ou retirada automática;
- expansão para fluxos clínicos não solicitados;
- funcionalidades futuras não descritas aqui.

Se uma mudança estrutural adicional parecer necessária, registrar como pendência e não implementá-la automaticamente.

---

## 10. Compatibilidade

A implementação deve:

- preservar pacientes, registros e dados existentes;
- aceitar casos antigos sem medicação atual preenchida;
- manter o resultado atual quando os novos campos estiverem vazios;
- não quebrar o ranking existente;
- não alterar os scores já validados sem justificativa e testes;
- usar campos opcionais e defaults seguros;
- manter informação insuficiente como estado válido.

---

## 11. Testes mínimos

Adicionar testes cobrindo:

- caso sem medicação atual;
- uma medicação atual com dose abaixo da faixa cadastrada;
- dose dentro da faixa;
- dose acima da faixa;
- tempo insuficiente;
- adesão insuficiente;
- resposta parcial;
- intolerância;
- risco que apenas informa;
- risco que exige cautela;
- risco que bloqueia opção;
- interação com medicação atual;
- múltiplas medicações em uso;
- ausência de fonte validada;
- apresentação da faixa terapêutica no resultado;
- preservação do ranking atual;
- compatibilidade com dados antigos;
- ausência de prescrição automática.

Executar a suíte existente do projeto e registrar os resultados.

---

## 12. Entregável

Implementar somente este complemento e criar ao final:

```text
codex/inbox/results/FINAL_COMPLEMENTO_MOTOR_FARMACOLOGICO_REPORT.md
```

O relatório deve informar:

1. arquivos criados e modificados;
2. onde os novos campos foram integrados;
3. como a medicação atual é avaliada;
4. como funcionam as perguntas de risco;
5. como o alvo terapêutico aparece no resultado;
6. como as oito abas são aproveitadas;
7. como as fontes oficiais são rastreadas;
8. testes executados e resultados;
9. limitações e dados pendentes de validação;
10. confirmação de que a arquitetura e o fluxo aprovados foram preservados.

---

## Critério final de conclusão

A missão estará concluída quando o aplicativo atual continuar com a mesma estrutura e experiência aprovadas, porém passar a incluir:

```text
medicação em uso
+
dose, tempo, adesão, resposta e tolerabilidade
+
perguntas de risco
+
alvo terapêutico no resultado
+
explicação baseada nas oito abas
+
rastreabilidade por fontes oficiais
```

Sem expansão adicional de escopo.