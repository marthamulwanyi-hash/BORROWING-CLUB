"""Sample hostel inventory used by the borrowing club program.

This file keeps the catalogue of available items in one place and also provides a
simple entry point for running the interactive club system.
"""

from hostelborrowing3 import (
    ApplianceItem,
    CleaningItem,
    ElectricKettle,
    HostelBorrowingClub,
    Iron,
    KitchenItem,
    LadderItem,
    LinenItem,
    PressureCooker,
    SportsItem,
    StudyItem,
    run_club,
)

INVENTORY: tuple[tuple[type, str, str, int], ...] = (
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


def build_sample_club() -> HostelBorrowingClub:
    """Create a club instance populated with the hostel inventory."""
    club = HostelBorrowingClub()
    for item_type, item_id, name, copies in INVENTORY:
        club.add_item(item_type(item_id, name, copies))
    return club


if __name__ == "__main__":
    run_club()
