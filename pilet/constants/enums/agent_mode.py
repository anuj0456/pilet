import enum


class AgentModeMeta(enum.EnumMeta):
    def __contains__(cls, item):
        return item in cls.__members__.values()


class AgentMode(str, enum.Enum, metaclass=AgentModeMeta):
    INTERACTIVE = "interactive"
    JOB_COMPLETION = "job_completion"
    COMPLETION = "completion"
