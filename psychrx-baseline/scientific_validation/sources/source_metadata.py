"""Source metadata factory."""

from __future__ import annotations

from scientific_validation.models import ScientificSource


class SourceMetadataFactory:
    """Builds source metadata records."""

    def create(
        self,
        title: str,
        authors: tuple[str, ...] = (),
        organization: str = "",
        publication_year: int = 0,
        revision_date: str = "",
        doi: str = "",
        pmid: str = "",
        isbn: str = "",
        language: str = "",
        country: str = "",
    ) -> ScientificSource:
        return ScientificSource(
            title=title,
            authors=authors,
            organization=organization,
            publication_year=publication_year,
            revision_date=revision_date,
            doi=doi,
            pmid=pmid,
            isbn=isbn,
            language=language,
            country=country,
        )

