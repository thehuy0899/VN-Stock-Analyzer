from abc import ABC, abstractmethod


class BaseDataSource(ABC):

    @abstractmethod
    def company(self, ticker: str):
        pass

    @abstractmethod
    def financial(self, ticker: str):
        pass

    @abstractmethod
    def business(self, ticker: str):
        pass

    @abstractmethod
    def industry(self, ticker: str):
        pass

    @abstractmethod
    def moat(self, ticker: str):
        pass

    @abstractmethod
    def management(self, ticker: str):
        pass