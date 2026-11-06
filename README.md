# Hostel Borrowing Club

A command-line hostel inventory and borrowing system written in Python. Members can browse available items and submit borrowing requests. Staff can approve or reject requests, while the program tracks active loans, due dates, overdue items, and returns.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run

From the project directory, run:

```bash
python hostelborrowing3.py
```

On Windows, you can also use the Python launcher:

```powershell
py -3 hostelborrowing3.py
```

## Features

- View sample inventory and available stock
- Register hostel members
- Submit borrowing requests for staff approval
- Approve or reject pending requests
- Track loans, due dates, and overdue status
- Return items and restore available stock
- View active loans and a member's requests

To borrow an item, first register the member, then submit a request using the item's ID and the member's student ID. Staff approval creates a loan and reduces the available stock. Each item type has its own loan period.

## Classes and Objects

A **class** defines the data and behavior that its objects share. An **object** is a specific instance created from a class while the program runs.

| Class | Purpose |
| --- | --- |
| `BorrowableItem` | Abstract base class defining shared inventory behavior. |
| `LinenItem`, `KitchenItem`, `ApplianceItem`, `CleaningItem`, `StudyItem`, `SportsItem`, `LadderItem` | Item classes that define categories and loan periods. |
| `PressureCooker`, `ElectricKettle`, `Iron` | Specialized item classes that inherit from other item classes. |
| `HostelMember` | Represents a registered member. |
| `BorrowingRequest` | Represents a member's pending, approved, or rejected request. |
| `Loan` | Represents an item borrowed by a member, including its due and return dates. |
| `HostelBorrowingClub` | Manages the inventory, members, requests, and loans. |

Examples of objects created by the application:

- `club` is a `HostelBorrowingClub` object containing the running session's data.
- A sample item such as `BED-001` (Bedsheet) is a `LinenItem` object.
- Registering a student creates a `HostelMember` object.
- Submitting a request creates a `BorrowingRequest` object; staff approval creates a related `Loan` object.

## OOP Concepts

- **Abstraction:** `BorrowableItem` defines a common contract for inventory items.
- **Inheritance and polymorphism:** Item subclasses provide item-specific categories and loan periods.
- **Encapsulation:** Class properties expose member, item, request, and loan data while keeping state management inside the classes.
- **Duck typing:** Inventory display accepts objects that provide a `get_details()` method.

## Data Persistence

Inventory, members, requests, and loans are held in memory. They return to the sample state when the program exits; records are not currently saved to a file or database.
