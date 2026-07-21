"""Build source-transparent age-population evidence rows for PsychRx.

The generated catalog is informational. It preserves official population text
and source locators, but it does not authorize medication selection, dosing or
therapeutic runtime use.
"""

from __future__ import annotations

import csv
import hashlib
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = ROOT / "knowledge_base" / "decision_support_engine" / "tables"
CLAIMS_PATH = TABLE_DIR / "medication_official_claims.csv"
OUTPUT_PATH = TABLE_DIR / "medication_population_evidence.csv"

NS = {"hl7": "urn:hl7-org:v3"}
PEDIATRIC_CODE = "34081-0"
GERIATRIC_CODE = "34082-8"
DOSAGE_CODE = "34068-7"

AGE_BANDS = (
    ("CHILD", "0", "11"),
    ("ADOLESCENT", "12", "17"),
    ("ADULT", "18", "64"),
    ("OLDER_ADULT", "65", ""),
)

FIELDS = (
    "medication_name",
    "age_band",
    "age_min_years",
    "age_max_years",
    "source_system",
    "source_abbreviation",
    "source_title",
    "source_version",
    "source_date",
    "source_url",
    "source_locator",
    "population_anchor",
    "population_summary",
    "dosage_anchor",
    "dosage_summary",
    "evidence_status",
    "scientific_review_status",
    "editorial_status",
    "display_eligible",
    "therapeutic_runtime_eligible",
    "content_sha256",
)


ALTERNATE_OFFICIAL_SOURCES = {
    "Agomelatina": {
        "source_system": "EMA",
        "source_abbreviation": "EMA",
        "source_title": "Valdoxan EPAR and product information",
        "source_version": "EPAR current product information",
        "source_date": "2026-07-20",
        "source_url": "https://www.ema.europa.eu/en/medicines/human/EPAR/valdoxan",
        "source_locator": "SmPC sections 4.1, 4.2 and 4.4",
        "child": "Valdoxan is authorised for major depressive episodes in adults; paediatric use is not an authorised indication.",
        "adolescent": "Valdoxan is authorised for major depressive episodes in adults; the EMA paediatric-extension claim was withdrawn.",
        "adult": "Valdoxan is authorised for treatment of major depressive episodes in adults.",
        "older": "Efficacy is documented below 75 years; EMA product information recommends against use from 75 years because efficacy was not demonstrated.",
        "dosage": "Adult product information describes 25 mg at bedtime, with possible increase to 50 mg after clinical review.",
    },
    "Amissulprida": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Amisulpride 100 mg Tablets - SmPC",
        "source_version": "text revision 2026-01-15",
        "source_date": "2026-01-15",
        "source_url": "https://www.medicines.org.uk/emc/product/101726/smpc",
        "source_locator": "SmPC sections 4.1-4.3",
        "child": "Use is contraindicated under 15 years; efficacy and safety under 18 years have not been established.",
        "adolescent": "Use under 18 years is not established; ages 15-17 require specialist initiation only if absolutely necessary.",
        "adult": "The SmPC indication is acute and chronic schizophrenic disorders in adults.",
        "older": "Treatment over 65 years is not recommended; if unavoidable, particular caution and possible dose reduction are required.",
        "dosage": "Adult dosage depends on positive or negative symptom predominance; the SmPC provides condition-specific ranges.",
    },
    "Bromazepam": {
        "source_system": "Health Canada",
        "source_abbreviation": "HC",
        "source_title": "BROMAZEPAM Product Monograph",
        "source_version": "Control No. 216862",
        "source_date": "2018-09-06",
        "source_url": "https://pdf.hres.ca/dpd_pm/00062167.PDF",
        "source_locator": "Indications and Clinical Use; Special Populations; Dosage and Administration",
        "child": "The product monograph does not recommend bromazepam below 18 years because clinical experience is insufficient.",
        "adolescent": "The product monograph does not recommend bromazepam below 18 years because clinical experience is insufficient.",
        "adult": "The monograph supports short-term symptomatic relief of excessive anxiety in anxiety neurosis.",
        "older": "Older and debilitated patients are more susceptible to dose-related adverse events and require a reduced initial dose.",
        "dosage": "The monograph separates usual adult dosing from a lower initial dose for older or debilitated patients.",
    },
    "Clomipramina": {
        "source_system": "DailyMed/FDA",
        "source_abbreviation": "DM",
        "source_title": "ANAFRANIL (clomipramine hydrochloride) Capsules - Official Label",
        "source_version": "NDA label update 2024-11-26",
        "source_date": "2024-11-26",
        "source_url": "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=4074b555-7635-41a9-809d-fae3b3610059",
        "source_locator": "Indications and Usage; Pediatric Use; Geriatric Use; Dosage and Administration",
        "child": "OCD is the only authorised paediatric indication; safety and effectiveness below 10 years have not been established.",
        "adolescent": "The official label supports OCD treatment from age 10, with a separate child/adolescent titration and weight-related maximum.",
        "adult": "The official indication is obsessions and compulsions in obsessive-compulsive disorder.",
        "older": "Evidence from age 65 is limited; cautious dose selection from the low end of the range is advised.",
        "dosage": "The label separates adult dosing from child/adolescent OCD dosing and provides weight-related paediatric limits.",
    },
    "Dosulepina": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Dosulepin Tablets 75 mg - SmPC",
        "source_version": "emc update 2025-11-12",
        "source_date": "2025-11-12",
        "source_url": "https://www.medicines.org.uk/emc/product/101606/smpc",
        "source_locator": "SmPC sections 4.1, 4.2 and 4.4",
        "child": "Dosulepin is not recommended for children.",
        "adolescent": "Dosulepin is not recommended for children and has no adolescent dosing authorised in this SmPC.",
        "adult": "Use is restricted to depressive illness when alternative treatment is not tolerated or has not worked.",
        "older": "The SmPC provides a lower initial range and highlights increased adverse-effect and cardiovascular susceptibility in older people.",
        "dosage": "The SmPC separates adult and older-person starting doses and restricts initiation to specialist care in new patients.",
    },
    "Levomepromazina": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Levomepromazine Maleate 25 mg Tablets - SmPC",
        "source_version": "emc product 11912",
        "source_date": "2026-07-20",
        "source_url": "https://www.medicines.org.uk/emc/product/11912/smpc",
        "source_locator": "SmPC sections 4.1, 4.2 and 4.4",
        "child": "Paediatric patients are particularly susceptible to hypotensive and sedative effects; the SmPC gives a paediatric ceiling for this formulation.",
        "adolescent": "Paediatric dosing is formulation-specific and requires special caution because of hypotensive and sedative effects.",
        "adult": "The SmPC separates psychiatric-condition dosing from terminal-illness dosing.",
        "older": "Older ambulant patients require prior assessment of hypotensive-reaction risk; dementia-related behavioural use is not licensed.",
        "dosage": "The SmPC gives distinct adult psychiatric, terminal-illness and paediatric instructions; formulations are not interchangeable.",
    },
    "Maprotilina": {
        "source_system": "Health Canada",
        "source_abbreviation": "HC",
        "source_title": "TEVA-MAPROTILINE Product Monograph",
        "source_version": "Control No. 145859",
        "source_date": "2011-10-20",
        "source_url": "https://pdf.hres.ca/dpd_pm/00014410.PDF",
        "source_locator": "Warnings; Dosage and Administration",
        "child": "The product monograph does not recommend maprotiline for children.",
        "adolescent": "The product monograph does not provide an authorised adolescent regimen and does not recommend use in children.",
        "adult": "The monograph provides an adult depression regimen with gradual titration.",
        "older": "Lower initial dosing, gradual increases and close cardiovascular surveillance are recommended for older or debilitated patients.",
        "dosage": "Adult and older/debilitated starting regimens are explicitly separated in the product monograph.",
    },
    "Mianserina": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Mianserin 30 mg film-coated tablets - SmPC",
        "source_version": "emc update 2026-06-30",
        "source_date": "2026-06-30",
        "source_url": "https://www.medicines.org.uk/emc/product/2741/smpc",
        "source_locator": "SmPC sections 4.2 and 4.4",
        "child": "Mianserin should not be used below 18 years; long-term growth, maturation and behavioural safety data are lacking.",
        "adolescent": "Mianserin should not be used below 18 years; monitoring is required if exceptional clinical need leads to use.",
        "adult": "The SmPC describes adult treatment for depressive illness.",
        "older": "Use over 65 years is restricted; the SmPC describes a lower initial and maintenance approach.",
        "dosage": "Adult and older-person dosing are separated in the SmPC.",
    },
    "Naltrexona": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Naltrexone hydrochloride 50 mg film-coated tablets - SmPC",
        "source_version": "emc update 2023-07-12",
        "source_date": "2023-07-12",
        "source_url": "https://www.medicines.org.uk/emc/product/8968/smpc",
        "source_locator": "SmPC sections 4.1, 4.2 and 4.4",
        "child": "Naltrexone tablets are not recommended below 18 years because safe use has not been established.",
        "adolescent": "Naltrexone tablets are not recommended below 18 years because safe use has not been established.",
        "adult": "The SmPC describes naltrexone as adjunctive therapy in opioid- and alcohol-dependence care.",
        "older": "Safe use for opioid dependence in older people has not been established; hepatic monitoring and caution are emphasised.",
        "dosage": "The SmPC provides an adult oral regimen and explicitly records absent paediatric and older-person evidence.",
    },
    "Sulpirida": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Sulpiride 400 mg Film-Coated Tablets - SmPC",
        "source_version": "text revision 2019-11-08",
        "source_date": "2019-11-08",
        "source_url": "https://www.medicines.org.uk/emc/product/2431/smpc",
        "source_locator": "SmPC sections 4.2 and 4.4",
        "child": "Clinical experience under 14 years is insufficient for specific recommendations.",
        "adolescent": "Paediatric efficacy and safety have not been thoroughly investigated; the SmPC requires caution.",
        "adult": "The SmPC separates positive, negative and mixed symptom dosing in schizophrenia.",
        "older": "The adult ranges may apply, but particular caution and renal-function-related dose reduction are required.",
        "dosage": "The SmPC provides symptom-pattern dosing and separate older-person cautions.",
    },
    "Zopiclona": {
        "source_system": "UK SmPC",
        "source_abbreviation": "UK-SMPC",
        "source_title": "Zopiclone 3.75 mg film-coated tablets - SmPC",
        "source_version": "emc update 2026-04-20",
        "source_date": "2026-04-20",
        "source_url": "https://www.medicines.org.uk/emc/product/10830/smpc",
        "source_locator": "SmPC sections 4.1, 4.2 and 4.4",
        "child": "Zopiclone should not be used below 18 years because safety and efficacy have not been established.",
        "adolescent": "Zopiclone should not be used below 18 years because safety and efficacy have not been established.",
        "adult": "The indication is short-term treatment of insomnia in adults when insomnia is disabling or causes severe distress.",
        "older": "The SmPC specifies a lower starting dose for older people and highlights fall and paradoxical-reaction risks.",
        "dosage": "The SmPC separates adult and older-person dosing and limits treatment duration.",
    },
}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _compact(value: str, word_limit: int = 90) -> str:
    words = " ".join(str(value or "").split()).split()
    return " ".join(words[:word_limit])


def _section_title(section: ET.Element | None) -> str:
    if section is None:
        return ""
    title = section.find("hl7:title", NS)
    return _compact("".join(title.itertext()), 20) if title is not None else ""


def _section_text(section: ET.Element | None) -> str:
    if section is None:
        return ""
    text = section.find("hl7:text", NS)
    content = text if text is not None else section
    return _compact("".join(content.itertext()))


def _section_by_code(root: ET.Element, code_value: str) -> ET.Element | None:
    for section in root.findall(".//hl7:section", NS):
        code = section.find("hl7:code", NS)
        if code is not None and code.get("code") == code_value:
            return section
    return None


def _section_by_title(root: ET.Element, phrases: tuple[str, ...]) -> ET.Element | None:
    """Locate a clinical subsection when older SPLs use a generic LOINC code."""
    matches: list[tuple[int, int, ET.Element]] = []
    for section in root.findall(".//hl7:section", NS):
        title = _section_title(section)
        lowered = title.lower()
        if not any(phrase in lowered for phrase in phrases):
            continue
        exact_rank = 0 if lowered.strip("0123456789. -") in phrases else 1
        matches.append((exact_rank, len(title), section))
    return min(matches, default=(0, 0, None), key=lambda item: (item[0], item[1]))[2]


def _clinical_population_fallback(root: ET.Element, terms: tuple[str, ...]) -> str:
    """Extract only bounded clinical sentences, never packaging/full-document text."""
    clinical_markers = (
        "patient",
        "safety",
        "efficacy",
        "effectiveness",
        "dose",
        "dosage",
        "treatment",
        "use",
        "risk",
        "recommended",
        "established",
    )
    candidates: list[tuple[int, int, str]] = []
    seen: set[str] = set()
    for section in root.findall(".//hl7:section", NS):
        text_element = section.find("hl7:text", NS)
        if text_element is None:
            continue
        text = " ".join("".join(text_element.itertext()).split())
        for sentence in re.split(r"(?<=[.!?;])\s+", text):
            lowered = sentence.lower()
            if not (30 <= len(sentence) <= 800):
                continue
            if not any(term in lowered for term in terms):
                continue
            if not any(marker in lowered for marker in clinical_markers):
                continue
            normalized = _compact(sentence)
            if normalized in seen:
                continue
            seen.add(normalized)
            preferred = 0 if any(
                phrase in lowered
                for phrase in (
                    "pediatric use",
                    "geriatric use",
                    "safety and effectiveness",
                    "elderly patients",
                )
            ) else 1
            candidates.append((preferred, len(sentence), normalized))
    candidates.sort(key=lambda item: (item[0], item[1]))
    return _compact(" ".join(item[2] for item in candidates[:3]))


def _fetch_dailymed(row: dict[str, str]) -> tuple[bytes, ET.Element]:
    request = urllib.request.Request(
        row["source_locator"], headers={"User-Agent": "PsychRx population evidence"}
    )
    with urllib.request.urlopen(request, timeout=40) as response:
        payload = response.read()
    return payload, ET.fromstring(payload)


def _daily_med_rows(claim: dict[str, str]) -> list[dict[str, str]]:
    payload, root = _fetch_dailymed(claim)
    pediatric = _section_by_code(root, PEDIATRIC_CODE)
    if pediatric is None:
        pediatric = _section_by_title(root, ("pediatric use", "pediatric patients"))
    geriatric = _section_by_code(root, GERIATRIC_CODE)
    if geriatric is None:
        geriatric = _section_by_title(
            root, ("geriatric use", "elderly patients", "dosage for elderly patients")
        )
    dosage = _section_by_code(root, DOSAGE_CODE)
    pediatric_text = _section_text(pediatric) or _clinical_population_fallback(
        root, ("pediatric", "children", "adolescent")
    )
    geriatric_text = _section_text(geriatric) or _clinical_population_fallback(
        root, ("geriatric", "elderly", "older patient")
    )
    adult_text = _compact(
        " ".join(
            item
            for item in (claim.get("indications_summary", ""), claim.get("dosage_excerpt", ""))
            if item
        )
    )
    band_text = {
        "CHILD": pediatric_text,
        "ADOLESCENT": pediatric_text,
        "ADULT": adult_text,
        "OLDER_ADULT": geriatric_text,
    }
    band_anchor = {
        "CHILD": _section_title(pediatric) or "bounded clinical population-text extraction",
        "ADOLESCENT": _section_title(pediatric) or "bounded clinical population-text extraction",
        "ADULT": claim.get("dosage_anchor", "") or _section_title(dosage),
        "OLDER_ADULT": _section_title(geriatric) or "bounded clinical population-text extraction",
    }
    rows = []
    for band, minimum, maximum in AGE_BANDS:
        summary = band_text[band]
        status = (
            "official_population_section_located"
            if band_anchor[band] and "extraction" not in band_anchor[band]
            else "official_population_text_located"
            if summary
            else "official_population_statement_not_found"
        )
        rows.append(
            {
                "medication_name": claim["medication_name"],
                "age_band": band,
                "age_min_years": minimum,
                "age_max_years": maximum,
                "source_system": "DailyMed/FDA",
                "source_abbreviation": "DM",
                "source_title": claim.get("source_title", ""),
                "source_version": claim.get("source_version", ""),
                "source_date": claim.get("source_date", ""),
                "source_url": claim.get("source_url", ""),
                "source_locator": claim.get("source_locator", ""),
                "population_anchor": band_anchor[band],
                "population_summary": summary,
                "dosage_anchor": claim.get("dosage_anchor", "") or _section_title(dosage),
                "dosage_summary": claim.get("dosage_excerpt", "") or _section_text(dosage),
                "evidence_status": status,
                "scientific_review_status": "official_source_extracted_pending_clinical_review",
                "editorial_status": "source_excerpt_display_only",
                "display_eligible": "true" if summary else "false",
                "therapeutic_runtime_eligible": "false",
                "content_sha256": hashlib.sha256(payload).hexdigest(),
            }
        )
    return rows


def _alternate_rows(medication_name: str) -> list[dict[str, str]]:
    source = ALTERNATE_OFFICIAL_SOURCES[medication_name]
    summaries = {
        "CHILD": source["child"],
        "ADOLESCENT": source["adolescent"],
        "ADULT": source["adult"],
        "OLDER_ADULT": source["older"],
    }
    rows = []
    for band, minimum, maximum in AGE_BANDS:
        summary = summaries[band]
        rows.append(
            {
                "medication_name": medication_name,
                "age_band": band,
                "age_min_years": minimum,
                "age_max_years": maximum,
                "source_system": source["source_system"],
                "source_abbreviation": source["source_abbreviation"],
                "source_title": source["source_title"],
                "source_version": source["source_version"],
                "source_date": source["source_date"],
                "source_url": source["source_url"],
                "source_locator": source["source_locator"],
                "population_anchor": source["source_locator"],
                "population_summary": summary,
                "dosage_anchor": source["source_locator"],
                "dosage_summary": source["dosage"],
                "evidence_status": "alternate_official_product_information_curated",
                "scientific_review_status": "official_source_extracted_pending_clinical_review",
                "editorial_status": "source_summary_display_only",
                "display_eligible": "true",
                "therapeutic_runtime_eligible": "false",
                "content_sha256": hashlib.sha256(
                    (source["source_url"] + summary + source["dosage"]).encode("utf-8")
                ).hexdigest(),
            }
        )
    return rows


def build() -> list[dict[str, str]]:
    rows = []
    for claim in _read_csv(CLAIMS_PATH):
        medication_name = claim["medication_name"]
        if medication_name in ALTERNATE_OFFICIAL_SOURCES:
            rows.extend(_alternate_rows(medication_name))
            continue
        if not claim.get("source_locator", "").startswith("https://dailymed.nlm.nih.gov/"):
            raise RuntimeError(f"official population source missing: {medication_name}")
        rows.extend(_daily_med_rows(claim))
    return rows


def main() -> None:
    rows = build()
    _write_csv(OUTPUT_PATH, rows)
    missing = sum(not row["population_summary"] for row in rows)
    print(
        f"Medication population evidence: {len(rows)} rows, "
        f"{len({row['medication_name'] for row in rows})} medications, "
        f"{missing} missing population summaries."
    )


if __name__ == "__main__":
    main()
