from app import model
from app.component import component


class SchemaActioner(component.Actioner):
    def apply(self, delta: model.DeltaItem) -> None:
        return None
