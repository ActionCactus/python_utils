from abc import ABC, abstractmethod, abstractclassmethod



class Operation(ABC):
    @abstractclassmethod
    def arg_name() -> str:
        pass

    @property
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def process_file(self, file_path: str):
        pass

    @abstractmethod
    def gather_results(self):
        pass

