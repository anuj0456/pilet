import enum


class TranslatorModelMeta(enum.EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class TranslatorModel(str, enum.Enum, metaclass=TranslatorModelMeta):
    DEFAULT = "default"
    SEAMLESS_4T = "seamless_4t"
    CUSTOM = "custom"
