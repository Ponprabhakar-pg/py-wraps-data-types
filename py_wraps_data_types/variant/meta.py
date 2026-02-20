from enum import EnumMeta

class VariantMeta(EnumMeta):
    def __instancecheck__(cls, instance):
        if isinstance(instance, str):
            return instance in cls._value2member_map_
        return super().__instancecheck__(instance)