import threading
from time import perf_counter_ns
from typing import Dict, List, Tuple


NUMBERS = (50, 100, 200)
ROUNDS = 10


def factorial(number: int) -> int:
    """
    Calculate n! using an iterative loop.

    Under the primitive-operation model, the loop repeats in proportion to n,
    so the time complexity is O(n). The function uses O(1) extra variables,
    although the resulting Python integer itself grows as n increases.
    """
    if number < 0:
        raise ValueError("Factorial is not defined for negative numbers.")

    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def factorial_worker(number: int, results: Dict[int, int]) -> None:
    """Thread target: calculate one factorial and store the result."""
    results[number] = factorial(number)


def run_threaded_round() -> Tuple[int, Dict[int, int]]:
    results: Dict[int, int] = {}
    threads = [
        threading.Thread(
            target=factorial_worker,
            args=(number, results),
            name=f"Factorial-{number}",
        )
        for number in NUMBERS
    ]

    # Start timing before the first thread starts.
    start_time = perf_counter_ns()

    for thread in threads:
        thread.start()

    # join() waits until every thread has completed.
    for thread in threads:
        thread.join()

    # This end time is taken after the last thread has finished.
    end_time = perf_counter_ns()

    return end_time - start_time, results


def run_sequential_round() -> Tuple[int, Dict[int, int]]:
    results: Dict[int, int] = {}

    start_time = perf_counter_ns()

    for number in NUMBERS:
        results[number] = factorial(number)

    end_time = perf_counter_ns()

    return end_time - start_time, results


def run_experiment() -> None:
    threaded_times: List[int] = []
    sequential_times: List[int] = []
    threaded_results: Dict[int, int] = {}
    sequential_results: Dict[int, int] = {}

    print("=" * 72)
    print("MULTITHREADED FACTORIAL EXPERIMENT")
    print("=" * 72)

    for round_number in range(1, ROUNDS + 1):
        elapsed_time, threaded_results = run_threaded_round()
        threaded_times.append(elapsed_time)
        print(f"Round {round_number:>2}: {elapsed_time:>12,} ns")

    threaded_average = sum(threaded_times) / len(threaded_times)

    print("-" * 72)
    print(f"Total threaded time : {sum(threaded_times):,.0f} ns")
    print(f"Average threaded time: {threaded_average:,.2f} ns")

    print("\n" + "=" * 72)
    print("SEQUENTIAL FACTORIAL EXPERIMENT")
    print("=" * 72)

    for round_number in range(1, ROUNDS + 1):
        elapsed_time, sequential_results = run_sequential_round()
        sequential_times.append(elapsed_time)
        print(f"Round {round_number:>2}: {elapsed_time:>12,} ns")

    sequential_average = sum(sequential_times) / len(sequential_times)

    print("-" * 72)
    print(f"Total sequential time : {sum(sequential_times):,.0f} ns")
    print(f"Average sequential time: {sequential_average:,.2f} ns")

    print("\n" + "=" * 72)
    print("FACTORIAL RESULT CHECK")
    print("=" * 72)

    for number in NUMBERS:
        threaded_value = threaded_results[number]
        sequential_value = sequential_results[number]
        same = threaded_value == sequential_value
        print(
            f"{number:>3}! contains {len(str(threaded_value)):>3} digits "
            f"| Threaded and sequential results match: {same}"
        )

    print("\n" + "=" * 72)
    print("FINAL COMPARISON")
    print("=" * 72)

    difference = threaded_average - sequential_average

    print(f"Average multithreaded time: {threaded_average:,.2f} ns")
    print(f"Average sequential time   : {sequential_average:,.2f} ns")
    print(f"Difference                : {difference:,.2f} ns")

    if threaded_average < sequential_average:
        print("Result: Multithreading was faster in this run.")
    elif threaded_average > sequential_average:
        print("Result: Sequential processing was faster in this run.")
    else:
        print("Result: Both methods recorded the same average time.")

    print(
        "\nNote: Factorial calculation is CPU-bound. In standard CPython, "
        "the Global Interpreter Lock normally prevents Python threads from "
        "executing CPU-bound Python bytecode in true parallel. Thread creation, "
        "scheduling, and joining also add overhead. Multithreading is usually "
        "more useful for I/O-bound work such as downloading files or waiting "
        "for network and database responses."
    )


def main() -> None:
    run_experiment()


if __name__ == "__main__":
    main()
