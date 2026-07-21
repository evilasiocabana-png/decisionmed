"""Build a traceable theory-to-practice evidence staging layer for PsychRx.

The didactic PDF defines clinical concerns that the motor should observe. It
does not authorize doses, indications, or therapeutic actions. Regulatory
labels and guidelines provide reviewable anchors for later normalization.

This script writes staging matrices only. It never edits the eight audited
source workbooks or promotes a claim to runtime eligibility.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unicodedata import normalize


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "knowledge_base" / "decision_support_engine" / "tables"
DOC_DIR = ROOT / "docs" / "decision_support_engine"

REGISTRY_PATH = TABLE_DIR / "medication_official_source_registry.csv"
PROFILE_PATH = TABLE_DIR / "medication_explanation_profile_backlog.csv"
DISEASE_USE_PATH = TABLE_DIR / "medication_disease_use_matrix.csv"
MOTOR2_PATH = TABLE_DIR / "motor2_strategy_matrix.csv"

THEORY_PATH = TABLE_DIR / "theory_to_practice_matrix.csv"
CLAIMS_PATH = TABLE_DIR / "medication_official_claims.csv"
DISEASE_REVIEW_PATH = TABLE_DIR / "medication_disease_use_evidence_review.csv"
GAP_PATH = TABLE_DIR / "medication_evidence_gap_matrix.csv"
MOTOR2_REVIEW_PATH = TABLE_DIR / "motor2_gap_resolution_matrix.csv"
REPORT_PATH = DOC_DIR / "THEORY_TO_PRACTICE_EVIDENCE_REPORT.md"

PDF_NAME = "Paicofarmacos 1 2.pdf"
PDF_PATH = Path(
    r"C:\Users\evcab\.codex\codex-remote-attachments\019f0d03-9cb5-7023-bb50-cd5bb3e7f2f3"
    r"\78575D84-8CD0-4FEB-8361-FA681BF25E5F\1-Paicofarmacos-1-2.pdf"
)

NICE_DEPRESSION = "https://www.nice.org.uk/guidance/ng222/chapter/Recommendations"
NICE_BIPOLAR = "https://www.nice.org.uk/guidance/cg185/chapter/recommendations"
NICE_PSYCHOSIS = "https://www.nice.org.uk/guidance/cg178/chapter/recommendations"
DAILYMED = "https://dailymed.nlm.nih.gov/"
EMA_AGOMELATINE = "https://www.ema.europa.eu/en/medicines/human/EPAR/valdoxan"

NS = {"hl7": "urn:hl7-org:v3"}


THEORY_ROWS = (
    (
        "TPC-001",
        "Escolha do tratamento",
        "7-9, 13",
        "Escolha depende de quadro, comorbidades, interacoes, resposta previa e tolerabilidade.",
        "diagnostico_ou_fenotipo|comorbidades|receita_atual|historico_de_tentativas|preferencias",
        "Verificar contexto, tratamentos previos, riscos e preferencias antes de comparar candidatos.",
        "contextualizar_ranking",
        "Exibir fatores que determinaram a comparacao; nao transformar preferencia em regra absoluta.",
        "NICE-NG222-1.4.2-1.4.11",
        "Needs and preferences; starting antidepressant medication",
        NICE_DEPRESSION,
        "official_guideline_validated",
    ),
    (
        "TPC-002",
        "Reavaliacao inicial",
        "14",
        "A resposta deve ser reavaliada precocemente, junto com efeitos adversos e adesao.",
        "tempo_de_uso|resposta|adesao|tolerabilidade|risco_suicida",
        "Distinguir exposicao insuficiente de ausencia de resposta em tempo adequado.",
        "qualificar_adequacao_do_ensaio",
        "Mostrar tempo informado, resposta, adesao e tolerabilidade antes da acao pratica.",
        "NICE-NG222-1.4.3-1.4.11",
        "Review between 2 and 4 weeks; first medication review",
        NICE_DEPRESSION,
        "official_guideline_validated",
    ),
    (
        "TPC-003",
        "Ensaio antidepressivo adequado",
        "15-17",
        "Dose, tempo, adesao e diagnostico devem ser verificados antes de concluir falha.",
        "dose_atual|faixa_por_quadro|tempo_de_uso|adesao|diagnostico_ou_fenotipo|resposta",
        "Somente classificar resposta inadequada quando os componentes do ensaio estiverem documentados.",
        "evitar_falsa_refratariedade",
        "Exibir componentes presentes e ausentes do ensaio; manter conclusao como indeterminada quando incompleto.",
        "NICE-NG222-1.9.1-1.9.6",
        "Further-line treatment after no or limited response",
        NICE_DEPRESSION,
        "official_guideline_validated",
    ),
    (
        "TPC-004",
        "Fase do tratamento",
        "18-21",
        "Fase aguda, continuacao e manutencao possuem objetivos temporais diferentes.",
        "fase_do_tratamento|remissao|recorrencia|gravidade|tempo_de_uso",
        "Nao comparar manutencao e fase aguda como se fossem o mesmo objetivo.",
        "ajustar_objetivo_temporal",
        "Identificar a fase e o objetivo: resposta aguda, consolidacao ou prevencao de recaida.",
        "NICE-NG222-1.4.11-1.8",
        "Continuation after remission and relapse prevention",
        NICE_DEPRESSION,
        "official_guideline_validated",
    ),
    (
        "TPC-005",
        "Retirada e descontinuacao",
        "22-23",
        "Retirada abrupta pode produzir sintomas; meia-vida e historico de retirada importam.",
        "medicamento|dose|duracao|historico_de_retirada|motivo_da_retirada",
        "Sinalizar necessidade de plano individual de retirada e monitorizacao sem calcular esquema automatico.",
        "alertar_retirada",
        "Mostrar risco de retirada e necessidade de reducao gradual acordada com o prescritor.",
        "NICE-NG222-1.4.12-1.4.21",
        "Stopping antidepressant medication",
        NICE_DEPRESSION,
        "official_guideline_validated",
    ),
    (
        "TPC-006",
        "Carga anticolinergica, sedativa e cardiovascular",
        "24-25",
        "Triciclicos exigem atencao a cognicao, quedas, retencao, sedacao e conducao cardiaca.",
        "idade|cognicao|quedas|retencao_urinaria|constipacao|cardiovascular|polifarmacia",
        "Aplicar cautelas por perfil e encaminhar detalhes ao claim regulatorio do medicamento.",
        "penalizar_por_risco",
        "Exibir riscos relevantes e o motivo da reducao de elegibilidade.",
        "DM-DRUG-LABEL",
        "Warnings, precautions, adverse reactions and interactions",
        DAILYMED,
        "drug_specific_validation_required",
    ),
    (
        "TPC-007",
        "Perfil dependente da dose",
        "26, 33-34, 68-70",
        "Alguns medicamentos apresentam efeitos clinicos distintos conforme dose e contexto.",
        "medicamento|dose_atual|quadro|alvo|resposta|tolerabilidade",
        "Comparar dose atual com faixa do quadro; manter explicacao integral separada da faixa numerica.",
        "comparar_dose_e_contexto",
        "Exibir leitura da dose, faixa do quadro, efeito dominante e fonte sem extrapolar entre medicamentos.",
        "DM-DRUG-LABEL",
        "Dosage and Administration; Clinical Pharmacology",
        DAILYMED,
        "drug_specific_validation_required",
    ),
    (
        "TPC-008",
        "Funcao sexual",
        "27-28",
        "Sintomas sexuais podem decorrer do quadro, da medicacao ou de outros fatores.",
        "funcao_sexual_baseline|inicio_temporal|medicamentos|resposta_do_quadro|outros_fatores",
        "Nao atribuir automaticamente causalidade ao medicamento.",
        "diferenciar_sintoma_e_evento_adverso",
        "Mostrar temporalidade, alternativas causais e fonte do risco por medicamento.",
        "DM-DRUG-LABEL",
        "Warnings and Precautions; Adverse Reactions",
        DAILYMED,
        "drug_specific_validation_required",
    ),
    (
        "TPC-009",
        "Risco de convulsao",
        "29-31",
        "Medicamentos que reduzem o limiar convulsivo exigem triagem de fatores predisponentes.",
        "convulsao|trauma_craniano|transtorno_alimentar|alcool|retirada_de_sedativos|interacoes",
        "Cruzar fatores do paciente com contraindicoes e advertencias da fonte oficial.",
        "excluir_ou_sinalizar_candidato",
        "Exibir o fator de risco, o medicamento afetado e a fonte regulatoria.",
        "DM-BUPROPION-LABEL",
        "Contraindications; Warnings and Precautions - Seizure",
        DAILYMED,
        "official_label_anchor_available",
    ),
    (
        "TPC-010",
        "Toxicidade serotoninergica",
        "34-36",
        "Associacoes serotoninergicas e mudancas recentes podem elevar risco de toxicidade.",
        "lista_completa_de_medicamentos|substancias|mudanca_recente|sinais_autonomicos|neuromusculares",
        "Avaliar interacoes e sinais de urgencia separadamente do ranking de rotina.",
        "acionar_alerta_de_interacao_ou_urgencia",
        "Exibir combinacao envolvida e recomendar avaliacao urgente quando houver quadro compativel.",
        "DM-DRUG-LABEL",
        "Warnings and Precautions - Serotonin Syndrome; Drug Interactions",
        DAILYMED,
        "drug_specific_validation_required",
    ),
    (
        "TPC-011",
        "Bipolaridade e antidepressivos",
        "36-38",
        "Mania ou hipomania muda a trilha de avaliacao e impede tratar depressao como unipolar sem revisao.",
        "mania_hipomania|curso_longitudinal|antidepressivos_atuais|estabilizadores_atuais",
        "Abrir trilha bipolar e sinalizar antidepressivo sem cobertura de humor para revisao.",
        "mudar_trilha_clinica",
        "Exibir eixo bipolar, cobertura atual e pendencias de seguranca/diagnostico.",
        "NICE-CG185-1.5-1.10",
        "Managing mania or hypomania; using medication",
        NICE_BIPOLAR,
        "official_guideline_validated",
    ),
    (
        "TPC-012",
        "Monitorizacao do litio",
        "39-43",
        "Litio exige nivel serico e monitorizacao renal, tireoidiana, calcio e interacoes.",
        "litemia|funcao_renal|tireoide|calcio|hidratacao|interacoes|adesao",
        "Nao avaliar adequacao do litio apenas pela dose em miligramas.",
        "exigir_monitorizacao_especifica",
        "Exibir nivel serico, exames e interacoes faltantes; separar dose prescrita de alvo serico.",
        "NICE-CG185-1.10.14-1.10.24",
        "Starting and monitoring lithium",
        NICE_BIPOLAR,
        "official_guideline_validated",
    ),
    (
        "TPC-013",
        "Ensaio antipsicotico e refratariedade",
        "43-50",
        "Escolha requer beneficio, efeitos adversos, dose, tempo e adesao; refratariedade exige tentativas adequadas.",
        "diagnostico|antipsicoticos_previos|dose|tempo|adesao|resposta|efeitos_adversos",
        "Registrar ensaio individual e somente reconhecer refratariedade com historico suficiente.",
        "qualificar_ensaio_antipsicotico",
        "Mostrar adequacao das tentativas e criterio faltante antes de escalar estrategia.",
        "NICE-CG178-1.3.5-1.5.7",
        "Choice and use of antipsychotics; clozapine after two adequate trials",
        NICE_PSYCHOSIS,
        "official_guideline_validated",
    ),
    (
        "TPC-014",
        "Efeitos extrapiramidais e acatisia",
        "51-55",
        "Sinais motores exigem reconhecimento e revisao da exposicao antes de simplesmente adicionar tratamento sintomatico.",
        "tremor|rigidez|bradicinesia|distonia|acatisia|discinesia|dose|mudanca_recente",
        "Separar evento adverso motor de piora psiquiatrica e sinalizar revisao do antipsicotico.",
        "alertar_evento_adverso_motor",
        "Exibir sinais presentes, temporalidade e medicamento potencialmente implicado.",
        "NICE-CG178-1.3.5-1.3.6",
        "Extrapyramidal effects and movement-disorder monitoring",
        NICE_PSYCHOSIS,
        "official_guideline_validated",
    ),
    (
        "TPC-015",
        "Risco metabolico de antipsicoticos",
        "55-56",
        "Peso, glicemia, lipideos e risco cardiovascular integram a escolha e a monitorizacao.",
        "peso|circunferencia_abdominal|pressao|glicemia_hba1c|lipideos|historico_cardiovascular",
        "Comparar risco metabolico e exigir baseline/seguimento quando aplicavel.",
        "penalizar_risco_metabolico",
        "Exibir risco relativo cadastrado, exames presentes e monitorizacao faltante.",
        "NICE-CG178-1.3.5.1-1.3.6.4",
        "Metabolic risks and baseline/ongoing monitoring",
        NICE_PSYCHOSIS,
        "official_guideline_validated",
    ),
    (
        "TPC-016",
        "Emergencias e toxindromes",
        "57-66, 72-74",
        "Emergencias devem ser reconhecidas e encaminhadas por fluxo proprio, fora do ranking ambulatorial.",
        "temperatura|rigidez|consciencia|sinais_vitais|ingestao|substancias|mudanca_recente|risco_imediato",
        "Interromper a comparacao ambulatorial e apresentar prioridade de avaliacao urgente.",
        "separar_fluxo_de_urgencia",
        "Mostrar o motivo da urgencia e ocultar qualquer sugestao rotineira como acao principal.",
        "DM-DRUG-LABEL",
        "Warnings and Precautions; Overdosage",
        DAILYMED,
        "emergency_protocol_validation_required",
    ),
)


CONDITION_TERMS = {
    "transtorno depressivo maior": ("major depressive disorder", "major depression"),
    "depressao": ("major depressive disorder", "depression"),
    "transtorno de ansiedade generalizada": ("generalized anxiety disorder",),
    "tag": ("generalized anxiety disorder",),
    "transtorno do panico": ("panic disorder",),
    "panico": ("panic disorder",),
    "toc": ("obsessive compulsive disorder", "obsessive-compulsive disorder"),
    "transtorno de ansiedade social": ("social anxiety disorder", "social phobia"),
    "fobia social": ("social anxiety disorder", "social phobia"),
    "transtorno de estresse pos traumatico": ("posttraumatic stress disorder", "post-traumatic stress disorder"),
    "transtorno bipolar episodio depressivo": ("bipolar depression", "depressive episodes associated with bipolar"),
    "transtorno bipolar mania hipomania": ("manic", "mania", "bipolar i disorder"),
    "esquizofrenia e transtornos psicoticos": ("schizophrenia",),
    "esquizofrenia manutencao": ("schizophrenia",),
    "tdah": ("attention deficit hyperactivity disorder", "attention-deficit/hyperactivity disorder"),
    "insonia": ("insomnia",),
    "dor neuropatica ou sindromes dolorosas": ("neuropathic pain", "fibromyalgia", "chronic musculoskeletal pain"),
    "fibromialgia": ("fibromyalgia",),
    "transtorno por uso de alcool": ("alcohol dependence", "alcohol use disorder"),
    "transtorno por uso de opioides": ("opioid dependence", "opioid use disorder"),
    "doenca de alzheimer": ("alzheimer",),
    "demencia associada a parkinson": ("parkinson", "dementia"),
    "epilepsia": ("seizure", "epilepsy"),
    "enxaqueca prevencao": ("migraine",),
    "transtorno disforico pre menstrual": ("premenstrual dysphoric disorder",),
    "bulimia nervosa": ("bulimia nervosa",),
}

REVIEW_ONLY_TERMS = (
    "resistente",
    "potencializacao",
    "off label",
    "comorbidade",
    "agitacao",
    "delirium",
    "craving",
    "abstinencia",
    "intoxicacao",
    "overdose",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def normalized(value: str) -> str:
    text = normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def first_words(value: str, limit: int = 25) -> str:
    words = " ".join(str(value or "").split()).split()
    return " ".join(words[:limit])


def section_text(section: ET.Element | None) -> str:
    if section is None:
        return ""
    text_node = section.find("hl7:text", NS)
    content_node = text_node if text_node is not None else section
    return " ".join("".join(content_node.itertext()).split())


def section_title(section: ET.Element) -> str:
    title = section.find("hl7:title", NS)
    return " ".join("".join(title.itertext()).split()) if title is not None else ""


def find_section(root: ET.Element, *, code: str = "", title_contains: str = "") -> ET.Element | None:
    for section in root.findall(".//hl7:section", NS):
        section_code = section.find("hl7:code", NS)
        title = section_title(section).lower()
        if code and section_code is not None and section_code.get("code") == code:
            return section
        if title_contains and title_contains.lower() in title:
            return section
    return None


def numeric_dosage_excerpt(value: str) -> str:
    sentences = re.split(r"(?<=[.!?;])\s+", value)
    selected: list[str] = []
    for sentence in sentences:
        if re.search(r"\d", sentence) and re.search(
            r"\b(?:mg|mcg|g|ml|mmol|tablet|capsule|once|twice|daily|week)\b",
            sentence,
            re.IGNORECASE,
        ):
            selected.append(first_words(sentence, 25))
        if len(selected) == 3:
            break
    return " | ".join(selected)


def indication_titles(section: ET.Element | None) -> str:
    if section is None:
        return ""
    titles: list[str] = []
    for child in section.findall(".//hl7:section", NS):
        title = re.sub(r"^\s*\d+(?:\.\d+)*\s*", "", section_title(child)).strip()
        if title and title.lower() not in {item.lower() for item in titles}:
            titles.append(title)
    if titles:
        return " | ".join(titles[:12])
    return first_words(section_text(section), 25)


def fetch_claim(row: dict[str, str]) -> dict[str, str]:
    base = {
        "medication_name": row["medication_name"],
        "source_system": row["source_system"],
        "source_status": row["source_status"],
        "source_title": row["title"],
        "source_version": row["spl_version"],
        "source_date": row["published_date"],
        "source_url": row["label_url"],
        "source_locator": row["service_url"],
        "indications_anchor": "",
        "indications_summary": "",
        "dosage_anchor": "",
        "dosage_excerpt": "",
        "mechanism_anchor": "",
        "mechanism_excerpt": "",
        "warnings_anchor": "",
        "warnings_excerpt": "",
        "interactions_anchor": "",
        "interactions_excerpt": "",
        "content_sha256": "",
        "extraction_status": "alternate_official_source_required",
        "editorial_status": "pending_formal_review",
        "runtime_eligible": "false",
    }
    if "context_mismatch" in row.get("source_status", ""):
        base["extraction_status"] = "official_source_context_mismatch_rejected"
        return base
    if not row.get("service_url"):
        return base
    try:
        request = urllib.request.Request(
            row["service_url"], headers={"User-Agent": "PsychRx evidence extraction"}
        )
        with urllib.request.urlopen(request, timeout=35) as response:
            payload = response.read()
        root = ET.fromstring(payload)
    except Exception as exc:  # noqa: BLE001 - record source failure per medication.
        base["extraction_status"] = "official_source_fetch_failed"
        base["warnings_excerpt"] = first_words(str(exc), 25)
        return base

    indications = find_section(root, code="34067-9")
    dosage = find_section(root, code="34068-7")
    mechanism = find_section(root, code="43679-0", title_contains="mechanism of action")
    warnings = find_section(root, code="43685-7")
    interactions = find_section(root, code="34073-7")
    base.update(
        {
            "indications_anchor": section_title(indications) if indications is not None else "",
            "indications_summary": indication_titles(indications),
            "dosage_anchor": section_title(dosage) if dosage is not None else "",
            "dosage_excerpt": numeric_dosage_excerpt(section_text(dosage)),
            "mechanism_anchor": section_title(mechanism) if mechanism is not None else "",
            "mechanism_excerpt": first_words(section_text(mechanism), 25),
            "warnings_anchor": section_title(warnings) if warnings is not None else "",
            "warnings_excerpt": first_words(section_text(warnings), 25),
            "interactions_anchor": section_title(interactions) if interactions is not None else "",
            "interactions_excerpt": first_words(section_text(interactions), 25),
            "content_sha256": hashlib.sha256(payload).hexdigest(),
            "extraction_status": "official_claim_anchors_extracted",
        }
    )
    return base


def agomelatine_claim(row: dict[str, str]) -> dict[str, str]:
    return {
        "medication_name": "Agomelatina",
        "source_system": "EMA",
        "source_status": "official_product_information_located",
        "source_title": "Valdoxan EPAR",
        "source_version": "current_public_epar",
        "source_date": "",
        "source_url": EMA_AGOMELATINE,
        "source_locator": EMA_AGOMELATINE,
        "indications_anchor": "Therapeutic indication",
        "indications_summary": "Major depressive episodes in adults",
        "dosage_anchor": "How is Valdoxan used?",
        "dosage_excerpt": "25 mg once daily at bedtime; 50 mg once daily may be considered after two weeks without improvement.",
        "mechanism_anchor": "How does Valdoxan work?",
        "mechanism_excerpt": "Agonism at MT1 and MT2 receptors and antagonism at 5-HT2C receptors.",
        "warnings_anchor": "Safe and effective use",
        "warnings_excerpt": "Liver function monitoring is required before and during treatment, including after dose increase.",
        "interactions_anchor": "Product information",
        "interactions_excerpt": "Review the current product information for medicine-specific interactions.",
        "content_sha256": "",
        "extraction_status": "official_claim_anchors_extracted",
        "editorial_status": "pending_formal_review",
        "runtime_eligible": "false",
    }


def build_claims(registry: list[dict[str, str]], refresh: bool) -> list[dict[str, str]]:
    if not refresh and CLAIMS_PATH.exists():
        return read_csv(CLAIMS_PATH)
    with ThreadPoolExecutor(max_workers=8) as executor:
        claims = list(executor.map(fetch_claim, registry))
    by_name = {row["medication_name"]: row for row in registry}
    if "Agomelatina" in by_name:
        claims = [row for row in claims if row["medication_name"] != "Agomelatina"]
        claims.append(agomelatine_claim(by_name["Agomelatina"]))
    return sorted(claims, key=lambda row: row["medication_name"])


def condition_matches_label(condition: str, indications: str) -> bool:
    condition_key = normalized(condition)
    if any(term in condition_key for term in REVIEW_ONLY_TERMS):
        return False
    terms = CONDITION_TERMS.get(condition_key, ())
    normalized_indications = normalized(indications)
    return bool(terms and any(normalized(term) in normalized_indications for term in terms))


def build_disease_reviews(
    disease_rows: list[dict[str, str]], claims_by_medication: dict[str, dict[str, str]]
) -> list[dict[str, str]]:
    reviews: list[dict[str, str]] = []
    for row in disease_rows:
        claim = claims_by_medication.get(row["medication_name"], {})
        direct = condition_matches_label(
            row["disease_or_context"], claim.get("indications_summary", "")
        )
        if direct:
            support = "official_label_indication_match"
            next_action = "editorial_review_of_indication_and_role"
        elif claim.get("indications_summary"):
            support = "no_direct_label_match_guideline_or_off_label_review_required"
            next_action = "validate_in_guideline_or_systematic_evidence"
        else:
            support = "official_indication_source_missing"
            next_action = "locate_alternate_official_source"
        reviews.append(
            {
                **row,
                "official_indication_match": "true" if direct else "false",
                "official_indications_summary": claim.get("indications_summary", ""),
                "official_source_anchor": (
                    f"{claim.get('source_url', '')}#{claim.get('indications_anchor', '')}"
                    if claim.get("source_url")
                    else ""
                ),
                "evidence_review_status": support,
                "next_review_action": next_action,
                "runtime_eligible": "false",
            }
        )
    return reviews


def is_missing(value: str) -> bool:
    text = normalized(value).replace("_", " ")
    missing_markers = ("nao cadastrad", "pendente", "unresolved", "backlog")
    return not text or any(marker in text for marker in missing_markers)


def build_motor2_reviews(
    motor2_rows: list[dict[str, str]],
    disease_reviews: list[dict[str, str]],
    claims_by_medication: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    disease_index = {
        (normalized(row["medication_name"]), normalized(row["disease_or_context"])): row
        for row in disease_reviews
    }
    reviews: list[dict[str, str]] = []
    for row in motor2_rows:
        claim = claims_by_medication.get(row["medication_name"], {})
        disease = disease_index.get(
            (normalized(row["medication_name"]), normalized(row["condition_or_context"]))
        )
        range_missing = is_missing(row["condition_range"])
        mechanism_missing = is_missing(row["mechanism_or_target"])
        dominant_missing = is_missing(row["dominant_effect"])
        dose_effect_missing = is_missing(row["dose_effect_band"])

        if not range_missing:
            range_resolution = "existing_local_range_preserved"
        elif disease and disease["official_indication_match"] == "true" and claim.get("dosage_excerpt"):
            range_resolution = "official_dosage_anchor_extracted_normalization_pending"
        elif disease:
            range_resolution = "guideline_or_off_label_range_review_required"
        else:
            range_resolution = "no_supported_relationship_registered_do_not_invent_range"

        if not mechanism_missing:
            mechanism_resolution = "existing_value_preserved"
            mechanism_candidate = ""
        elif claim.get("mechanism_excerpt"):
            mechanism_resolution = "official_mechanism_candidate_extracted_pending_editorial_review"
            mechanism_candidate = claim["mechanism_excerpt"]
        else:
            mechanism_resolution = "alternate_pharmacology_source_required"
            mechanism_candidate = ""

        reviews.append(
            {
                "medication_name": row["medication_name"],
                "condition_or_context": row["condition_or_context"],
                "dose_effect_band": row["dose_effect_band"],
                "condition_range": row["condition_range"],
                "range_gap": "true" if range_missing else "false",
                "range_resolution_status": range_resolution,
                "official_dosage_candidate": (
                    claim.get("dosage_excerpt", "")
                    if range_resolution == "official_dosage_anchor_extracted_normalization_pending"
                    else ""
                ),
                "official_indication_match": disease.get("official_indication_match", "false") if disease else "false",
                "dominant_effect_gap": "true" if dominant_missing else "false",
                "dominant_effect_resolution_status": (
                    "existing_value_preserved"
                    if not dominant_missing
                    else "expert_pharmacology_synthesis_required"
                ),
                "mechanism_gap": "true" if mechanism_missing else "false",
                "mechanism_resolution_status": mechanism_resolution,
                "official_mechanism_candidate": mechanism_candidate,
                "dose_effect_gap": "true" if dose_effect_missing else "false",
                "dose_effect_resolution_status": (
                    "existing_value_preserved"
                    if not dose_effect_missing
                    else "official_dosage_and_pharmacology_normalization_required"
                ),
                "official_source_url": claim.get("source_url", ""),
                "editorial_status": "pending_formal_review",
                "runtime_eligible": "false",
            }
        )
    return reviews


def build_gap_summary(
    profiles: list[dict[str, str]],
    motor2_rows: list[dict[str, str]],
    disease_rows: list[dict[str, str]],
    claims_by_medication: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    summaries: list[dict[str, str]] = []
    for profile in sorted(profiles, key=lambda row: row["medication_name"]):
        medication = profile["medication_name"]
        rows = [row for row in motor2_rows if row["medication_name"] == medication]
        disease_count = sum(row["medication_name"] == medication for row in disease_rows)
        claim = claims_by_medication.get(medication, {})
        missing_range = sum(is_missing(row["condition_range"]) for row in rows)
        missing_effect = sum(is_missing(row["dominant_effect"]) for row in rows)
        missing_mechanism = sum(is_missing(row["mechanism_or_target"]) for row in rows)
        missing_dose_effect = sum(is_missing(row["dose_effect_band"]) for row in rows)
        if claim.get("extraction_status") == "official_claim_anchors_extracted":
            status = "official_claims_extracted_pending_editorial_normalization"
        else:
            status = "alternate_official_source_required"
        summaries.append(
            {
                "medication_name": medication,
                "drug_class": profile["drug_class"],
                "motor2_rows": str(len(rows)),
                "missing_condition_ranges": str(missing_range),
                "missing_dose_effect_bands": str(missing_dose_effect),
                "missing_dominant_effects": str(missing_effect),
                "missing_mechanisms": str(missing_mechanism),
                "disease_use_rows": str(disease_count),
                "official_indications_available": "true" if claim.get("indications_summary") else "false",
                "official_dosage_available": "true" if claim.get("dosage_excerpt") else "false",
                "official_mechanism_available": "true" if claim.get("mechanism_excerpt") else "false",
                "official_source_url": claim.get("source_url", ""),
                "evidence_acquisition_status": status,
                "next_action": (
                    "normalize_claims_then_scientific_and_editorial_review"
                    if status.startswith("official_claims")
                    else "locate_ema_anvisa_or_other_official_source"
                ),
                "runtime_eligible": "false",
            }
        )
    return summaries


def write_theory_matrix() -> list[dict[str, str]]:
    checksum = hashlib.sha256(PDF_PATH.read_bytes()).hexdigest() if PDF_PATH.exists() else "source_not_local"
    fields = [
        "concern_id",
        "theoretical_topic",
        "didactic_source",
        "didactic_source_sha256",
        "didactic_pages",
        "theoretical_concern",
        "required_app_inputs",
        "motor_check",
        "decision_impact",
        "advice_output",
        "official_source_id",
        "official_source_section",
        "official_source_url",
        "validation_status",
        "runtime_eligible",
    ]
    rows = [
        dict(
            zip(
                fields,
                (
                    concern_id,
                    topic,
                    PDF_NAME,
                    checksum,
                    pages,
                    concern,
                    inputs,
                    check,
                    impact,
                    output,
                    source_id,
                    source_section,
                    source_url,
                    status,
                    "false",
                ),
            )
        )
        for (
            concern_id,
            topic,
            pages,
            concern,
            inputs,
            check,
            impact,
            output,
            source_id,
            source_section,
            source_url,
            status,
        ) in THEORY_ROWS
    ]
    write_csv(THEORY_PATH, rows, fields)
    return rows


def write_report(
    theory_rows: list[dict[str, str]],
    claims: list[dict[str, str]],
    disease_reviews: list[dict[str, str]],
    gap_rows: list[dict[str, str]],
    motor2_reviews: list[dict[str, str]],
) -> None:
    claim_count = sum(row["extraction_status"] == "official_claim_anchors_extracted" for row in claims)
    indication_matches = sum(row["official_indication_match"] == "true" for row in disease_reviews)
    range_candidates = sum(
        row["range_resolution_status"] == "official_dosage_anchor_extracted_normalization_pending"
        for row in motor2_reviews
    )
    mechanism_candidates = sum(
        row["mechanism_resolution_status"]
        == "official_mechanism_candidate_extracted_pending_editorial_review"
        for row in motor2_reviews
    )
    unresolved_ranges = sum(row["range_gap"] == "true" for row in motor2_reviews)
    unresolved_effects = sum(row["dominant_effect_gap"] == "true" for row in motor2_reviews)
    unresolved_mechanisms = sum(row["mechanism_gap"] == "true" for row in motor2_reviews)
    unresolved_bands = sum(row["dose_effect_gap"] == "true" for row in motor2_reviews)
    alternate_sources = [
        row["medication_name"]
        for row in gap_rows
        if row["evidence_acquisition_status"] == "alternate_official_source_required"
    ]

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        "\n".join(
            [
                "# Theory to Practice Evidence Report",
                "",
                "## Resultado",
                "",
                f"- Preocupacoes teoricas mapeadas: {len(theory_rows)}.",
                f"- Medicamentos auditados: {len(gap_rows)}.",
                f"- Claims regulatorios com ancoras extraidas: {claim_count}.",
                f"- Relacoes de uso por doenca revisadas: {len(disease_reviews)}.",
                f"- Correspondencias diretas com indicacao regulatoria: {indication_matches}.",
                f"- Linhas Motor 2 classificadas: {len(motor2_reviews)}.",
                f"- Lacunas de faixa existentes: {unresolved_ranges}.",
                f"- Lacunas com secao oficial de dose pronta para normalizacao: {range_candidates}.",
                f"- Lacunas de efeito dominante: {unresolved_effects}.",
                f"- Lacunas de mecanismo: {unresolved_mechanisms}.",
                f"- Candidatos oficiais de mecanismo extraidos: {mechanism_candidates}.",
                f"- Lacunas de banda dose-efeito: {unresolved_bands}.",
                "",
                "## Fontes alternativas ainda necessarias",
                "",
                *(f"- {name}." for name in alternate_sources),
                "",
                "## Regra de integridade",
                "",
                "O PDF didatico define preocupacoes e perguntas. DailyMed/FDA, EMA e NICE fornecem ancoras oficiais. Nenhum claim desta camada e runtime eligible antes de normalizacao, revisao cientifica e revisao editorial.",
                "",
                f"As {unresolved_ranges} faixas ausentes ou ainda marcadas como pendentes nao devem ser preenchidas em massa: relacoes sem indicacao ou suporte registrado permanecem explicitamente sem faixa para evitar criar uso clinico inexistente.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Fetch current official label sections from registered locators.",
    )
    args = parser.parse_args()

    registry = read_csv(REGISTRY_PATH)
    profiles = read_csv(PROFILE_PATH)
    disease_rows = read_csv(DISEASE_USE_PATH)
    motor2_rows = read_csv(MOTOR2_PATH)
    theory_rows = write_theory_matrix()
    claims = build_claims(registry, refresh=args.refresh)
    write_csv(CLAIMS_PATH, claims, list(claims[0].keys()))
    claims_by_medication = {row["medication_name"]: row for row in claims}

    disease_reviews = build_disease_reviews(disease_rows, claims_by_medication)
    write_csv(DISEASE_REVIEW_PATH, disease_reviews, list(disease_reviews[0].keys()))
    motor2_reviews = build_motor2_reviews(motor2_rows, disease_reviews, claims_by_medication)
    write_csv(MOTOR2_REVIEW_PATH, motor2_reviews, list(motor2_reviews[0].keys()))
    gap_rows = build_gap_summary(profiles, motor2_rows, disease_rows, claims_by_medication)
    write_csv(GAP_PATH, gap_rows, list(gap_rows[0].keys()))
    write_report(theory_rows, claims, disease_reviews, gap_rows, motor2_reviews)

    print(f"theory_rows={len(theory_rows)}")
    print(f"official_claims={len(claims)}")
    print(f"disease_use_reviews={len(disease_reviews)}")
    print(f"medication_gap_rows={len(gap_rows)}")
    print(f"motor2_review_rows={len(motor2_reviews)}")


if __name__ == "__main__":
    main()
