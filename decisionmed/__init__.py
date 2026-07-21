"""DecisionMEd platform contracts.

The package contains technology-independent composition primitives. Clinical
knowledge and executable clinical reasoning remain outside this package.
"""

from .specialties import (
    DEFAULT_SPECIALTY_PACKS,
    PSYCHIATRY_PACK,
    DuplicateSpecialtyPackError,
    SpecialtyPack,
    SpecialtyPackRegistry,
    SpecialtyPackStatus,
    UnknownSpecialtyPackError,
    build_default_specialty_registry,
)

__all__ = [
    "DEFAULT_SPECIALTY_PACKS",
    "PSYCHIATRY_PACK",
    "DuplicateSpecialtyPackError",
    "SpecialtyPack",
    "SpecialtyPackRegistry",
    "SpecialtyPackStatus",
    "UnknownSpecialtyPackError",
    "build_default_specialty_registry",
]
