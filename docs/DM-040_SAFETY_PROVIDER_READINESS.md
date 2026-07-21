# DM-040 — Safety provider readiness

## Objective

Require technical provider coverage in addition to governed safety metadata so
that validated specifications alone cannot make the safety configuration appear
complete.

## Readiness contract

The safety gate now evaluates, in order:

1. non-empty specification registry;
2. validated and current specification lifecycle;
3. at least one provider binding;
4. absence of incompatible provider versions;
5. complete provider coverage for every specification.

Reasons distinguish `no_safety_providers`, incompatible versions, incomplete
coverage, and `safety_configuration_complete`. Counts expose provider bindings,
missing providers, and incompatible providers.

## Safety limits

Complete coverage is still only technical metadata. This mission does not call a
provider, accept patient data, generate a `SafetyFinding`, bind a specialty
runtime capability, or authorize clinical execution.

## Architecture

Application injects an optional provider registry into readiness. The default is
an empty registry derived from the loaded specifications, so absence always
fails closed. No Interface dependency or clinical rule is introduced.

## Rollback

Remove provider injection and restore the preceding specification-only readiness
condition. Catalog schema and data are unaffected.
