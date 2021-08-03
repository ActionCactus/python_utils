from abc import ABC, abstractmethod, abstractclassmethod



class Operation(ABC):
    @abstractclassmethod
    def arg_name() -> str:
        pass

    @property
    @abstractmethod
    def name() -> str:
        pass

