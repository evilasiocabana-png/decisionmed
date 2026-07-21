# SSRI Source Inventory RC2

## Status

Raw intake only.

This file continues:

```text
MISSION A02.5-002 - SSRI_SOURCE_CORPUS_INTAKE_CONTINUATION
```

It does not authorize A02.5-003.

## Scope Boundary

This inventory registers source candidates only.

It does not:

- interpret content;
- summarize content;
- normalize metadata;
- classify evidence;
- compare medications;
- map ontology;
- create clinical rules;
- create therapeutic recommendations.

## Raw Source Inventory

| Source ID | Title | Organization/authorship | Year | URL or identifier | Raw document type | Language | Access status | Administrative note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| B001 | Stahl's Essential Psychopharmacology | pending_identification | pending | pending | book | pending_identification | restricted | core_book_item_from_rc1 |
| B002 | Stahl's Prescriber's Guide | pending_identification | pending | pending | book | pending_identification | restricted | core_book_item_from_rc1 |
| B003 | The Maudsley Prescribing Guidelines in Psychiatry | pending_identification | pending | pending | book | pending_identification | restricted | core_book_item_from_rc1 |
| G001 | Practice Guideline for Major Depressive Disorder | APA | pending | pending | clinical_guideline | en | restricted | core_guideline_item_from_rc1_pending_exact_identifier |
| G002 | Canadian Network for Mood and Anxiety Treatments 2023 Update on Clinical Guidelines for Management of Major Depressive Disorder in Adults | CANMAT | 2024 | PMID:38711351; https://pubmed.ncbi.nlm.nih.gov/38711351/ | clinical_guideline | en | accessible | core_guideline_item |
| G003 | Depression in adults: treatment and management | NICE | 2022 | NG222; https://www.nice.org.uk/guidance/ng222 | clinical_guideline | en | accessible | core_guideline_item |
| G004 | Unipolar Depression Guideline | WFSBP | pending | pending | clinical_guideline | en | restricted | core_guideline_item_from_rc1_pending_exact_identifier |
| G005 | Canadian Network for Mood and Anxiety Treatments 2023 Update on Clinical Guidelines for Management of Major Depressive Disorder in Adults | CANMAT | 2024 | PMC11351064; https://pmc.ncbi.nlm.nih.gov/articles/PMC11351064/ | clinical_guideline_full_text_record | en | accessible | duplicate_candidate_of_G002 |
| G006 | Canadian Network for Mood and Anxiety Treatments 2023 Update on Clinical Guidelines for Management of Major Depressive Disorder in Adults | CANMAT | 2023 | https://www.canmat.org/sdm_downloads/canadian-network-for-mood-and-anxiety-treatments-canmat-2023-update-on-clinical-guidelines-for-management-of-major-depressive-disorder-in-adults/ | clinical_guideline_resource_page | en | accessible | duplicate_candidate_or_resource_page_for_G002 |
| G007 | Depression in adults: treatment and management | NICE | 2022 | https://www.nice.org.uk/guidance/ng222/resources/depression-in-adults-treatment-and-management-pdf-66143832307909 | clinical_guideline_pdf | en | accessible | duplicate_candidate_pdf_for_G003 |
| G008 | Depression in adults: treatment and management - Evidence | NICE | 2022 | https://www.nice.org.uk/guidance/ng222/evidence | guideline_evidence_page | en | accessible | supporting_evidence_page_no_extraction |
| R001 | Drug Safety Communications | FDA | pending | https://www.fda.gov/drugs/drug-safety-and-availability/drug-safety-communications | regulatory_safety_index | en | accessible | core_regulatory_item |
| R002 | Clinical investigation of medicinal products in the treatment of depression | EMA | 2025 | https://www.ema.europa.eu/en/clinical-investigation-medicinal-products-treatment-depression-scientific-guideline | regulatory_scientific_guideline | en | accessible | core_regulatory_item |
| R003 | Farmacovigilancia | ANVISA | pending | https://www.gov.br/anvisa/pt-br/assuntos/fiscalizacao-e-monitoramento/farmacovigilancia | regulatory_safety_index | pt-BR | accessible | core_regulatory_item |
| R004 | Guideline on clinical investigation of medicinal products in the treatment of depression - Revision 3 | EMA | 2025 | https://www.ema.europa.eu/en/documents/scientific-guideline/guideline-clinical-investigation-medicinal-products-treatment-depression-revision-3_en.pdf | regulatory_scientific_guideline_pdf | en | accessible | duplicate_candidate_pdf_for_R002 |
| R005 | Draft guideline on clinical investigation of medicinal products in the treatment of depression - Revision 3 | EMA | 2023 | https://www.ema.europa.eu/en/documents/scientific-guideline/draft-guideline-clinical-investigation-medicinal-products-treatment-depression-revision-3_en.pdf | regulatory_draft_guideline_pdf | en | accessible | review_required_draft_document |
| R006 | Antidepressivos - Alertas | ANVISA | pending | https://antigo.anvisa.gov.br/alertas/-/buscar?tagsName=antidepressivos | regulatory_alert_search_page | pt-BR | accessible | review_required_legacy_anvisa_page |
| L001 | Fluoxetine prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=9de65da4-73f8-4c88-8198-c92e63224ddb | official_label | en | accessible | ssri_label |
| L002 | Sertraline prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=fe9e8b7d-61ea-409d-84aa-3ebd79a046b5 | official_label | en | accessible | ssri_label |
| L003 | Paroxetine prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=ef3b5cbe-f9e1-c1ac-79da-cfe14e3a7e7e | official_label | en | accessible | ssri_label |
| L004 | Citalopram prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=26683db8-b319-4d67-8cd8-3c9803daa628 | official_label | en | accessible | ssri_label |
| L005 | Escitalopram prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=3019a647-9bcf-48cf-928c-0467f9b921a8 | official_label | en | accessible | ssri_label |
| L006 | Fluvoxamine prescribing information | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=6eeb14df-6fcf-a737-5359-5744eb4accea | official_label | en | accessible | ssri_label |
| L007 | Vilazodone hydrochloride tablet label | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f917f30d-f2a7-43eb-836f-53eaa2a31cb0 | official_label | en | accessible | review_required_ssri_applicability_not_decided |
| L008 | VIIBRYD vilazodone hydrochloride tablet label | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/lookup.cfm?setid=4c55ccfb-c4cf-11df-851a-0800200c9a66 | official_label | en | accessible | duplicate_candidate_or_brand_label_for_L007 |
| L009 | TRINTELLIX vortioxetine tablet label | DailyMed / FDA label repository | pending | https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=1a5b68e2-14d0-419d-9ec6-1ca97145e838 | official_label | en | accessible | review_required_boundary_ssri_like_serotonin_modulator_no_ontology_decision |

## Declaration Final

RC2 is a raw source intake inventory. It contains no scientific interpretation, no metadata normalization, no evidence classification and no therapeutic recommendation.
