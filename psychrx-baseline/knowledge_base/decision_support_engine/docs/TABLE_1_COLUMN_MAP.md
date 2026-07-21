# Table 1 Column Map

Source: `Psicologia e Psiquiatria 9.pdf`, page 1, visual header supplied by the founder.

This document defines the normalized column names for the first antidepressant
indication matrix. It is a working transcription scaffold. Values must still be
filled from visual review of the source table.

## Header Mapping

| Visual header | Normalized column |
| --- | --- |
| Medicamento | `medicamento` |
| Dose anotada na linha | `dose_referencia_linha` |
| TAG | `TAG` |
| Panico | `panico` |
| T. de estresse | `transtorno_de_estresse` |
| Fobias | `fobias` |
| Fobia social | `fobia_social` |
| TOC | `TOC` |
| Depressao melancolica | `depressao_melancolica` |
| Depressao ansiosa | `depressao_ansiosa` |
| Depressao com agitacao/agressiva | `depressao_com_agitacao_agressiva` |
| Depressao atipica | `depressao_atipica` |
| Dor | `dor` |
| Vicios | `vicios` |
| Tabagismo | `tabagismo` |
| Compulsao | `compulsao` |
| Bulimia, anorexia | `bulimia_anorexia` |
| TDPM | `TDPM` |
| Ideacao suicida | `ideacao_suicida` |

## Rule

The matrix should be used to derive:

```text
clinical target
-> medication candidates
-> missing safety questions
-> decision-support explanation
```

It must not be treated as a standalone prescribing rule.

## Row Labels Transcribed

| Medicamento | Dose de referencia visivel na linha |
| --- | --- |
| Venlafaxina |  |
| Desvenlafaxina | 50-100 |
| Duloxetina | 60-120 |
| Amitriptilina |  |
| Nortriptilina |  |
| Clomipramina |  |
| Imipramina |  |
| Doxepina |  |
| Dosulepina |  |
| Mirtazapina |  |
| Trazodona |  |
| Mianserina |  |
| Maprotilina |  |
| Fluoxetina |  |
| Citalopram | 20-40 |
| Escitalopram | 10-20 |
| Sertralina |  |
| Fluvoxamina |  |
| Paroxetina |  |
| Vortioxetina |  |
| Agomelatina |  |
| Vilazodona |  |
| Bupropiona | 150-300 |
