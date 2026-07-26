from datetime import date, timedelta
import unittest

from decisionmed.knowledge import (
    ClinicalComplementaryExam,
    ClinicalContentStatus,
    ClinicalDiscriminator,
    ClinicalEntityType,
    ClinicalModuleContent,
    ClinicalModuleContentRegistry,
    ClinicalModuleDefinition,
    ClinicalModuleRegistry,
    ClinicalModuleStatus,
    KnowledgeError,
)


def module() -> ClinicalModuleDefinition:
    return ClinicalModuleDefinition(
        module_id="module.cardiology.acute-thoracic-syndrome",
        version="0.1.0",
        official_name="Síndrome torácica aguda",
        display_name="Síndrome torácica aguda",
        entity_type=ClinicalEntityType.INITIAL_SYNDROME,
        primary_specialty="cardiology",
        legacy_keys=("cardiovascular_discomfort",),
    )


def content(**overrides: object) -> ClinicalModuleContent:
    values: dict[str, object] = {
        "module_id": "module.cardiology.acute-thoracic-syndrome",
        "version": "0.1.0",
        "definition": None,
        "boundaries": None,
        "anchor_values": ("Peito",),
        "required_manifestations": (),
        "frequent_manifestations": (),
        "atypical_manifestations": (),
        "contrary_findings": (),
        "risk_factors": (),
        "red_flags": (),
        "stop_conditions": (),
        "likely_hypotheses": ("Síndrome coronariana aguda",),
        "cannot_miss_hypotheses": ("Dissecção aguda de aorta",),
        "mimics": ("Dor musculoesquelética",),
        "discriminators": (
            ClinicalDiscriminator(
                question_id="discriminator.cardiovascular.duration",
                text="Quanto dura cada episódio?",
                options=("Segundos", "Minutos"),
            ),
        ),
        "physical_examination": ("Sinais vitais",),
        "complementary_exams": (
            ClinicalComplementaryExam(
                exam_id="exam.cardiology.ecg",
                name="ECG de 12 derivações",
                clinical_question="Há alteração isquêmica ou do ritmo?",
                when="Na avaliação inicial quando clinicamente indicado.",
            ),
        ),
        "diagnostic_criteria": (),
        "post_exam_reassessment": (),
        "safety_conduct": (),
        "initial_treatment": (),
        "definitive_treatment": (),
        "destination_return_followup": (),
        "source_ids": (),
        "content_status": ClinicalContentStatus.PARTIAL,
        "status": ClinicalModuleStatus.DRAFT,
    }
    values.update(overrides)
    return ClinicalModuleContent(**values)


class ClinicalModuleContentRegistryTest(unittest.TestCase):
    def test_partial_content_is_registered_and_execution_stays_blocked(self) -> None:
        modules = ClinicalModuleRegistry((module(),))
        registry = ClinicalModuleContentRegistry(modules, (content(),))

        stored = registry.require("cardiovascular_discomfort")

        self.assertEqual(1, len(stored.discriminators))
        self.assertEqual(1, len(stored.complementary_exams))
        self.assertFalse(stored.clinical_execution_allowed)
        self.assertEqual({"partial": 1}, registry.counts_by_content_status())

    def test_duplicate_or_missing_module_content_fails_closed(self) -> None:
        modules = ClinicalModuleRegistry((module(),))
        with self.assertRaises(KnowledgeError):
            ClinicalModuleContentRegistry(modules, (content(), content()))
        with self.assertRaises(KnowledgeError):
            ClinicalModuleContentRegistry(
                modules,
                (content(module_id="module.cardiology.missing"),),
            )

    def test_complete_content_cannot_omit_required_sections(self) -> None:
        with self.assertRaises(KnowledgeError):
            content(content_status=ClinicalContentStatus.COMPLETE)

    def test_validated_content_requires_review_and_sources(self) -> None:
        with self.assertRaises(KnowledgeError):
            content(status=ClinicalModuleStatus.VALIDATED)

        reviewed_on = date.today() - timedelta(days=1)
        complete = content(
            definition="Definição revisada.",
            boundaries="Limites revisados.",
            red_flags=("Sinal de alarme",),
            stop_conditions=("Interromper fluxo em instabilidade",),
            post_exam_reassessment=("Reavaliar hipótese após resultado",),
            safety_conduct=("Aplicar gate de segurança",),
            destination_return_followup=("Definir destino e retorno",),
            source_ids=("evidence.source",),
            content_status=ClinicalContentStatus.COMPLETE,
            status=ClinicalModuleStatus.VALIDATED,
            reviewed_on=reviewed_on,
            reviewed_by="reviewer.clinical",
            review_due_on=date.today() + timedelta(days=365),
        )
        self.assertEqual(ClinicalModuleStatus.VALIDATED, complete.status)


if __name__ == "__main__":
    unittest.main()
