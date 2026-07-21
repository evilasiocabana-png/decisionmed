"""Read the PsychRx unified motor table from the curated workbook.

The repository is intentionally lightweight and uses only the Python standard
library. It reads the reviewed workbook as a source table for decision support
without modifying the scientific corpus or enabling autonomous prescribing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from unicodedata import normalize
from zipfile import ZipFile
import xml.etree.ElementTree as ET

from application.clinical_decision_support_contract import EvidenceCitationPayload


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TABLE_PATH = (
    PROJECT_ROOT
    / "knowledge_base"
    / "decision_support_engine"
    / "tables"
    / "Tabela_Motor_Unificada_audit_evilasio.xlsx"
)

SPREADSHEET_NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass(frozen=True)
class MotorTableEntry:
    """One row from the reviewed unified motor table."""

    row_id: str
    entity: str
    item_type: str
    drug_class: str
    sources: str
    motor_use: str
    symptom_targets: str
    indication_context: str
    dose_range: str
    half_life: str
    appetite_weight: str
    libido: str
    action_serotonin: str
    action_dopamine: str
    action_noradrenaline: str
    action_histamine: str
    cautions: str
    derived_question: str
    allowed_actions: str
    do_not_mix_with: str
    status: str

    def citation(self, section: str = "") -> EvidenceCitationPayload:
        """Return a traceable citation to the table row."""
        return EvidenceCitationPayload(
            source_id=f"PSYCHRX-TABELA-MOTOR-{self.row_id}",
            title="Tabela Motor Unificada auditada por Evilasio",
            organization="PsychRx",
            year="2026",
            section=section or f"Tabela Motor / {self.row_id}",
            excerpt_anchor=self.row_id.lower(),
            evidence_type="curated_decision_support_table",
            quality="local_reviewed_table",
            applicability="physician_review_only",
            limitations=(
                "Tabela local de suporte a decisao; nao substitui julgamento "
                "medico, bula, diretriz, contraindicoes ou revisao clinica."
            ),
        )


class MotorTableRepository:
    """Loads and queries the reviewed motor workbook."""

    def __init__(self, workbook_path: Path | None = None) -> None:
        self._workbook_path = workbook_path or DEFAULT_TABLE_PATH
        self._entries: tuple[MotorTableEntry, ...] | None = None

    def entries(self) -> tuple[MotorTableEntry, ...]:
        """Return all entries from the Tabela Motor worksheet."""
        if self._entries is None:
            self._entries = self._load_entries()
        return self._entries

    def find_current(self, medication_name: str) -> MotorTableEntry | None:
        """Find a row matching a currently used medication."""
        normalized = self._normalize(medication_name)
        if not normalized:
            return None
        for entry in self.entries():
            entity = self._normalize(entry.entity)
            if entity and (entity in normalized or normalized in entity):
                return entry
        return None

    def substitution_candidates(
        self,
        target: str,
        current_names: tuple[str, ...],
    ) -> tuple[MotorTableEntry, ...]:
        """Return table rows that can support substitution review."""
        return self._candidates(target, current_names, ("substituir",))

    def association_candidates(
        self,
        target: str,
        current_names: tuple[str, ...],
    ) -> tuple[MotorTableEntry, ...]:
        """Return table rows that can support association review."""
        return self._candidates(target, current_names, ("associar", "associacao"))

    def _candidates(
        self,
        target: str,
        current_names: tuple[str, ...],
        action_terms: tuple[str, ...],
    ) -> tuple[MotorTableEntry, ...]:
        current = {self._normalize(name) for name in current_names}
        matched: list[MotorTableEntry] = []
        for entry in self.entries():
            if self._normalize(entry.entity) in current:
                continue
            if entry.item_type.lower() != "medicamento":
                continue
            actions = self._normalize(entry.allowed_actions)
            if not any(self._normalize(term) in actions for term in action_terms):
                continue
            if self._matches_target(entry, target):
                matched.append(entry)
        return tuple(matched)

    def _matches_target(self, entry: MotorTableEntry, target: str) -> bool:
        haystack = self._normalize(
            " ".join(
                (
                    entry.motor_use,
                    entry.symptom_targets,
                    entry.indication_context,
                    entry.drug_class,
                )
            )
        )
        target_terms = self._target_terms(target)
        return any(term in haystack for term in target_terms)

    def _target_terms(self, target: str) -> tuple[str, ...]:
        normalized = self._normalize(target)
        terms: set[str] = set()
        if any(term in normalized for term in ("sono", "sedacao", "ativacao")):
            terms.update(("sono", "sedacao", "insonia", "ativacao"))
        if any(term in normalized for term in ("ansiedade", "seroton")):
            terms.update(("ansiedade", "seroton", "toc"))
        if any(term in normalized for term in ("humor", "energia", "antidepressivo")):
            terms.update(("humor", "energia", "depressao", "antidepressivo", "fadiga"))
        if "dor" in normalized:
            terms.update(("dor", "somatico"))
        if not terms:
            terms.update(normalized.split())
        return tuple(term for term in terms if term)

    def _load_entries(self) -> tuple[MotorTableEntry, ...]:
        if not self._workbook_path.exists():
            return ()
        rows = self._read_sheet_rows("Tabela Motor")
        if not rows:
            return ()
        header = [self._normalize_header(value) for value in rows[0]]
        entries: list[MotorTableEntry] = []
        for row in rows[1:]:
            data = {
                header[index]: row[index] if index < len(row) else ""
                for index in range(len(header))
            }
            row_id = data.get("id", "").strip()
            entity = data.get("entidade", "").strip()
            if not row_id or not entity:
                continue
            entries.append(
                MotorTableEntry(
                    row_id=row_id,
                    entity=entity,
                    item_type=data.get("tipo", ""),
                    drug_class=data.get("classe", ""),
                    sources=data.get("fontes", data.get("fonte_s", "")),
                    motor_use=data.get("uso_principal_no_motor", ""),
                    symptom_targets=data.get("sintoma_prejuizo_alvo", ""),
                    indication_context=data.get("indicacoes_contexto", ""),
                    dose_range=data.get("dose_faixa_informativa", ""),
                    half_life=data.get("meia_vida", ""),
                    appetite_weight=data.get("apetite_peso", ""),
                    libido=data.get("libido", ""),
                    action_serotonin=data.get("acao_serotonina_0_4", ""),
                    action_dopamine=data.get("acao_dopamina_0_4", ""),
                    action_noradrenaline=data.get("acao_noradrenalina_0_4", ""),
                    action_histamine=data.get("acao_histamina_0_4", ""),
                    cautions=data.get("cautelas_contras", ""),
                    derived_question=data.get("pergunta_derivada", ""),
                    allowed_actions=data.get("acoes_permitidas", ""),
                    do_not_mix_with=data.get("nao_misturar_com", ""),
                    status=data.get("status", ""),
                )
            )
        return tuple(entries)

    def _read_sheet_rows(self, sheet_name: str) -> list[list[str]]:
        with ZipFile(self._workbook_path) as workbook:
            shared_strings = self._shared_strings(workbook)
            sheet_path = self._sheet_path(workbook, sheet_name)
            if not sheet_path:
                return []
            sheet = ET.fromstring(workbook.read(sheet_path))
            rows: list[list[str]] = []
            for row in sheet.findall(".//a:sheetData/a:row", SPREADSHEET_NS):
                values: list[str] = []
                for cell in row.findall("a:c", SPREADSHEET_NS):
                    column_index = self._column_index(cell.attrib.get("r", "A1"))
                    while len(values) < column_index:
                        values.append("")
                    values.append(self._cell_value(cell, shared_strings))
                rows.append(values)
            return rows

    def _shared_strings(self, workbook: ZipFile) -> list[str]:
        if "xl/sharedStrings.xml" not in workbook.namelist():
            return []
        root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
        values: list[str] = []
        for item in root.findall("a:si", SPREADSHEET_NS):
            values.append(
                "".join(text.text or "" for text in item.findall(".//a:t", SPREADSHEET_NS))
            )
        return values

    def _sheet_path(self, workbook: ZipFile, sheet_name: str) -> str:
        workbook_xml = ET.fromstring(workbook.read("xl/workbook.xml"))
        relationships = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
        relationship_targets = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in relationships.findall("rel:Relationship", SPREADSHEET_NS)
        }
        for sheet in workbook_xml.findall(".//a:sheet", SPREADSHEET_NS):
            if sheet.attrib.get("name") != sheet_name:
                continue
            rel_id = sheet.attrib.get(
                "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id",
                "",
            )
            target = relationship_targets.get(rel_id, "")
            if not target:
                return ""
            target = target.lstrip("/")
            return f"xl/{target}" if not target.startswith("xl/") else target
        return ""

    def _cell_value(self, cell: ET.Element, shared_strings: list[str]) -> str:
        value_node = cell.find("a:v", SPREADSHEET_NS)
        if cell.attrib.get("t") == "inlineStr":
            return "".join(
                text.text or "" for text in cell.findall(".//a:t", SPREADSHEET_NS)
            ).strip()
        if value_node is None or value_node.text is None:
            return ""
        raw_value = value_node.text
        if cell.attrib.get("t") == "s":
            return shared_strings[int(raw_value)].strip()
        return raw_value.strip()

    def _column_index(self, cell_reference: str) -> int:
        letters = "".join(character for character in cell_reference if character.isalpha())
        result = 0
        for character in letters:
            result = result * 26 + (ord(character.upper()) - ord("A") + 1)
        return result

    def _normalize_header(self, value: str) -> str:
        return (
            self._normalize(value)
            .replace("s", "s")
            .replace("/", "_")
            .replace("-", "_")
        )

    def _normalize(self, value: str) -> str:
        without_accents = normalize("NFKD", value.lower()).encode("ascii", "ignore")
        normalized = without_accents.decode("ascii")
        keep = []
        for character in normalized:
            if character.isalnum():
                keep.append(character)
            elif character in {" ", "_", "/"}:
                keep.append("_")
        return "_".join("".join(keep).split("_")).strip("_")
