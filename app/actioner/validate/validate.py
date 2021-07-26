from typing import List

from app import model


class Validator:
    """Base class for validators"""

    def validate_target(
            self, target: model.Spec, descriptions: List[model.Description]) -> bool:
        raise NotImplementedError()
