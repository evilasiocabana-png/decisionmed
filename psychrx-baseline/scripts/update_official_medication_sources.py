"""Locate official medication sources and attach them to the motor tables.

This script performs source intake only. It does not extract clinical claims,
does not validate mechanisms, and does not make any runtime field eligible.
It records official regulatory locators so later review can fill pending
fields with source, section, and excerpt.
"""

from __future__ import annotations

import csv
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "knowledge_base" / "decision_support_engine" / "tables"
REGISTRY_PATH = TABLE_DIR / "medication_official_source_registry.csv"
REPORT_PATH = ROOT / "docs" / "decision_support_engine" / "MOTOR_OFFICIAL_SOURCE_INTAKE_REPORT.md"

MATRIX_PATH = TABLE_DIR / "pharmacological_decision_matrix.csv"
PENDING_AUDIT_PATH = TABLE_DIR / "medication_explanation_pending_audit.csv"
PROFILE_BACKLOG_PATH = TABLE_DIR / "medication_explanation_profile_backlog.csv"
MOTOR2_PATH = TABLE_DIR / "motor2_strategy_matrix.csv"

DAILYMED_SEARCH = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json"
DAILYMED_LABEL = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={setid}"
DAILYMED_SERVICE = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml"


QUERY_MAP = {
    "Acamprosato": "acamprosate",
    "Agomelatina": "agomelatine",
    "Alprazolam": "alprazolam",
    "Amissulprida": "amisulpride",
    "Amitriptilina": "amitriptyline",
    "Aripiprazol": "aripiprazole",
    "Asenapina": "asenapine",
    "Atomoxetina": "atomoxetine",
    "Brexpiprazol": "brexpiprazole",
    "Bromazepam": "bromazepam",
    "Buprenorfina": "buprenorphine",
    "Bupropiona": "bupropion",
    "Bupropiona XL": "bupropion",
    "Buspirona": "buspirone",
    "Carbamazepina": "carbamazepine",
    "Cariprazina": "cariprazine",
    "Citalopram": "citalopram",
    "Clobazam": "clobazam",
    "Clomipramina": "clomipramine",
    "Clonazepam": "clonazepam",
    "Clonidina": "clonidine",
    "Clozapina": "clozapine",
    "Clorpromazina": "chlorpromazine",
    "Desipramina": "desipramine",
    "Desvenlafaxina": "desvenlafaxine",
    "Diazepam": "diazepam",
    "Dissulfiram": "disulfiram",
    "Divalproato": "divalproex sodium",
    "Donepezila": "donepezil",
    "Dosulepina": "dosulepin",
    "Doxepina": "doxepin",
    "Droperidol": "droperidol",
    "Duloxetina": "duloxetine",
    "Escitalopram": "escitalopram",
    "Eszopiclona": "eszopiclone",
    "Fenitoina": "phenytoin",
    "Fenobarbital": "phenobarbital",
    "Fluoxetina": "fluoxetine",
    "Fluvoxamina": "fluvoxamine",
    "Galantamina": "galantamine",
    "Guanfacina XR": "guanfacine",
    "Haloperidol": "haloperidol",
    "Imipramina": "imipramine",
    "Lamotrigina": "lamotrigine",
    "Levomepromazina": "levomepromazine",
    "Lisdexanfetamina": "lisdexamfetamine",
    "Litio": "lithium",
    "Lorazepam": "lorazepam",
    "Lurasidona": "lurasidone",
    "Maprotilina": "maprotiline",
    "Memantina": "memantine",
    "Metadona": "methadone",
    "Metilfenidato IR": "methylphenidate",
    "Metilfenidato LP": "methylphenidate",
    "Mianserina": "mianserin",
    "Midazolam": "midazolam",
    "Mirtazapina": "mirtazapine",
    "Naloxona": "naloxone",
    "Naltrexona": "naltrexone",
    "Nortriptilina": "nortriptyline",
    "Olanzapina": "olanzapine",
    "Oxazepam": "oxazepam",
    "Oxcarbazepina": "oxcarbazepine",
    "Paliperidona": "paliperidone",
    "Paroxetina": "paroxetine",
    "Prometazina": "promethazine",
    "Quetiapina": "quetiapine",
    "Risperidona": "risperidone",
    "Rivastigmina": "rivastigmine",
    "Sertralina": "sertraline",
    "Sulpirida": "sulpiride",
    "Temazepam": "temazepam",
    "Tioridazina": "thioridazine",
    "Topiramato": "topiramate",
    "Trazodona": "trazodone",
    "Valproato": "valproic acid",
    "Venlafaxina": "venlafaxine",
    "Venlafaxina XR": "venlafaxine",
    "Vilazodona": "vilazodone",
    "Vortioxetina": "vortioxetine",
    "Ziprasidona": "ziprasidone",
    "Zolpidem": "zolpidem",
    "Zopiclona": "zopiclone",
}

LOW_PRIORITY_TITLE_TERMS = (
    "repack",
    "prepack",
    "unit dose",
    "unit-dose",
    "a-s medication",
    "bryant ranch",
    "remedypack",
    "remedyrepack",
    "pd-rx",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def medications() -> list[str]:
    rows = read_csv(MATRIX_PATH)
    return sorted({row["drug_name"].strip() for row in rows if row.get("drug_name", "").strip()})


def dailymed_search(query: str) -> dict[str, str]:
    params = urllib.parse.urlencode(
        {
            "drug_name": query,
            "label_type": "human/rxonly",
            "pagesize": "20",
        }
    )
    url = f"{DAILYMED_SEARCH}?{params}"
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "PsychRx source registry"})
        with urllib.request.urlopen(request, timeout=25) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - source intake must continue.
        return {
            "status": "not_found",
            "error": str(exc),
            "query_url": url,
        }

    data = payload.get("data") or []
    if not data:
        return {
            "status": "not_found",
            "error": "",
            "query_url": url,
        }

    selected = sorted(data, key=_label_score, reverse=True)[0]
    setid = selected.get("setid", "")
    title = selected.get("title", "")
    context_status = _context_status(query, title)
    return {
        "status": context_status,
        "setid": setid,
        "title": title,
        "published_date": selected.get("published_date", ""),
        "spl_version": str(selected.get("spl_version", "")),
        "label_url": DAILYMED_LABEL.format(setid=setid),
        "service_url": DAILYMED_SERVICE.format(setid=setid),
        "query_url": url,
        "error": "",
    }


def _label_score(label: dict[str, object]) -> int:
    title = str(label.get("title", "")).lower()
    score = 100
    for term in LOW_PRIORITY_TITLE_TERMS:
        if term in title:
            score -= 20
    if "[" not in title:
        score += 10
    if "tablet" in title or "capsule" in title or "solution" in title:
        score += 5
    return score


def _context_status(query: str, title: str) -> str:
    normalized_query = query.lower()
    normalized_title = title.lower()
    if normalized_query == "amisulpride" and (
        "barhemsys" in normalized_title or "injection" in normalized_title
    ):
        return "official_label_located_context_mismatch_review_required"
    return "official_label_located_pending_formal_review"


def build_registry() -> list[dict[str, str]]:
    registry: list[dict[str, str]] = []
    for medication in medications():
        query = QUERY_MAP.get(medication, medication)
        result = dailymed_search(query)
        registry.append(
            {
                "medication_name": medication,
                "official_query": query,
                "source_system": "DailyMed/FDA",
                "source_status": result.get("status", "not_found"),
                "setid": result.get("setid", ""),
                "title": result.get("title", ""),
                "published_date": result.get("published_date", ""),
                "spl_version": result.get("spl_version", ""),
                "label_url": result.get("label_url", ""),
                "service_url": result.get("service_url", ""),
                "query_url": result.get("query_url", ""),
                "source_use": (
                    "official regulatory locator for later dose, safety, "
                    "contraindication, warning, and adverse reaction extraction"
                ),
                "review_status": _review_status(result.get("status", "not_found")),
                "notes": result.get("error", ""),
            }
        )
        time.sleep(0.05)
    return registry


def registry_by_medication(registry: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row["medication_name"]: row for row in registry}


def _review_status(status: str) -> str:
    if status == "official_label_located_context_mismatch_review_required":
        return "source_locator_context_mismatch_no_clinical_claim_extracted"
    if status != "not_found":
        return "source_locator_only_no_clinical_claim_extracted"
    return "official_source_not_found_in_dailymed"


def source_token(source: dict[str, str]) -> str:
    if source.get("source_status") == "not_found" or not source.get("label_url"):
        return "DM:PENDENTE_PESQUISAR"
    return f"DM:{source['label_url']}"


def append_source(existing: str, token: str) -> str:
    if not token or token in existing:
        return existing
    if not existing:
        return token
    return f"{existing}; {token}"


def update_pending_audit(registry: list[dict[str, str]]) -> None:
    by_med = registry_by_medication(registry)
    rows = read_csv(PENDING_AUDIT_PATH)
    for row in rows:
        source = by_med.get(row["medication_name"])
        if not source:
            continue
        row["source_reference"] = append_source(row["source_reference"], source_token(source))
        if source["source_status"] != "not_found":
            row["source_status"] = "official_label_located_pending_formal_review"
            row["next_research_need"] = (
                "extrair secao, trecho e campo especifico da fonte oficial "
                "antes de promover para validated_for_table"
            )
    write_csv(PENDING_AUDIT_PATH, rows, list(rows[0].keys()))


def update_profile_backlog(registry: list[dict[str, str]]) -> None:
    by_med = registry_by_medication(registry)
    rows = read_csv(PROFILE_BACKLOG_PATH)
    for row in rows:
        source = by_med.get(row["medication_name"])
        if not source:
            continue
        row["source_reference"] = append_source(row["source_reference"], source_token(source))
        if source["source_status"] != "not_found":
            row["current_source_status"] = "official_label_located_pending_formal_review"
        if "DM=DailyMed/FDA" not in row.get("source_legend", ""):
            row["source_legend"] = append_source(row.get("source_legend", ""), "DM=DailyMed/FDA")
    write_csv(PROFILE_BACKLOG_PATH, rows, list(rows[0].keys()))


def update_motor2(registry: list[dict[str, str]]) -> None:
    by_med = registry_by_medication(registry)
    rows = read_csv(MOTOR2_PATH)
    for row in rows:
        source = by_med.get(row["medication_name"])
        if not source:
            continue
        row["dose_effect_source"] = append_source(row["dose_effect_source"], source_token(source))
    write_csv(MOTOR2_PATH, rows, list(rows[0].keys()))


def write_report(registry: list[dict[str, str]]) -> None:
    located = [row for row in registry if row["source_status"] != "not_found"]
    missing = [row for row in registry if row["source_status"] == "not_found"]
    lines = [
        "# Motor Official Source Intake Report",
        "",
        "## Objetivo",
        "",
        "Registrar locators oficiais de fonte regulatoria para alimentar a pesquisa do Motor Farmacologico sem extrair ou validar conteudo clinico automaticamente.",
        "",
        "## Fonte consultada",
        "",
        "- DailyMed/FDA REST API: https://dailymed.nlm.nih.gov/dailymed/services/",
        "- DailyMed public label pages: https://dailymed.nlm.nih.gov/dailymed/",
        "",
        "## Resultado",
        "",
        f"- Medicamentos pesquisados: {len(registry)}",
        f"- Fonte DailyMed/FDA localizada: {len(located)}",
        f"- Nao localizado em DailyMed/FDA nesta etapa: {len(missing)}",
        "",
        "## Limite",
        "",
        "Esta etapa registra fonte oficial localizada. Ela nao transforma nenhum campo em recomendacao, nao extrai mecanismo, nao define dose para paciente e nao libera runtime clinico.",
        "",
        "## Pendentes fora de DailyMed/FDA",
        "",
    ]
    for row in missing:
        lines.append(f"- {row['medication_name']} -> pesquisar EMA, ANVISA, NICE, APA, Stahl ou Goodman conforme campo.")
    lines.extend(
        [
            "",
            "## Proximo passo",
            "",
            "Executar extracao campo a campo apenas quando houver fonte, secao, trecho revisavel e revisao editorial/cientifica.",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    registry = build_registry()
    write_csv(
        REGISTRY_PATH,
        registry,
        [
            "medication_name",
            "official_query",
            "source_system",
            "source_status",
            "setid",
            "title",
            "published_date",
            "spl_version",
            "label_url",
            "service_url",
            "query_url",
            "source_use",
            "review_status",
            "notes",
        ],
    )
    update_pending_audit(registry)
    update_profile_backlog(registry)
    update_motor2(registry)
    write_report(registry)
    located = sum(1 for row in registry if row["source_status"] != "not_found")
    print(f"Official source registry updated: {located}/{len(registry)} DailyMed/FDA locators found.")


if __name__ == "__main__":
    main()
