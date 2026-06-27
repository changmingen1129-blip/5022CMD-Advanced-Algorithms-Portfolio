from dataclasses import dataclass
from time import perf_counter_ns
from typing import Optional, List, Any


@dataclass
class Medicine:
    """Entity class used to represent one pharmacy product."""
    product_id: int
    name: str
    category: str
    price: float
    quantity: int

    def __str__(self) -> str:
        return (
            f"{self.product_id:<10} {self.name:<24} {self.category:<15} "
            f"RM {self.price:<8.2f} {self.quantity:<8}"
        )


class HashTable:
    """Hash table that resolves collisions using linear probing."""

    _DELETED = object()

    def __init__(self, size: int = 31) -> None:
        if size <= 0:
            raise ValueError("Hash table size must be positive.")
        # Bucket structure: a one-dimensional Python list.
        self.size = size
        self.table: List[Any] = [None] * size
        self.count = 0

    def _hash(self, product_id: int) -> int:
        return product_id % self.size

    def insert(self, medicine: Medicine) -> bool:
        """Insert a medicine. Returns False when the key already exists or table is full."""
        if self.count >= self.size:
            return False

        start_index = self._hash(medicine.product_id)
        first_deleted_index: Optional[int] = None

        for step in range(self.size):
            index = (start_index + step) % self.size
            bucket = self.table[index]

            if bucket is None:
                target = first_deleted_index if first_deleted_index is not None else index
                self.table[target] = medicine
                self.count += 1
                return True

            if bucket is self._DELETED:
                if first_deleted_index is None:
                    first_deleted_index = index
                continue

            if bucket.product_id == medicine.product_id:
                return False

        if first_deleted_index is not None:
            self.table[first_deleted_index] = medicine
            self.count += 1
            return True

        return False

    def search(self, product_id: int) -> Optional[Medicine]:
        """Search by product ID using the same linear-probing sequence."""
        start_index = self._hash(product_id)

        for step in range(self.size):
            index = (start_index + step) % self.size
            bucket = self.table[index]

            if bucket is None:
                return None

            if bucket is self._DELETED:
                continue

            if bucket.product_id == product_id:
                return bucket

        return None

    def update(
        self,
        product_id: int,
        name: str,
        category: str,
        price: float,
        quantity: int,
    ) -> bool:
        medicine = self.search(product_id)
        if medicine is None:
            return False

        medicine.name = name
        medicine.category = category
        medicine.price = price
        medicine.quantity = quantity
        return True

    def delete(self, product_id: int) -> bool:
        start_index = self._hash(product_id)

        for step in range(self.size):
            index = (start_index + step) % self.size
            bucket = self.table[index]

            if bucket is None:
                return False

            if bucket is self._DELETED:
                continue

            if bucket.product_id == product_id:
                self.table[index] = self._DELETED
                self.count -= 1
                return True

        return False

    def get_all(self) -> List[Medicine]:
        return [
            item
            for item in self.table
            if item is not None and item is not self._DELETED
        ]

    def display_bucket_positions(self) -> None:
        print("\nHASH TABLE BUCKETS")
        print("-" * 72)
        for index, item in enumerate(self.table):
            if item is None:
                value = "EMPTY"
            elif item is self._DELETED:
                value = "DELETED"
            else:
                value = f"{item.product_id} - {item.name}"
            print(f"Bucket {index:02d}: {value}")


def create_sample_data() -> List[Medicine]:
    # Some IDs differ by 31, so they intentionally produce collisions.
    return [
        Medicine(1001, "Panadol", "Tablet", 8.50, 50),
        Medicine(1032, "Cough Relief", "Syrup", 12.90, 20),
        Medicine(1063, "Vitamin C", "Supplement", 25.00, 30),
        Medicine(1004, "Ibuprofen", "Tablet", 10.50, 45),
        Medicine(1005, "Antacid", "Tablet", 7.80, 35),
        Medicine(1006, "Allergy Relief", "Tablet", 14.20, 25),
        Medicine(1007, "Multivitamin", "Supplement", 28.90, 18),
        Medicine(1008, "Children Cough Syrup", "Syrup", 15.50, 22),
        Medicine(1009, "ORS Sachet", "Supplement", 6.00, 60),
        Medicine(1010, "Pain Relief Gel", "Topical", 18.80, 16),
        Medicine(1011, "Calcium Tablet", "Supplement", 21.90, 28),
        Medicine(1012, "Fever Patch", "Patch", 9.90, 40),
        Medicine(1013, "Throat Lozenges", "Lozenge", 11.50, 32),
        Medicine(1014, "Saline Spray", "Spray", 13.20, 24),
        Medicine(1015, "Probiotic Capsule", "Supplement", 31.00, 15),
    ]


def linear_search(items: List[Medicine], product_id: int) -> Optional[Medicine]:
    for medicine in items:
        if medicine.product_id == product_id:
            return medicine
    return None


def print_products(products: List[Medicine]) -> None:
    print("\nPHARMACY PRODUCTS")
    print("=" * 80)
    print(f"{'ID':<10} {'Name':<24} {'Category':<15} {'Price':<11} {'Quantity':<8}")
    print("-" * 80)
    if not products:
        print("No products are available.")
    else:
        for item in sorted(products, key=lambda x: x.product_id):
            print(item)
    print("=" * 80)


def run_performance_test(hash_table: HashTable, items: List[Medicine]) -> None:
    search_keys = [1001, 1008, 1015, 1032, 9999, 8888]
    repetitions = 10_000

    print("\nSEARCH PERFORMANCE COMPARISON")
    print(f"Each key is searched {repetitions:,} times.")
    print("=" * 82)
    print(
        f"{'Key':<10} {'Status':<14} {'Hash Table (ns)':>18} "
        f"{'List Search (ns)':>18} {'Faster':>12}"
    )
    print("-" * 82)

    total_hash = 0
    total_list = 0

    for key in search_keys:
        status = "Existing" if hash_table.search(key) else "Not Existing"

        start = perf_counter_ns()
        for _ in range(repetitions):
            hash_table.search(key)
        hash_time = perf_counter_ns() - start

        start = perf_counter_ns()
        for _ in range(repetitions):
            linear_search(items, key)
        list_time = perf_counter_ns() - start

        total_hash += hash_time
        total_list += list_time
        faster = "Hash Table" if hash_time < list_time else "List"

        print(
            f"{key:<10} {status:<14} {hash_time:>18,} "
            f"{list_time:>18,} {faster:>12}"
        )

    print("-" * 82)
    print(
        f"{'Average':<25} {total_hash // len(search_keys):>18,} "
        f"{total_list // len(search_keys):>18,}"
    )
    print("=" * 82)


def read_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


def read_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    medicines = create_sample_data()
    hash_table = HashTable(size=31)

    for medicine in medicines:
        hash_table.insert(medicine)

    while True:
        print(
            "\n"
            "============================================\n"
            "       PHARMACY INVENTORY SYSTEM\n"
            "============================================\n"
            "1. Display all products\n"
            "2. Insert a new product\n"
            "3. Search for a product\n"
            "4. Edit a product\n"
            "5. Delete a product\n"
            "6. Display hash-table bucket positions\n"
            "7. Run search performance comparison\n"
            "0. Exit\n"
            "============================================"
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print_products(hash_table.get_all())

        elif choice == "2":
            product_id = read_int("Product ID: ")
            if hash_table.search(product_id):
                print("A product with this ID already exists.")
                continue

            name = input("Product name: ").strip()
            category = input("Category: ").strip()
            price = read_float("Price (RM): ")
            quantity = read_int("Quantity: ")

            if quantity < 0:
                print("Quantity cannot be negative.")
                continue

            new_medicine = Medicine(product_id, name, category, price, quantity)

            if hash_table.insert(new_medicine):
                medicines.append(new_medicine)
                print("Product inserted successfully.")
            else:
                print("The product could not be inserted.")

        elif choice == "3":
            product_id = read_int("Enter product ID to search: ")
            result = hash_table.search(product_id)
            if result:
                print_products([result])
            else:
                print("Product not found.")

        elif choice == "4":
            product_id = read_int("Enter product ID to edit: ")
            current = hash_table.search(product_id)
            if current is None:
                print("Product not found.")
                continue

            name = input(f"New name [{current.name}]: ").strip() or current.name
            category = input(f"New category [{current.category}]: ").strip() or current.category

            price_text = input(f"New price [{current.price:.2f}]: ").strip()
            quantity_text = input(f"New quantity [{current.quantity}]: ").strip()

            try:
                price = float(price_text) if price_text else current.price
                quantity = int(quantity_text) if quantity_text else current.quantity
                if price < 0 or quantity < 0:
                    raise ValueError
            except ValueError:
                print("Invalid price or quantity.")
                continue

            hash_table.update(product_id, name, category, price, quantity)
            print("Product updated successfully.")

        elif choice == "5":
            product_id = read_int("Enter product ID to delete: ")
            target = hash_table.search(product_id)
            if hash_table.delete(product_id):
                medicines[:] = [m for m in medicines if m.product_id != product_id]
                print(f"{target.name} was deleted.")
            else:
                print("Product not found.")

        elif choice == "6":
            hash_table.display_bucket_positions()

        elif choice == "7":
            run_performance_test(hash_table, medicines)

        elif choice == "0":
            print("Program ended.")
            break

        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
