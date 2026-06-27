from dataclasses import dataclass
from time import perf_counter_ns
from typing import List, Optional, Callable, Tuple


@dataclass
class Transaction:
    """Entity class for one online-shopping transaction."""
    transaction_id: int
    customer_name: str
    product_name: str
    amount: float
    transaction_date: str

    def __str__(self) -> str:
        return (
            f"{self.transaction_id:<8} {self.customer_name:<20} "
            f"{self.product_name:<22} RM {self.amount:<9.2f} "
            f"{self.transaction_date:<12}"
        )


def merge(
    left: List[Transaction],
    right: List[Transaction],
    key: Callable[[Transaction], object],
) -> List[Transaction]:
    """Combine two sorted lists into one sorted list."""
    merged: List[Transaction] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if key(left[left_index]) <= key(right[right_index]):
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def merge_sort(
    transactions: List[Transaction],
    key: Callable[[Transaction], object] = lambda item: item.transaction_id,
    call_counter: Optional[List[int]] = None,
) -> List[Transaction]:
    """
    Recursive Merge Sort.

    Divide: split the list into two halves.
    Conquer: recursively sort each half.
    Combine: merge both sorted halves.
    """
    if call_counter is not None:
        call_counter[0] += 1

    # Base case
    if len(transactions) <= 1:
        return transactions.copy()

    # Divide
    middle = len(transactions) // 2
    left_half = transactions[:middle]
    right_half = transactions[middle:]

    # Conquer
    sorted_left = merge_sort(left_half, key, call_counter)
    sorted_right = merge_sort(right_half, key, call_counter)

    # Combine
    return merge(sorted_left, sorted_right, key)


def binary_search(
    transactions: List[Transaction],
    target_id: int,
    low: int,
    high: int,
) -> Optional[Transaction]:
    """Recursive Binary Search on a list sorted by transaction ID."""
    if low > high:
        return None

    middle = (low + high) // 2
    middle_id = transactions[middle].transaction_id

    if middle_id == target_id:
        return transactions[middle]

    if target_id < middle_id:
        return binary_search(transactions, target_id, low, middle - 1)

    return binary_search(transactions, target_id, middle + 1, high)


def linear_search(
    transactions: List[Transaction],
    target_id: int,
) -> Optional[Transaction]:
    for transaction in transactions:
        if transaction.transaction_id == target_id:
            return transaction
    return None


def create_sample_data() -> List[Transaction]:
    # The records are intentionally unsorted.
    return [
        Transaction(1015, "Alicia Tan", "Wireless Mouse", 79.90, "2026-04-03"),
        Transaction(1003, "Brian Lee", "USB-C Cable", 29.90, "2026-04-04"),
        Transaction(1021, "Carmen Lim", "Mechanical Keyboard", 249.00, "2026-04-05"),
        Transaction(1008, "Daniel Wong", "Laptop Stand", 89.50, "2026-04-07"),
        Transaction(1012, "Emily Goh", "Webcam", 159.00, "2026-04-08"),
        Transaction(1001, "Farid Hassan", "Power Bank", 119.90, "2026-04-09"),
        Transaction(1018, "Grace Ong", "Bluetooth Speaker", 139.00, "2026-04-10"),
        Transaction(1006, "Harith Zain", "Phone Case", 35.00, "2026-04-11"),
        Transaction(1025, "Irene Chew", "Tablet Cover", 69.90, "2026-04-12"),
        Transaction(1010, "Jason Ng", "HDMI Adapter", 45.50, "2026-04-13"),
        Transaction(1004, "Karen Yap", "Gaming Headset", 189.00, "2026-04-14"),
        Transaction(1020, "Leon Chan", "External SSD", 399.00, "2026-04-15"),
        Transaction(1009, "Mei Ling", "Desk Lamp", 99.00, "2026-04-16"),
        Transaction(1016, "Nabil Rahman", "Smart Watch", 299.00, "2026-04-17"),
        Transaction(1002, "Olivia Teh", "Screen Protector", 25.90, "2026-04-18"),
    ]


def print_transactions(
    transactions: List[Transaction],
    title: str = "TRANSACTIONS",
) -> None:
    print(f"\n{title}")
    print("=" * 100)
    print(
        f"{'ID':<8} {'Customer':<20} {'Product':<22} "
        f"{'Amount':<13} {'Date':<12}"
    )
    print("-" * 100)

    if not transactions:
        print("No transactions are available.")
    else:
        for transaction in transactions:
            print(transaction)

    print("=" * 100)


def is_sorted_by_id(transactions: List[Transaction]) -> bool:
    return all(
        transactions[index].transaction_id
        <= transactions[index + 1].transaction_id
        for index in range(len(transactions) - 1)
    )


def run_performance_comparison(transactions: List[Transaction]) -> None:
    repetitions = 10_000
    sorted_transactions = merge_sort(transactions)

    start = perf_counter_ns()
    for _ in range(repetitions):
        merge_sort(transactions)
    merge_time = perf_counter_ns() - start

    test_keys = [1001, 1012, 1025, 9999]

    print("\nPERFORMANCE COMPARISON")
    print(f"Each operation is repeated {repetitions:,} times.")
    print("=" * 92)
    print(f"{'Operation':<35} {'Total Time (ns)':>20} {'Average (ns)':>18} {'Complexity':>15}")
    print("-" * 92)
    print(
        f"{'Merge Sort':<35} {merge_time:>20,} "
        f"{merge_time / repetitions:>18,.2f} {'O(n log n)':>15}"
    )

    for key in test_keys:
        start = perf_counter_ns()
        for _ in range(repetitions):
            binary_search(sorted_transactions, key, 0, len(sorted_transactions) - 1)
        binary_time = perf_counter_ns() - start

        start = perf_counter_ns()
        for _ in range(repetitions):
            linear_search(transactions, key)
        linear_time = perf_counter_ns() - start

        print(
            f"{f'Binary Search for {key}':<35} {binary_time:>20,} "
            f"{binary_time / repetitions:>18,.2f} {'O(log n)':>15}"
        )
        print(
            f"{f'Linear Search for {key}':<35} {linear_time:>20,} "
            f"{linear_time / repetitions:>18,.2f} {'O(n)':>15}"
        )

    print("=" * 92)


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
                print("Amount cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def main() -> None:
    transactions = create_sample_data()

    while True:
        print(
            "\n"
            "================================================\n"
            "    ONLINE TRANSACTION MANAGEMENT SYSTEM\n"
            "================================================\n"
            "1. Display all transactions\n"
            "2. Sort transactions by ID using Merge Sort\n"
            "3. Search transaction using Binary Search\n"
            "4. Search transaction using Linear Search\n"
            "5. Insert a new transaction\n"
            "6. Sort transactions by amount\n"
            "7. Display complexity table\n"
            "8. Run performance comparison\n"
            "0. Exit\n"
            "================================================"
        )

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print_transactions(transactions, "CURRENT TRANSACTIONS")

        elif choice == "2":
            print_transactions(transactions, "BEFORE MERGE SORT")
            counter = [0]
            transactions = merge_sort(transactions, call_counter=counter)
            print_transactions(transactions, "AFTER MERGE SORT BY TRANSACTION ID")
            print(f"Recursive calls made: {counter[0]}")

        elif choice == "3":
            if not is_sorted_by_id(transactions):
                print("The data must be sorted before Binary Search.")
                print("The program will sort it using Merge Sort now.")
                transactions = merge_sort(transactions)

            target_id = read_int("Enter transaction ID to search: ")
            result = binary_search(transactions, target_id, 0, len(transactions) - 1)

            if result:
                print_transactions([result], "BINARY SEARCH RESULT")
            else:
                print("Transaction not found.")

        elif choice == "4":
            target_id = read_int("Enter transaction ID to search: ")
            result = linear_search(transactions, target_id)

            if result:
                print_transactions([result], "LINEAR SEARCH RESULT")
            else:
                print("Transaction not found.")

        elif choice == "5":
            transaction_id = read_int("Transaction ID: ")
            if linear_search(transactions, transaction_id):
                print("A transaction with this ID already exists.")
                continue

            customer_name = input("Customer name: ").strip()
            product_name = input("Product name: ").strip()
            amount = read_float("Amount (RM): ")
            transaction_date = input("Date (YYYY-MM-DD): ").strip()

            transactions.append(
                Transaction(
                    transaction_id,
                    customer_name,
                    product_name,
                    amount,
                    transaction_date,
                )
            )
            print("Transaction inserted successfully.")

        elif choice == "6":
            transactions = merge_sort(transactions, key=lambda item: item.amount)
            print_transactions(transactions, "TRANSACTIONS SORTED BY AMOUNT")

        elif choice == "7":
            print("\nTIME COMPLEXITY TABLE")
            print("=" * 55)
            print(f"{'Algorithm':<22} {'Best':<10} {'Average':<10} {'Worst':<10}")
            print("-" * 55)
            print(f"{'Merge Sort':<22} {'O(n log n)':<10} {'O(n log n)':<10} {'O(n log n)':<10}")
            print(f"{'Binary Search':<22} {'O(1)':<10} {'O(log n)':<10} {'O(log n)':<10}")
            print(f"{'Linear Search':<22} {'O(1)':<10} {'O(n)':<10} {'O(n)':<10}")
            print("=" * 55)

        elif choice == "8":
            run_performance_comparison(transactions)

        elif choice == "0":
            print("Program ended.")
            break

        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
