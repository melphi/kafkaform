import pathlib

from app.parse import spec, parse


def _load_spec(file_name: str) -> spec.Spec:
    file_path = str(pathlib.Path(__file__).parent.joinpath(file_name).absolute())
    parser = parse.Parser()
    return parser.parse(file_path)


BASIC_SPEC = _load_spec("basic.yml")
