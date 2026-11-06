"""Hostel borrowing club demonstrating core object-oriented programming.

The sample inventory and member records are held in memory while the program
runs. See the classes below for abstraction, encapsulation, inheritance,
polymorphism, and duck typing in the borrowing workflow.
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import Protocol


class SupportsDetails(Protocol):
    def get_details(self) -> str:
        ...
# A class defines an object type. For example, HostelMember is a class and
# HostelMember("S001", "Alex") creates a member object from that class.

class BorrowingError(Exception):
    """Raised when an item or member cannot complete a borrowing operation."""


class BorrowableItem(ABC):
    """Abstract base class for items that hostel members may borrow."""

    def __init__(self, item_id: str, name: str, total_copies: int) -> None:
        item_id = item_id.strip().upper()
        name = name.strip()
        if not item_id:
            raise ValueError("An item ID is required.")
        if not name:
            raise ValueError("An item name is required.")
        if type(total_copies) is not int or total_copies < 1:
            raise ValueError("Total copies must be a positive whole number.")

        self._item_id = item_id
        self._name = name
        self._total_copies = total_copies
        self._available_copies = total_copies

    @property
    def item_id(self) -> str:
        return self._item_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def total_copies(self) -> int:
        return self._total_copies

    @property
    def available_copies(self) -> int:
        return self._available_copies

    @property
    def borrowed_copies(self) -> int:
        return self._total_copies - self._available_copies

    @property
    @abstractmethod
    def category(self) -> str:
        """Return the item's inventory category."""

    @property
    @abstractmethod
    def loan_days(self) -> int:
        """Return the maximum number of days this item may be borrowed."""

    def borrow(self) -> None:
        if self._available_copies == 0:
            raise BorrowingError(f"No copies of {self.name} are available.")
        self._available_copies -= 1

    def return_item(self) -> None:
        if self._available_copies == self._total_copies:
            raise BorrowingError(f"No borrowed copy of {self.name} needs returning.")
        self._available_copies += 1

    def get_details(self) -> str:
        """Describe this item; subclasses supply category and loan period."""
        loan_length = "day" if self.loan_days == 1 else "days"
        return (
            f"{self.item_id:<8} {self.name:<25} {self.category:<12} "
            f"{self.available_copies}/{self.total_copies} available "
            f"(loan: {self.loan_days} {loan_length})"
        )

# INHERITANCE: each item category is a more specific kind of BorrowableItem.
# Subclasses reuse its common ID, stock, condition, borrow, and return logic.
class LinenItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Bedding"

    @property
    def loan_days(self) -> int:
        return 7


class KitchenItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Kitchen"

    @property
    def loan_days(self) -> int:
        return 2


class PressureCooker(KitchenItem):
    @property
    def loan_days(self) -> int:
        return 1


class ElectricKettle(KitchenItem):
    @property
    def loan_days(self) -> int:
        return 1


class ApplianceItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Appliance"

    @property
    def loan_days(self) -> int:
        return 3


class Iron(ApplianceItem):
    @property
    def category(self) -> str:
        return "Laundry"


class LadderItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Maintenance"

    @property
    def loan_days(self) -> int:
        return 1


class CleaningItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Cleaning"

    @property
    def loan_days(self) -> int:
        return 1


class StudyItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Study"

    @property
    def loan_days(self) -> int:
        return 7


class SportsItem(BorrowableItem):
    @property
    def category(self) -> str:
        return "Sports"

    @property
    def loan_days(self) -> int:
        return 2


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

 # OBJECTS: each request instance tracks one member's request for one item.

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


def build_sample_club() -> HostelBorrowingClub:
    """Create the club and its sample hostel inventory."""
    
 # POLYMORPHISM: this one collection contains objects from different
    # subclasses. The loop constructs item objects and the rest of the system
    # uses their shared BorrowableItem interface.
    
    club = HostelBorrowingClub()
    inventory: tuple[tuple[type[BorrowableItem], str, str, int], ...] = (
        (LinenItem, "BED-001", "Bedsheet", 20),
        (LinenItem, "BED-002", "Blanket", 15),
        (LinenItem, "BED-003", "Pillow", 20),
        (LinenItem, "BED-004", "Pillowcase", 20),
        (LinenItem, "BED-005", "Mosquito net", 12),
        (LinenItem, "BED-006", "Mattress protector", 10),
        (KitchenItem, "KIT-001", "Dinner plate", 30),
        (KitchenItem, "KIT-002", "Cup or mug", 30),
        (KitchenItem, "KIT-003", "Spoon and fork set", 25),
        (KitchenItem, "KIT-004", "Cooking pot", 10),
        (KitchenItem, "KIT-005", "Frying pan", 8),
        (ElectricKettle, "KIT-006", "Electric kettle", 10),
        (KitchenItem, "KIT-007", "Serving bowl", 10),
        (PressureCooker, "KIT-008", "Pressure cooker (6L)", 5),
        (PressureCooker, "KIT-009", "Pressure cooker (3L)", 5),
        (Iron, "APP-001", "Steam iron", 8),
        (ApplianceItem, "APP-002", "Extension cable", 12),
        (ApplianceItem, "APP-003", "Desk fan", 10),
        (ApplianceItem, "APP-004", "Phone charger", 15),
        (ApplianceItem, "APP-005", "Power adapter", 12),
        (LadderItem, "MNT-001", "Aluminium ladder", 2),
        (CleaningItem, "CLN-001", "Bucket", 15),
        (CleaningItem, "CLN-002", "Basin", 15),
        (CleaningItem, "CLN-003", "Broom", 10),
        (CleaningItem, "CLN-004", "Mop", 8),
        (CleaningItem, "CLN-005", "Dustpan and brush", 8),
        (CleaningItem, "CLN-006", "Laundry basket", 8),
        (StudyItem, "STD-001", "Scientific calculator", 10),
        (StudyItem, "STD-002", "Dictionary", 6),
        (StudyItem, "STD-003", "Study lamp", 10),
        (StudyItem, "STD-004", "Laptop stand", 8),
        (SportsItem, "SPT-001", "Football", 6),
        (SportsItem, "SPT-002", "Volleyball", 6),
        (SportsItem, "SPT-003", "Badminton racket", 8),
        (SportsItem, "SPT-004", "Board game", 5),
        (SportsItem, "SPT-005", "Skipping rope", 10),
    )
    for item_type, item_id, name, copies in inventory:
        club.add_item(item_type(item_id, name, copies))
    return club


def show_inventory(club: HostelBorrowingClub) -> None:
    print("\nID       ITEM                      CATEGORY     STOCK")
    print("-" * 75)
    for item in club.list_items():
        print(describe_item(item))


def show_active_loans(club: HostelBorrowingClub) -> None:
    loans = club.active_loans()
    if not loans:
        print("\nThere are no active loans.")
        return

    print("\nACTIVE LOANS")
    print("-" * 75)
    for loan in loans:
        overdue_label = " OVERDUE" if loan.is_overdue else ""
        print(
            f"{loan.loan_id} | {loan.item.name} | {loan.member.name} "
            f"({loan.member.student_id}) | due {loan.due_on}{overdue_label}"
        )


def show_member_requests(club: HostelBorrowingClub, student_id: str) -> None:
    normalized_student_id = student_id.strip().upper()
    requests = tuple(
        request
        for request in club.requests
        if request.member.student_id == normalized_student_id
    )
    if not requests:
        print("\nYou have no borrowing requests.")
        return

    print("\nYOUR BORROWING REQUESTS")
    print("-" * 75)
    for request in requests:
        loan_status = (
            f" | Loan {request.loan.loan_id}, due {request.loan.due_on}"
            if request.loan is not None
            else ""
        )
        print(
            f"{request.request_id} | {request.item.name} | "
            f"{request.status}{loan_status}"
        )


def review_pending_requests(club: HostelBorrowingClub) -> None:
    pending = club.pending_requests()
    if not pending:
        print("\nThere are no pending requests.")
        return

    print("\nPENDING BORROWING REQUESTS")
    print("-" * 75)
    for request in pending:
        print(
            f"{request.request_id} | {request.item.name} "
            f"({request.item.available_copies} available) | "
            f"{request.member.name} ({request.member.student_id})"
        )

    request_id = input("Request ID to review (Enter to cancel): ").strip()
    if not request_id:
        return
    decision = input("Approve or reject? (a/r): ").strip().casefold()
    if decision not in ("a", "approve", "r", "reject"):
        print("Enter 'a' to approve or 'r' to reject.")
        return

    request = club.decide_request(
        request_id, approved=decision in ("a", "approve")
    )
    if request.status == BorrowingRequest.APPROVED:
        loan = request.loan
        if loan is None:
            raise BorrowingError(f"Approved request {request.request_id} is missing its loan.")
        print(
            f"Approved {request.request_id}. Loan {loan.loan_id} "
            f"created; return by {loan.due_on}."
        )
    else:
        print(f"Rejected request {request.request_id}.")


def run_club() -> None:
    """Run the interactive hostel borrowing club menu."""
    club = build_sample_club()
    print("Welcome to the Hostel Borrowing Club!")

    while True:
        print(
            "\n1. View all borrowable items"
            "\n2. Register a member"
            "\n3. Request to borrow an item"
            "\n4. Review requests (staff)"
            "\n5. Return a borrowed item"
            "\n6. View active loans"
            "\n7. View a member's requests"
            "\n0. Exit"
        )
        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                show_inventory(club)
            elif choice == "2":
                member = club.register_member(
                    input("Student ID: "), input("Member name: ")
                )
                print(f"Registered {member.name} ({member.student_id}).")
            elif choice == "3":
                request = club.request_item(
                    input("Item ID: "), input("Student ID: ")
                )
                print(
                    f"Request {request.request_id} submitted for {request.item.name}. "
                    "Wait for staff approval before taking the item."
                )
            elif choice == "4":
                review_pending_requests(club)
            elif choice == "5":
                loan = club.return_item(input("Loan ID: "))
                print(f"Returned {loan.item.name}. Thank you, {loan.member.name}!")
            elif choice == "6":
                show_active_loans(club)
            elif choice == "7":
                show_member_requests(club, input("Student ID: "))
            elif choice == "0":
                print("Thank you for using the Hostel Borrowing Club.")
                break
            else:
                print("Choose one of the listed options.")
        except (BorrowingError, ValueError) as error:
            print(f"Unable to complete that action: {error}")


if __name__ == "__main__":
    run_club()
