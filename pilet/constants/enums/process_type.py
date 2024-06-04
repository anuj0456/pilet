from enum import Enum


class ProcessType(str, Enum):
    sequential = "sequential"
    hierarchical = "hierarchical"
