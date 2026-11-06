# Hostel Borrowing Club

A command-line Python program for managing a hostel's shared inventory.
Members can register and request items. Staff can approve or reject requests,
and approved requests become loans with a due date.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run the program

Open a terminal in the project directory and run:

```bash
python hostelborrowing3.py
```

On Windows, you can also use:

```powershell
py -3 hostelborrowing3.py
```

## Use the menu

1. Select **1** to view the inventory and item IDs.
2. Select **2** to register a member with their student ID and name.
3. Select **3** to request an item using its item ID and the registered
   member's student ID.
4. Select **4** to review pending requests. Enter the request ID, then enter
   `a` to approve or `r` to reject. An approved request creates a loan.
5. Select **5** to return a loan using its loan ID.
6. Select **6** to view active loans and any overdue items.
7. Select **7** to view a member's requests using their student ID.
8. Select **0** to exit.

Example:

```text
Choose an option: 2
Student ID: S001
Member name: Alex Student

Choose an option: 3
Item ID: KIT-008
Student ID: S001

Choose an option: 4
Request ID to review (Enter to cancel): R0001
Approve or reject? (a/r): a
```

Use your own student ID and name. The program displays available item IDs,
request IDs, loan IDs, and due dates as you use it.

## Sample inventory

| Category | Item IDs | Items |
|---|---|---|
| Bedding | `BED-001`–`BED-006` | Bedsheet, blanket, pillow, pillowcase, mosquito net, mattress protector |
| Kitchen | `KIT-001`–`KIT-009` | Dinner plate, cup or mug, spoon and fork set, cooking pot, frying pan, electric kettle, serving bowl, 6L and 3L pressure cookers |
| Laundry and appliances | `APP-001`–`APP-005` | Steam iron, extension cable, desk fan, phone charger, power adapter |
| Maintenance | `MNT-001` | Aluminium ladder |
| Cleaning | `CLN-001`–`CLN-006` | Bucket, basin, broom, mop, dustpan and brush, laundry basket |
| Study | `STD-001`–`STD-004` | Scientific calculator, dictionary, study lamp, laptop stand |
| Sports | `SPT-001`–`SPT-005` | Football, volleyball, badminton racket, board game, skipping rope |

Each item category defines its own loan period. Available stock and due dates
are shown by the program.

## Object-oriented programming concepts

- **Classes and objects:** `HostelMember`, `BorrowingRequest`, `Loan`, and
  `HostelBorrowingClub` are classes. Registering a member or creating a loan
  constructs an object (an instance of a class).
- **Abstraction:** `BorrowableItem` is an abstract base class. Its abstract
  `category` and `loan_days` properties define what concrete item classes must
  provide.
- **Encapsulation:** `BorrowableItem` keeps item data in underscore-prefixed
  fields and changes stock through `borrow()` and `return_item()`.
- **Inheritance:** item categories such as `KitchenItem` and `LinenItem`
  inherit shared behavior from `BorrowableItem`. `PressureCooker` and
  `ElectricKettle` inherit from `KitchenItem`.
- **Polymorphism:** `get_details()` uses each item's own category and loan
  period, while the inventory can display different item subclasses through
  the same interface.
- **Duck typing:** `describe_item()` calls `get_details()` on an item. Objects
  that provide this method can be displayed without being a particular class.

## Data storage and limitations

Members, inventory changes, requests, and loans are held in memory. They reset
when the program exits. The program does not save records to a file or
database, and this version does not track item condition. Keep it running
while members submit requests and staff review them.
