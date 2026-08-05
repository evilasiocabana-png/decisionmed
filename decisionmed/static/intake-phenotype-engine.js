(function exposeDecisionMedPhenotypeEngine(root, factory) {
  let ruleEngine = root.DecisionMedRuleEngine;
  if (typeof module === "object" && module.exports) {
    ruleEngine = require("./intake-rule-engine.js");
  }
  const api = factory(ruleEngine);
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.DecisionMedPhenotypeEngine = api;
})(
  typeof globalThis === "object" ? globalThis : this,
  function createPhenotypeEngine(ruleEngine) {
    "use strict";

    const VERSION = "1.0.0";
    const MAX_SYNDROME_CANDIDATES = 6;
    const MAX_DIFFERENTIAL_QUESTIONS = 6;
    const SYNDROMIC_ENTITY_TYPES = new Set([
      "initial_syndrome",
      "standardized_syndrome",
      "clinical_presentation",
      "manifestation",
    ]);
    const ENTITY_PRIORITY = Object.freeze({
      initial_syndrome: 4,
      clinical_presentation: 3,
      standardized_syndrome: 2,
      manifestation: 1,
    });
    const MODULE_SPECIALTIES = Object.freeze({
      cardiology: ["cardiology"],
      pulmonology: ["pulmonology"],
      neurologic: ["neurology"],
      neurology: ["neurology"],
      urinary: ["urology", "nephrology"],
      urology: ["urology", "nephrology"],
      abdominal: ["gastroenterology", "hepatology"],
      coloproctology: ["gastroenterology"],
      dermatology: ["dermatology"],
      visual: ["ophthalmology"],
      ophthalmology: ["ophthalmology"],
      musculoskeletal: ["orthopedics", "rheumatology"],
      orthopedics: ["orthopedics", "rheumatology"],
      gynecology: ["gynecology"],
      obstetric: ["obstetrics"],
      obstetrics: ["obstetrics"],
      metabolic: ["endocrinology"],
      endocrinology: ["endocrinology"],
      systemic: [
        "rheumatology",
        "infectious-diseases",
        "hematology",
        "internal-medicine",
      ],
      mentalhealth: ["psychiatry"],
      psychiatry: ["psychiatry"],
      generalmedicine: ["internal-medicine", "emergency"],
    });
    const UNKNOWN_VALUES = new Set([
      "nao sabe informar",
      "nao foi avaliado",
      "nao foi observada",
      "nao foi observado",
      "ainda nao foi avaliado",
      "prefere nao responder",
    ]);
    const ABSENT_VALUES = new Set([
      "nao",
      "nenhum",
      "nenhuma",
      "nunca",
      "nada percebido",
      "nao se aplica",
      "dentro do esperado",
      "sem tosse",
      "sem mudanca",
      "nao mudou",
      "nao houve",
      "nao esta presente",
      "urina normalmente",
    ]);
    const AXIS_LABELS = Object.freeze({
      manifestation: "Manifestação principal",
      temporal: "Tempo e início",
      trigger: "Desencadeantes",
      location: "Localização",
      quality: "Qualidade",
      intensity: "Intensidade",
      course: "Padrão e evolução",
      modifier: "Modificadores",
      associated: "Achados associados",
      context: "Contexto e antecedentes",
      safety: "Segurança",
      directed: "Investigação dirigida",
    });

    let MODULES = [];
    let CONTENT_BY_MODULE = new Map();
    let MODULE_BY_RUNTIME_KEY = new Map();
    let COMPILED_RULES = [];

    function normalize(value) {
      return String(value || "")
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLocaleLowerCase("pt-BR")
        .replace(/[^a-z0-9]+/g, " ")
        .trim();
    }

    function unique(values) {
      return [...new Set(values.filter(Boolean))];
    }

    function runtimeKey(module) {
      if (module.runtime_key) return module.runtime_key;
      if (module.key) return module.key;
      const legacy = module.legacy_keys || module.legacyKeys || [];
      return legacy[0] || module.module_id || module.moduleId;
    }

    function moduleId(module) {
      return module.module_id || module.moduleId || null;
    }

    function moduleName(module) {
      return module.display_name || module.name || module.official_name || runtimeKey(module);
    }

    function moduleEntityType(module) {
      return module.entity_type || module.entityType || "clinical_presentation";
    }

    function moduleSpecialty(module) {
      return module.primary_specialty || module.primarySpecialty || null;
    }

    function configureCatalog(modules = [], contents = []) {
      if (!Array.isArray(modules) || !Array.isArray(contents)) {
        throw new TypeError("phenotype catalog and content must be arrays");
      }
      MODULES = modules
        .filter((item) => item && moduleId(item) && runtimeKey(item))
        .map((item) => Object.freeze({ ...item }));
      CONTENT_BY_MODULE = new Map();
      for (const item of contents) {
        if (!item || typeof item !== "object") continue;
        const id = item.module_id || item.moduleId;
        const legacyKey = item.legacy_key || item.legacyKey;
        if (id) CONTENT_BY_MODULE.set(id, Object.freeze({ ...item }));
        if (legacyKey) CONTENT_BY_MODULE.set(`legacy:${legacyKey}`, Object.freeze({ ...item }));
      }
      MODULE_BY_RUNTIME_KEY = new Map(MODULES.map((item) => [runtimeKey(item), item]));
      return Object.freeze({
        moduleCount: MODULES.length,
        contentCount: CONTENT_BY_MODULE.size,
        syndromicCount: MODULES.filter((item) =>
          SYNDROMIC_ENTITY_TYPES.has(moduleEntityType(item)),
        ).length,
      });
    }

    function configureRules(items = []) {
      if (!Array.isArray(items)) throw new TypeError("phenotype rules must be an array");
      if (!ruleEngine) {
        COMPILED_RULES = [];
        return Object.freeze({ count: 0 });
      }
      const rules = items
        .filter((item) => item && ["support", "oppose", "alarm"].includes(item.effect))
        .map((item) => ({
          ruleId: item.rule_id || item.ruleId,
          moduleId: item.module_id || item.moduleId || null,
          version: item.version || "unknown",
          status: item.status || "unknown",
          effect: item.effect,
          strength: item.strength || "moderate",
          target: item.output_value || item.outputValue || item.output_key || item.outputKey,
          priority: item.priority === true,
          rationale: item.rationale || "Regra clínica declarativa.",
          sourceIds: item.source_ids || item.sourceIds || [],
          when: item.when,
        }));
      COMPILED_RULES = ruleEngine.compileRules(rules);
      return Object.freeze({ count: COMPILED_RULES.length });
    }

    function contentFor(module) {
      return (
        CONTENT_BY_MODULE.get(moduleId(module)) ||
        CONTENT_BY_MODULE.get(`legacy:${runtimeKey(module)}`) ||
        {}
      );
    }

    function valuesFor(content, snakeName, camelName) {
      const values = content[snakeName] || content[camelName] || [];
      return Array.isArray(values) ? values : [];
    }

    function polarity(value) {
      const normalized = normalize(value);
      if (!normalized || UNKNOWN_VALUES.has(normalized)) return "unknown";
      if (ABSENT_VALUES.has(normalized) || normalized === "0") return "absent";
      return "present";
    }

    function axisFor(answerId, section) {
      const id = String(answerId || "");
      if (section === "safety" || id.startsWith("safety.")) return "safety";
      if (id === "symptom.started" || id === "symptom.onset") return "temporal";
      if (id === "symptom.trigger") return "trigger";
      if (/location|\.eye$|\.side$/.test(id)) return "location";
      if (/quality|type/.test(id)) return "quality";
      if (/intensity/.test(id)) return "intensity";
      if (/pattern|trend|course|persistence|duration/.test(id)) return "course";
      if (/modifier|position|reproducible|pleuritic/.test(id)) return "modifier";
      if (/associated|systems|general/.test(id)) return "associated";
      if (section === "history") return "context";
      if (section === "symptom") return "manifestation";
      return "directed";
    }

    function buildPhenotype(input = {}) {
      const answers = Array.isArray(input.answers) ? input.answers : [];
      const features = [];
      if (String(input.complaint || "").trim()) {
        features.push(
          Object.freeze({
            id: "complaint",
            axis: "manifestation",
            axisLabel: AXIS_LABELS.manifestation,
            label: String(input.complaint).trim(),
            normalized: normalize(input.complaint),
            polarity: "present",
            question: "Queixa principal",
            order: 0,
          }),
        );
      }
      answers.forEach((answer, answerIndex) => {
        (answer.values || []).forEach((value, valueIndex) => {
          const axis = axisFor(answer.id, answer.section);
          features.push(
            Object.freeze({
              id: `${answer.id || "answer"}:${valueIndex}`,
              answerId: answer.id || null,
              axis,
              axisLabel: AXIS_LABELS[axis] || AXIS_LABELS.directed,
              label: String(value),
              normalized: normalize(value),
              polarity: polarity(value),
              question: answer.question || null,
              order: answerIndex + 1,
            }),
          );
        });
      });
      return Object.freeze({
        features: Object.freeze(features),
        present: Object.freeze(features.filter((item) => item.polarity === "present")),
        absent: Object.freeze(features.filter((item) => item.polarity === "absent")),
        unknown: Object.freeze(features.filter((item) => item.polarity === "unknown")),
        axisCount: new Set(features.filter((item) => item.polarity === "present").map((item) => item.axis)).size,
      });
    }

    function specialtiesFor(selectedModules = []) {
      return new Set(
        selectedModules.flatMap((key) => MODULE_SPECIALTIES[key] || [key]),
      );
    }

    function anchorMatchesFeature(anchor, feature) {
      const left = normalize(anchor);
      const right = feature.normalized;
      if (!left || !right) return false;
      if (left === right) return true;
      if (Math.min(left.length, right.length) < 4) return false;
      return left.includes(right) || right.includes(left);
    }

    function candidateDetails(module, phenotype, specialties, note) {
      const content = contentFor(module);
      const anchors = valuesFor(content, "anchor_values", "anchorValues");
      const matchedFeatures = phenotype.present.filter((feature) =>
        anchors.some((anchor) => anchorMatchesFeature(anchor, feature)),
      );
      const normalizedNote = normalize(note);
      const noteAnchors = normalizedNote
        ? anchors.filter((anchor) => {
            const value = normalize(anchor);
            return value.length >= 4 && normalizedNote.includes(value);
          })
        : [];
      const specialtyMatch = specialties.has(moduleSpecialty(module));
      const searchableName = normalize([
        moduleName(module),
        ...(module.synonyms || []),
        ...(module.abbreviations || []),
      ].join(" "));
      const nameMatches = phenotype.present.filter(
        (feature) =>
          feature.normalized.length >= 4 && searchableName.includes(feature.normalized),
      );
      const entityType = moduleEntityType(module);
      const score =
        matchedFeatures.length * 6 +
        noteAnchors.length * 3 +
        nameMatches.length * 2 +
        (specialtyMatch ? 18 : 0) +
        (ENTITY_PRIORITY[entityType] || 0) +
        ((module.legacy_keys || module.legacyKeys || []).length ? 2 : 0);
      return {
        module,
        content,
        key: runtimeKey(module),
        moduleId: moduleId(module),
        name: moduleName(module),
        entityType,
        specialty: moduleSpecialty(module),
        score,
        specialtyMatch,
        matchedFeatures,
        matchedAnchors: unique([
          ...matchedFeatures.flatMap((feature) =>
            anchors.filter((anchor) => anchorMatchesFeature(anchor, feature)),
          ),
          ...noteAnchors,
        ]),
        reasons: unique([
          ...matchedFeatures.map((feature) => `${feature.axisLabel}: ${feature.label}`),
          ...(specialtyMatch ? [`Área relacionada: ${moduleSpecialty(module)}`] : []),
          ...(noteAnchors.length ? ["Há correspondência com a descrição opcional."] : []),
        ]),
      };
    }

    function rankSyndromes(input = {}) {
      const phenotype = buildPhenotype(input);
      const specialties = specialtiesFor(input.selectedModules || []);
      const candidates = MODULES
        .filter((module) => SYNDROMIC_ENTITY_TYPES.has(moduleEntityType(module)))
        .map((module) => candidateDetails(module, phenotype, specialties, input.note || ""))
        .filter(
          (item) =>
            item.matchedFeatures.length > 0 ||
            item.matchedAnchors.length > 0 ||
            item.specialtyMatch,
        );
      const trace = [];
      const specialtyCandidates = candidates.filter((candidate) => candidate.specialtyMatch);
      let pool = specialtyCandidates.length ? specialtyCandidates : candidates;
      if (specialtyCandidates.length && specialtyCandidates.length < candidates.length) {
        trace.push(
          Object.freeze({
            featureId: "confirmed-clinical-area",
            label: "Área clínica definida pelo roteamento",
            before: candidates.length,
            after: specialtyCandidates.length,
            applied: true,
          }),
        );
      }
      for (const feature of phenotype.present.filter((item) => item.id !== "complaint")) {
        const matching = pool.filter((candidate) =>
          candidate.matchedFeatures.some((item) => item.id === feature.id),
        );
        if (matching.length && matching.length < pool.length) {
          trace.push(
            Object.freeze({
              featureId: feature.id,
              label: feature.label,
              before: pool.length,
              after: matching.length,
              applied: true,
            }),
          );
          pool = matching;
        } else {
          trace.push(
            Object.freeze({
              featureId: feature.id,
              label: feature.label,
              before: pool.length,
              after: pool.length,
              applied: false,
            }),
          );
        }
      }
      const source = pool.length ? pool : candidates;
      const sorted = source.sort(
        (left, right) =>
          right.score - left.score ||
          right.matchedFeatures.length - left.matchedFeatures.length ||
          (ENTITY_PRIORITY[right.entityType] || 0) -
            (ENTITY_PRIORITY[left.entityType] || 0) ||
          left.name.localeCompare(right.name, "pt-BR"),
      );
      const limit = Math.min(
        MAX_SYNDROME_CANDIDATES,
        Math.max(1, Number(input.limit) || MAX_SYNDROME_CANDIDATES),
      );
      return Object.freeze({
        engine: "DecisionMedPhenotypeEngine",
        version: VERSION,
        phenotype,
        candidates: Object.freeze(
          sorted.slice(0, limit).map((item, index) =>
            Object.freeze({
              key: item.key,
              moduleId: item.moduleId,
              name: item.name,
              entityType: item.entityType,
              specialty: item.specialty,
              order: index + 1,
              compatibility:
                item.matchedFeatures.length >= 4
                  ? "maior"
                  : item.matchedFeatures.length >= 2
                    ? "intermediária"
                    : "inicial",
              matchCount: item.matchedFeatures.length,
              matchedAnchors: Object.freeze([...item.matchedAnchors]),
              reasons: Object.freeze([...item.reasons]),
              probabilityCalibrated: false,
            }),
          ),
        ),
        trace: Object.freeze(trace),
        deferredFeatures: Object.freeze(
          trace.filter((item) => !item.applied).map((item) => item.label),
        ),
        stopRule:
          "O filtro para quando restam até seis classificações sindrômicas; a escolha continua profissional.",
        probabilityCalibrated: false,
      });
    }

    function diagnosisModule(name) {
      const target = normalize(name);
      if (!target) return null;
      const exact = MODULES.find((module) => {
        if (moduleEntityType(module) !== "diagnosis") return false;
        return [moduleName(module), ...(module.synonyms || []), ...(module.abbreviations || [])]
          .map(normalize)
          .includes(target);
      });
      if (exact) return exact;
      return MODULES.find((module) => {
        if (moduleEntityType(module) !== "diagnosis") return false;
        const candidate = normalize(moduleName(module));
        return (
          Math.min(candidate.length, target.length) >= 8 &&
          (candidate.includes(target) || target.includes(candidate))
        );
      }) || null;
    }

    function differentialNamesForSyndromeKey(key) {
      const module = MODULE_BY_RUNTIME_KEY.get(key);
      if (!module) return [];
      const content = contentFor(module);
      return unique([
        ...valuesFor(content, "likely_hypotheses", "likely"),
        ...valuesFor(content, "cannot_miss_hypotheses", "cannotMiss"),
        ...valuesFor(content, "mimics", "mimics"),
      ]);
    }

    function planDifferentiation(input = {}) {
      const syndromeKeys = Array.isArray(input.syndromeKeys) ? input.syndromeKeys : [];
      const answered = new Set(input.answeredIds || []);
      const maxQuestions = Math.min(
        MAX_DIFFERENTIAL_QUESTIONS,
        Math.max(1, Number(input.maxQuestions) || MAX_DIFFERENTIAL_QUESTIONS),
      );
      const candidateNames = unique(syndromeKeys.flatMap(differentialNamesForSyndromeKey));
      const questions = [];
      const seen = new Set();
      for (const question of input.baseQuestions || []) {
        if (!question?.id || seen.has(question.id) || answered.has(question.id)) continue;
        seen.add(question.id);
        questions.push({
          ...question,
          phase: "differential",
          targetDiagnoses: Object.freeze([...candidateNames]),
          questionOrigin: "confirmed_syndrome",
        });
        if (questions.length >= maxQuestions) break;
      }
      if (questions.length < maxQuestions && candidateNames.length <= 4) {
        for (const candidateName of candidateNames) {
          const module = diagnosisModule(candidateName);
          if (!module) continue;
          const content = contentFor(module);
          const candidateQuestions = valuesFor(content, "discriminators", "discriminators");
          const selected = candidateQuestions.find((question) => {
            const id = question.question_id || question.id;
            return id && !seen.has(id) && !answered.has(id);
          });
          if (!selected) continue;
          const id = selected.question_id || selected.id;
          seen.add(id);
          questions.push({
            id,
            text: selected.text,
            options: [...(selected.options || [])],
            rationale: selected.rationale || null,
            detailOnPositive:
              selected.detail_on_positive === true || selected.detailOnPositive === true,
            detailRequired:
              selected.detail_required === true || selected.detailRequired === true,
            sourceIds: [...(selected.source_ids || selected.sourceIds || [])],
            module: syndromeKeys[0] || "differential",
            section: "discriminator",
            phase: "differential",
            targetDiagnosis: candidateName,
            targetDiagnoses: Object.freeze([candidateName]),
            questionOrigin: "diagnosis_profile",
          });
          if (questions.length >= maxQuestions) break;
        }
      }
      return Object.freeze({
        questions: Object.freeze(questions.map((item) => Object.freeze(item))),
        candidateCount: candidateNames.length,
        candidateNames: Object.freeze(candidateNames),
        budget: maxQuestions,
        stopRule:
          questions.length >= maxQuestions
            ? "Limite de perguntas atingido; continuar pela avaliação clínica, exame físico ou exames complementares."
            : "Não há outra pergunta estruturada que separe melhor as hipóteses; avançar para exame físico ou exames complementares.",
      });
    }

    function answerFactKey(answerId) {
      return String(answerId || "")
        .replace(/^discriminator\./, "")
        .replace(/[^a-zA-Z0-9]+/g, "_")
        .replace(/^_|_$/g, "");
    }

    function factsFor(answers) {
      const answerValues = {};
      const values = [];
      for (const answer of answers) {
        const key = answerFactKey(answer.id);
        if (key) answerValues[key] = [...(answer.values || [])];
        values.push(...(answer.values || []));
      }
      return {
        values: unique(values),
        answerValues,
        answer_values: answerValues,
      };
    }

    function targetMatches(left, right) {
      const first = normalize(left);
      const second = normalize(right);
      if (!first || !second) return false;
      return (
        first === second ||
        (Math.min(first.length, second.length) >= 10 &&
          (first.includes(second) || second.includes(first)))
      );
    }

    function directQuestionEffect(answer, candidateName) {
      if (!answer.targetDiagnosis || !targetMatches(answer.targetDiagnosis, candidateName)) {
        return null;
      }
      const values = answer.values || [];
      if (!values.length || values.every((value) => polarity(value) === "unknown")) return null;
      const text = normalize(answer.question);
      const hasYes = values.some((value) => normalize(value) === "sim");
      const hasNo = values.some((value) => normalize(value) === "nao");
      if (/contradiga|sustente melhor outra/.test(text)) {
        if (hasYes) return { effect: "oppose", reason: `${answer.question}: Sim.` };
        return null;
      }
      if (/sinal de alarme|piora rapida|repercussao importante/.test(text)) {
        if (hasYes) return { effect: "alarm", reason: `${answer.question}: Sim.` };
        return null;
      }
      if (hasYes) return { effect: "support", reason: `${answer.question}: Sim.` };
      if (hasNo) return { effect: "oppose", reason: `${answer.question}: Não.` };
      return null;
    }

    function analyzeDifferentials(input = {}) {
      const syndromes = Array.isArray(input.syndromes) ? input.syndromes : [];
      const answers = Array.isArray(input.answers) ? input.answers : [];
      const ruleMatches = ruleEngine && COMPILED_RULES.length
        ? ruleEngine.evaluateRules(COMPILED_RULES, factsFor(answers))
        : [];
      const groups = [
        ["likely", "more_likely", "Mais provável"],
        ["cannotMiss", "cannot_miss", "Grave que não pode ser perdida"],
        ["mimics", "mimic", "Alternativa que imita o quadro"],
      ];
      const profiles = new Map();
      for (const syndrome of syndromes) {
        for (const [field, group, groupLabel] of groups) {
          for (const name of syndrome.differential?.[field] || []) {
            const key = `${group}:${normalize(name)}`;
            if (!profiles.has(key)) {
              const module = diagnosisModule(name);
              const content = module ? contentFor(module) : {};
              profiles.set(key, {
                key,
                name,
                group,
                groupLabel,
                originatingSyndromes: [],
                sharedSyndromicEvidence: [],
                present: [],
                absentOrContrary: [],
                pending: valuesFor(content, "diagnostic_criteria", "diagnosticCriteria"),
                alarms: [],
                sourceIds: unique([
                  ...(syndrome.sourceIds || []),
                  ...(syndrome.contentSourceIds || []),
                  ...valuesFor(content, "source_ids", "sourceIds"),
                ]),
                diagnosisModuleId: module ? moduleId(module) : null,
              });
            }
            const profile = profiles.get(key);
            profile.originatingSyndromes.push(syndrome.name);
            profile.sharedSyndromicEvidence.push(...(syndrome.supports || []));
          }
        }
      }
      for (const profile of profiles.values()) {
        for (const match of ruleMatches.filter((item) => targetMatches(item.target, profile.name))) {
          const reason = `${match.rationale} [${match.ruleId}]`;
          if (match.effect === "support") profile.present.push(reason);
          else if (match.effect === "oppose") profile.absentOrContrary.push(reason);
          else if (match.effect === "alarm") profile.alarms.push(reason);
        }
        for (const answer of answers) {
          const effect = directQuestionEffect(answer, profile.name);
          if (!effect) continue;
          if (effect.effect === "support") profile.present.push(effect.reason);
          else if (effect.effect === "oppose") profile.absentOrContrary.push(effect.reason);
          else profile.alarms.push(effect.reason);
        }
        const targetedQuestions = answers.filter(
          (answer) => answer.targetDiagnosis && targetMatches(answer.targetDiagnosis, profile.name),
        );
        if (!profile.pending.length && !targetedQuestions.length) {
          profile.pending.push("Critérios individualizados ainda não vinculados para esta hipótese.");
        }
      }
      return Object.freeze({
        engine: "DecisionMedPhenotypeEngine",
        version: VERSION,
        profiles: Object.freeze(
          [...profiles.values()].map((profile) => {
            const cannotMiss = profile.group === "cannot_miss";
            const present = unique(profile.present);
            const absentOrContrary = unique(profile.absentOrContrary);
            const alarms = unique(profile.alarms);
            let assessmentStatus = "unresolved";
            if (alarms.length) assessmentStatus = "alarm";
            else if (present.length > absentOrContrary.length) assessmentStatus = "supported";
            else if (absentOrContrary.length && cannotMiss) {
              assessmentStatus = "cannot_miss_requires_exclusion";
            } else if (absentOrContrary.length) assessmentStatus = "less_compatible";
            return Object.freeze({
              ...profile,
              originatingSyndromes: Object.freeze(unique(profile.originatingSyndromes)),
              sharedSyndromicEvidence: Object.freeze(unique(profile.sharedSyndromicEvidence)),
              present: Object.freeze(present),
              absentOrContrary: Object.freeze(absentOrContrary),
              pending: Object.freeze(unique(profile.pending)),
              alarms: Object.freeze(alarms),
              sourceIds: Object.freeze(unique(profile.sourceIds)),
              assessmentStatus,
              cannotMissPreserved: cannotMiss,
              automaticallyConfirmed: false,
            });
          }),
        ),
        probabilityCalibrated: false,
        confirmedByEngine: false,
      });
    }

    return Object.freeze({
      version: VERSION,
      maxSyndromeCandidates: MAX_SYNDROME_CANDIDATES,
      maxDifferentialQuestions: MAX_DIFFERENTIAL_QUESTIONS,
      configureCatalog,
      configureRules,
      buildPhenotype,
      rankSyndromes,
      planDifferentiation,
      analyzeDifferentials,
    });
  },
);
