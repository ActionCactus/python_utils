from operations.operation import Operation

class AspectRatio(Operation):
    def arg_name() -> str:
        return "aspect_ratio"

    @property
    def name(self) -> str:
        return "Filter-AspectRatio"
