from datetime import date, timedelta

from hostelborrowing3 import SupportsDetails

# Note: Ensure BorrowableItem, HostelMember, SupportsDetails, 
# and BorrowingError are imported or defined in your module.


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


class HostelBorrowingClub:
    """Manages inventory, hostel members, requests, and item loans."""

    def __init__(self) -> None:
        self._items: dict[str, BorrowableItem] = {}
        self._members: dict[str, HostelMember] = {}
        self._loans: dict[str, Loan] = {}
        self._requests: dict[str, BorrowingRequest] = {}
        self._next_loan_number = 1
        self._next_request_number = 1

    @property
    def items(self) -> tuple[BorrowableItem, ...]:
        return tuple(self._items.values())

    @property
    def members(self) -> tuple[HostelMember, ...]:
        return tuple(self._members.values())

    @property
    def loans(self) -> tuple[Loan, ...]:
        return tuple(self._loans.values())

    @property
    def requests(self) -> tuple[BorrowingRequest, ...]:
        return tuple(self._requests.values())

    def add_item(self, item: BorrowableItem) -> None:
        if item.item_id in self._items:
            raise BorrowingError(f"Item ID {item.item_id} already exists.")
        self._items[item.item_id] = item

    def register_member(self, student_id: str, name: str) -> HostelMember:
        member = HostelMember(student_id, name)
        if member.student_id in self._members:
            raise BorrowingError(
                f"Student ID {member.student_id} is already registered."
            )
        self._members[member.student_id] = member
        return member

    def list_items(self, category: str | None = None) -> tuple[BorrowableItem, ...]:
        items = self.items
        if category is None:
            return items
        requested_category = category.strip().casefold()
        return tuple(
            item for item in items if item.category.casefold() == requested_category
        )

    def request_item(self, item_id: str, student_id: str) -> BorrowingRequest:
        normalized_item_id = item_id.strip().upper()
        normalized_student_id = student_id.strip().upper()
        try:
            item = self._items[normalized_item_id]
        except KeyError as error:
            raise BorrowingError(f"Item {normalized_item_id} was not found.") from error
        try:
            member = self._members[normalized_student_id]
        except KeyError as error:
            raise BorrowingError(
                f"Student {normalized_student_id} is not registered."
            ) from error

        if item.available_copies == 0:
            raise BorrowingError(
                f"No copies of {item.name} are currently available."
            )

        for request in self._requests.values():
            if (
                request.member.student_id == member.student_id
                and request.item.item_id == item.item_id
                and request.status == BorrowingRequest.PENDING
            ):
                raise BorrowingError(
                    f"You already have a pending request for {item.name}."
                )

        request_id = f"R{self._next_request_number:04}"
        request = BorrowingRequest(request_id, member, item)
        self._requests[request_id] = request
        self._next_request_number += 1
        return request

    def pending_requests(self) -> tuple[BorrowingRequest, ...]:
        return tuple(
            request
            for request in self.requests
            if request.status == BorrowingRequest.PENDING
        )

    def decide_request(
        self, request_id: str, approved: bool, borrowed_on: date | None = None
    ) -> BorrowingRequest:
        normalized_request_id = request_id.strip().upper()
        try:
            request = self._requests[normalized_request_id]
        except KeyError as error:
            raise BorrowingError(
                f"Request {normalized_request_id} was not found."
            ) from error

        if request.status != BorrowingRequest.PENDING:
            raise BorrowingError(
                f"Request {request.request_id} has already been decided."
            )

        if approved:
            loan = self.borrow_item(
                request.item.item_id, request.member.student_id, borrowed_on
            )
            request.approve(loan)
        else:
            request.reject()
        return request

    def borrow_item(
        self, item_id: str, student_id: str, borrowed_on: date | None = None
    ) -> Loan:
        normalized_item_id = item_id.strip().upper()
        normalized_student_id = student_id.strip().upper()
        try:
            item = self._items[normalized_item_id]
        except KeyError as error:
            raise BorrowingError(f"Item {normalized_item_id} was not found.") from error
        try:
            member = self._members[normalized_student_id]
        except KeyError as error:
            raise BorrowingError(
                f"Student {normalized_student_id} is not registered."
            ) from error

        item.borrow()
        loan_number = self._next_loan_number
        loan = Loan(
            f"L{loan_number:04}",
            member,
            item,
            borrowed_on if borrowed_on is not None else date.today(),
        )
        self._loans[loan.loan_id] = loan
        self._next_loan_number += 1
        return loan

    def return_item(
        self, loan_id: str, returned_on: date | None = None
    ) -> Loan:
        normalized_loan_id = loan_id.strip().upper()
        try:
            loan = self._loans[normalized_loan_id]
        except KeyError as error:
            raise BorrowingError(f"Loan {normalized_loan_id} was not found.") from error

        loan.mark_returned(returned_on if returned_on is not None else date.today())
        return loan

    def active_loans(self) -> tuple[Loan, ...]:
        return tuple(loan for loan in self.loans if loan.is_active)


def describe_item(item: SupportsDetails) -> str:
    """Duck typing: any object with get_details() can be displayed."""
    return item.get_details()