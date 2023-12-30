from typing import Sequence


class TemplateError(Exception):
    ...


class NotEnoughParametersError(TemplateError):
    def __init__(
        self,
        required_params: Sequence[str],
        received_params: Sequence[str],
        *args,
    ) -> None:
        self.message = {
            "status": "Not enough parameters",
            "required": required_params,
            "received": received_params,
        }

        super().__init__(*args)
