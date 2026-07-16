from abc import ABC, abstractmethod

from core.engine_result import EngineResult


class BaseEngine(ABC):
    """
    Base class for all analysis engines.
    """

    @abstractmethod
    def analyze(self, company) -> EngineResult:
        """
        Analyze a company and return standardized result.
        """
        pass