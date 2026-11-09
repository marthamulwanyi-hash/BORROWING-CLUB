class HostelMember:
    """A member whose personal details are exposed through read-only properties."""

    def __init__(self, student_id: str, name: str) -> None:
        student_id = student_id.strip().upper()
        name = name.strip()
        if not student_id:
            raise ValueError("A student ID is required.")
        if not name:
            raise ValueError("A member name is required.")
        self._student_id = student_id
        self._name = name

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def name(self) -> str:
        return self._name

 