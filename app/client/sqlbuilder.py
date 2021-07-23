from jinja2 import sandbox


class Builder:
    """Safe SQL builder"""

    _FORBIDDEN = [";", "--"]

    def __init__(self):
        self._env = sandbox.SandboxedEnvironment(autoescape=True)

    def safe_interpolate(self, sql: str, params: dict) -> str:
        if params:
            for val in params.values():
                for forbidden in self._FORBIDDEN:
                    if forbidden in val:
                        raise ValueError(f"SQL parameter [{val}] can not contain forbidden character [{forbidden}]")
        try:
            template = self._env.from_string(sql)
            return template.render(params)
        except Exception as e:
            raise ValueError(f"Could not format query [{sql}] with parameters [{params}]: {str(e)}")
