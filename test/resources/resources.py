import pathlib

from app import actioner, model
from test import component


def _load_spec(file_name: str) -> model.Spec:
    file_path = str(pathlib.Path(__file__).parent.joinpath(file_name).absolute())
    parser = actioner.Parser(parsers_map=component.PARSERS_MAP)
    return parser.parse(file_path)


BASIC_SPEC = _load_spec("basic.yml")
