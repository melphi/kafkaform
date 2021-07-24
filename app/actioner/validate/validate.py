from app import model


class Validator:
    """Base class for validators"""

    def validate(self, target: model.Spec) -> bool:
        raise NotImplementedError()
