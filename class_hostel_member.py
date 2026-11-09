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

 # OBJECTS: each Loan instance connects one particular member and item.

class Loan:
    """Connects a hostel member, an item, and their borrowing dates."""

    def __init__(
        self,
        loan_id: str,
        member: HostelMember,
        item: BorrowableItem,
        borrowed_on: date,
    ) -> None:
        self._loan_id = loan_id
        self._member = member
        self._item = item
        self._borrowed_on = borrowed_on
        self._due_on = borrowed_on + timedelta(days=item.loan_days)
        self._returned_on: date | None = None

    @property
    def loan_id(self) -> str:
        return self._loan_id

    @property
    def member(self) -> HostelMember:
        return self._member

    @property
    def item(self) -> BorrowableItem:
        return self._item

    @property
    def borrowed_on(self) -> date:
        return self._borrowed_on

    @property
    def due_on(self) -> date:
        return self._due_on

    @property
    def returned_on(self) -> date | None:
        return self._returned_on

    @property
    def is_active(self) -> bool:
        return self._returned_on is None

    @property
    def is_overdue(self) -> bool:
        return self.is_active and date.today() > self.due_on

    def mark_returned(self, returned_on: date) -> None:
        if not self.is_active:
            raise BorrowingError(f"Loan {self.loan_id} has already been returned.")
        if returned_on < self.borrowed_on:
            raise BorrowingError("A return date cannot be before the borrowing date.")
        self._item.return_item()
        self._returned_on = returned_on