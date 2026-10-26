
def first_fit(blocks, processes):
    return allocate_memory(blocks, processes, "First Fit")


def best_fit(blocks, processes):
    return allocate_memory(blocks, processes, "Best Fit")


def worst_fit(blocks, processes):
    return allocate_memory(blocks, processes, "Worst Fit")


def allocate_memory(block_sizes, processes, algorithm):
    # Each algorithm gets its own copy of the memory blocks.
    remaining = block_sizes.copy()
    allocations = []
    unallocated = []

    for process_id, process_size in enumerate(processes, start=1):
        chosen = -1

        for i, available in enumerate(remaining):
            if available >= process_size:
                if algorithm == "First Fit":
                    chosen = i
                    break

                elif algorithm == "Best Fit":
                    if chosen == -1 or remaining[i] < remaining[chosen]:
                        chosen = i

                elif algorithm == "Worst Fit":
                    if chosen == -1 or remaining[i] > remaining[chosen]:
                        chosen = i

        if chosen != -1:
            remaining[chosen] -= process_size

            allocations.append({
                "process": f"P{process_id}",
                "size": process_size,
                "block": f"B{chosen + 1}",
                "remaining": remaining[chosen]
            })
        else:
            unallocated.append({
                "process": f"P{process_id}",
                "size": process_size
            })

    return {
        "algorithm": algorithm,
        "allocations": allocations,
        "unallocated": unallocated,
        "remaining": remaining
    }


def display_result(result):
    print("\n" + "=" * 60)
    print(f"{result['algorithm']} ALLOCATION")
    print("=" * 60)

    print(f"{'Process':<12}{'Size':<12}{'Block':<12}{'Block Left':<15}")
    print("-" * 51)

    for item in result["allocations"]:
        print(
            f"{item['process']:<12}"
            f"{item['size']:<12}"
            f"{item['block']:<12}"
            f"{item['remaining']:<15}"
        )

    if result["unallocated"]:
        print("\nUnallocated Processes:")
        for item in result["unallocated"]:
            print(f"{item['process']} (Size: {item['size']})")

    print("\nFinal Free Memory in Each Block:")
    for i, size in enumerate(result["remaining"], start=1):
        print(f"Block B{i}: {size}")

    allocated_count = len(result["allocations"])
    total_processes = allocated_count + len(result["unallocated"])

    print(f"\nProcesses allocated: {allocated_count}/{total_processes}")
    print(f"Processes not allocated: {len(result['unallocated'])}")


def main():
    print("=" * 60)
    print("       MEMORY ALLOCATION SIMULATOR")
    print("=" * 60)

    try:
        n = int(input("\nEnter the number of memory blocks: "))
        if n <= 0:
            print("Error: Enter at least one memory block.")
            return

        blocks = []
        for i in range(n):
            size = int(input(f"Enter size of Block B{i + 1}: "))
            if size <= 0:
                print("Error: Block sizes must be positive.")
                return
            blocks.append(size)

        m = int(input("\nEnter the number of processes: "))
        if m <= 0:
            print("Error: Enter at least one process.")
            return

        processes = []
        for i in range(m):
            size = int(input(f"Enter size of Process P{i + 1}: "))
            if size <= 0:
                print("Error: Process sizes must be positive.")
                return
            processes.append(size)

        print("\nSelect an algorithm:")
        print("1. First Fit")
        print("2. Best Fit")
        print("3. Worst Fit")
        print("4. Compare All Three")

        choice = input("Enter your choice (1-4): ").strip()

        algorithms = {
            "1": ["First Fit"],
            "2": ["Best Fit"],
            "3": ["Worst Fit"],
            "4": ["First Fit", "Best Fit", "Worst Fit"]
        }

        if choice not in algorithms:
            print("Invalid choice. Please run the program again.")
            return

        functions = {
            "First Fit": first_fit,
            "Best Fit": best_fit,
            "Worst Fit": worst_fit
        }

        results = []

        for name in algorithms[choice]:
            result = functions[name](blocks, processes)
            results.append(result)
            display_result(result)

        if len(results) == 3:
            print("\n" + "=" * 60)
            print("       ALGORITHM COMPARISON")
            print("=" * 60)
            print(f"{'Algorithm':<18}{'Allocated':<15}{'Not Allocated':<15}")
            print("-" * 48)

            for result in results:
                print(
                    f"{result['algorithm']:<18}"
                    f"{len(result['allocations']):<15}"
                    f"{len(result['unallocated']):<15}"
                )

        print("\nProgram completed successfully.")

    except ValueError:
        print("\nInvalid input. Please enter whole numbers only.")


if __name__ == "__main__":
    main()
