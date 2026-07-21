# ADR DM-001 — SpecialtyPack como fronteira de composição

## Status

Aceito em 2026-07-21.

## Contexto

O DecisionMEd precisa reutilizar a arquitetura segura do PsychRx e permitir a
entrada futura de outras especialidades sem duplicar o núcleo da plataforma.
O baseline do PsychRx permanece preservado em `psychrx-baseline/` e não deve
ser transformado diretamente na aplicação multiespecialidade.

A Constituição Clínica, os Princípios Arquiteturais e o Engineering Blueprint
exigem separação entre domínio, conhecimento, evidência, raciocínio, segurança,
aplicação, interface e auditoria. Também proíbem conhecimento científico
hardcoded e qualquer salto direto da interface para uma decisão clínica.

## Decisão

Criar `SpecialtyPack` como um manifesto imutável de composição da plataforma.
Ele pertence à fundação do DecisionMEd e referencia contratos independentes de:

- workflow;
- segurança;
- política de evidência;
- namespace de conhecimento;
- auditoria;
- capacidades obrigatórias.

`SpecialtyPack` não é uma nova camada clínica, não contém conhecimento médico e
não executa raciocínio. A implementação inicial fica em `decisionmed/`, fora do
baseline. Psiquiatria é registrada como primeiro pacote em estado
`reference_only`, apontando para contratos arquiteturais do PsychRx.

Um pacote só poderá mudar para `active` em missão futura que valide os contratos
referenciados, os gates de segurança, evidência, rastreabilidade e integração.

## Alternativas consideradas

### Copiar o fluxo e o conhecimento para cada especialidade

Rejeitada por duplicar lógica, enfraquecer versionamento e aumentar o risco de
divergência clínica.

### Criar uma nova camada clínica para especialidades

Rejeitada porque `SpecialtyPack` é composição, não raciocínio. As camadas
oficiais continuam responsáveis por seus próprios significados e decisões.

### Manifesto de composição referencial

Aceita porque permite registrar especialidades sem mover conhecimento para o
código e sem permitir que interface ou registro decidam conduta.

## Consequências

- novas especialidades passam a ter identidade e dependências explícitas;
- o núcleo pode validar contratos antes de ativar um pacote;
- conhecimento científico continua versionado fora do manifesto;
- o PsychRx original e o baseline copiado permanecem inalterados;
- ativação clínica continua bloqueada até validação específica;
- mudanças no formato do manifesto exigem revisão desta ADR.

## Riscos e mitigações

- **Manifesto virar depósito de regra clínica:** os campos aceitos são apenas
  identificadores estruturais e os testes verificam o contrato.
- **Ativação prematura:** Psiquiatria inicia como `reference_only`.
- **Registro duplicado:** o registry rejeita chaves repetidas.
- **Dependências implícitas:** segurança, evidência e auditoria são obrigatórias
  no manifesto inicial e documentadas no contrato.

## Rollback

Reverter os cinco arquivos da missão DM-001. Nenhum dado clínico, conteúdo
científico ou arquivo do baseline precisa ser migrado para desfazer a decisão.

## Critérios de revisão

Revisar esta ADR antes de:

- ativar o primeiro pacote em runtime;
- adicionar campos com significado clínico ao manifesto;
- permitir carregamento dinâmico externo;
- alterar as fronteiras entre composição, aplicação e camadas clínicas.
