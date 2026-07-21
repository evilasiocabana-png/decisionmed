# 019 - Clinical Navigation Engine

## 1. Definicao

O Clinical Navigation Engine e o motor conceitual responsavel por orientar como o PsychRx acompanha a evolucao do paciente ao longo do tempo.

Ele organiza mudancas no estado clinico, revisoes de hipoteses, ajustes de objetivos e continuidade do cuidado sem transformar o sistema em prescritor automatico.

## 2. Missao

A missao do Clinical Navigation Engine e manter coerencia longitudinal entre o estado atual do paciente, sua trajetoria, os objetivos terapeuticos, as restricoes, a resposta clinica e a monitorizacao.

Ele responde a pergunta:

```text
Como o raciocinio clinico deve se orientar diante da evolucao deste paciente ao longo do tempo?
```

## 3. Responsabilidades

O motor deve:

- comparar estados clinicos sucessivos;
- identificar mudancas relevantes;
- apoiar revisao de hipoteses;
- apoiar revisao de objetivos;
- organizar continuidade do cuidado;
- reconhecer estados clinicos;
- relacionar resposta, tolerabilidade e funcionalidade;
- indicar quando uma estrategia precisa ser reavaliada;
- manter rastreabilidade longitudinal.

## 4. Entradas Conceituais

As entradas conceituais incluem:

- Clinical Snapshots sucessivos;
- hipoteses diagnosticas anteriores e atuais;
- objetivos terapeuticos ativos;
- estrategias previamente consideradas ou selecionadas pelo medico;
- resposta clinica;
- eventos adversos;
- adesao;
- dados de monitorizacao;
- restricoes novas ou modificadas;
- sinais de recaida, recorrencia, remissao ou estabilidade.

## 5. Saidas Conceituais

As saidas conceituais incluem:

- leitura da evolucao clinica;
- mudancas relevantes desde o Snapshot anterior;
- necessidade de revisar hipoteses;
- necessidade de revisar objetivos;
- necessidade de reavaliar estrategia;
- indicacao de continuidade, cautela ou alerta;
- pontos que exigem monitorizacao;
- explicacao longitudinal.

## 6. Navegacao Longitudinal

A navegacao longitudinal deve considerar que o paciente muda ao longo do tempo.

O motor deve acompanhar:

- melhora;
- piora;
- resposta parcial;
- ausencia de resposta;
- instabilidade;
- remissao;
- recaida;
- recorrencia;
- estabilizacao parcial;
- estabilizacao sustentada.

Cada estado deve ser interpretado no contexto da trajetoria, nao como evento isolado.

## 7. Mudancas Terapeuticas

Mudancas terapeuticas devem ser compreendidas como eventos que exigem nova avaliacao clinica.

O motor deve registrar conceitualmente:

- motivo da mudanca;
- objetivo que motivou a mudanca;
- risco identificado;
- evidencia ou justificativa associada;
- impacto esperado;
- necessidade de monitorizacao;
- efeito sobre o plano longitudinal.

Ele nao decide a mudanca. Ele organiza o raciocinio sobre ela.

## 8. Revisao de Hipoteses

Hipoteses diagnosticas devem poder mudar quando novos dados surgem.

O Clinical Navigation Engine deve apoiar revisao quando houver:

- curso inesperado;
- resposta incompatível com hipotese inicial;
- novos sintomas;
- nova sindrome;
- deterioracao;
- efeitos adversos que confundem o quadro;
- informacao longitudinal relevante.

## 9. Adaptacao do Plano

O plano clinico deve ser adaptavel, mas nao improvisado.

A adaptacao deve respeitar:

- Snapshot atualizado;
- objetivos terapeuticos;
- restricoes;
- seguranca;
- evidencias;
- preferencias do paciente;
- monitorizacao;
- decisao medica.

## 10. Estados Clinicos

O motor deve organizar estados clinicos como categorias conceituais de acompanhamento.

Estados relevantes incluem:

- instabilidade aguda;
- risco aumentado;
- resposta inicial;
- resposta parcial;
- remissao;
- estabilidade parcial;
- estabilidade sustentada;
- recaida;
- recorrencia;
- deterioracao clinica.

Estados clinicos devem orientar raciocinio, nao substituir julgamento.

## 11. Continuidade do Cuidado

Continuidade significa que cada nova leitura clinica deve dialogar com leituras anteriores.

O motor deve evitar:

- decisoes sem memoria clinica;
- perda de contexto;
- repeticao de estrategias ja malsucedidas sem justificativa;
- ignorar eventos adversos previos;
- tratar cada consulta como se fosse o primeiro contato.

## 12. Relacao com Clinical Snapshot

O Clinical Snapshot fornece o estado atual. O Clinical Navigation Engine compara esse estado com os anteriores.

Sem Snapshots sucessivos, a navegacao longitudinal perde sua base.

## 13. Relacao com Monitoring Engine

O Monitoring Engine fornece sinais de resposta, seguranca, adesao e eventos adversos.

O Clinical Navigation Engine interpreta esses sinais na trajetoria do paciente.

## 14. Relacao com Longitudinal Reasoning

Longitudinal Reasoning define o modelo de raciocinio temporal. O Clinical Navigation Engine aplica esse modelo para orientar o percurso clinico.

## 15. Limites

O Clinical Navigation Engine nao deve:

- prescrever mudancas;
- substituir seguimento medico;
- criar plano automatico;
- ignorar riscos agudos;
- operar sem Snapshot atualizado;
- tratar estabilidade como ausencia definitiva de risco;
- criar regras clinicas sem evidencia.

## 16. Declaracao Final

O Clinical Navigation Engine e o motor que preserva continuidade no raciocinio do PsychRx.

Ele impede que o sistema pense apenas em eventos isolados e organiza a evolucao do paciente como trajetoria.

No PsychRx, acompanhar e tao importante quanto avaliar.
