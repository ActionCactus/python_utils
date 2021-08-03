from typing import List, Dict
from photo_tagger.operations.operation import Operation
from photo_tagger.operations.aspect_ratio import AspectRatio

operations = [AspectRatio]

class OperationFactory:
    def __init__(self) -> None:
        self._arg_map = self._gather_arg_map()

    def gather_operations(self, parsed_args: dict) -> List[Operation]:
        retval = {}
        for arg_name, arg_value in parsed_args.items():
            if arg_name in self._arg_map:
                print(arg_name)
            if arg_value == True and arg_name in self._arg_map and not arg_name in retval:
                retval[arg_name] = self._arg_map[arg_name]()

        return retval.values()

    def _gather_arg_map(self) -> Dict[str, str]:
        retval = {}
        for op in operations:
            retval[op.arg_name()] = op

        return retval

