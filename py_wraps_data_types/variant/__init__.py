from enum import Enum
from .meta import VariantMeta

class Variant(str, Enum, metaclass=VariantMeta):
    """
    A string-based Enum that allows raw strings to pass isinstance() checks.
    """
    def __str__(self):
        return self.value