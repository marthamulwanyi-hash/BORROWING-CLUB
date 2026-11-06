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