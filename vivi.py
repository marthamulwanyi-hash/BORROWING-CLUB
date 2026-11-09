class BorrowingRequest:
    """A member's request to borrow an item, awaiting staff approval."""

    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"

    def __init__(
        self,
        request_id: str,
        member: HostelMember,
        item: BorrowableItem,
    ) -> None:
        self._request_id = request_id
        self._member = member
        self._item = item
        self._status = self.PENDING
        self._loan: Loan | None = None

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def member(self) -> HostelMember:
        return self._member

    @property
    def item(self) -> BorrowableItem:
        return self._item

    @property
    def status(self) -> str:
        return self._status

    @property
    def loan(self) -> Loan | None:
        return self._loan

    def approve(self, loan: Loan) -> None:
        if self._status != self.PENDING:
            raise BorrowingError(f"Request {self.request_id} is no longer pending.")
        self._loan = loan
        self._status = self.APPROVED

    def reject(self) -> None:
        if self._status != self.PENDING:
            raise BorrowingError(f"Request {self.request_id} is no longer pending.")
        self._status = self.REJECTED