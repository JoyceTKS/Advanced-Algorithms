import random

# Generate a 12-digit Malaysian IC number (1950–2015)
def generate_ic_12():
    full_year = random.randint(1980, 2005)
    year = full_year % 100  # last 2 digits
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    state = random.randint(1, 21)
    serial = random.randint(0, 9999)
    return f"{year:02d}{month:02d}{day:02d}{state:02d}{serial:04d}"

# Extend IC to 16-digit format
def convert_to_16(ic12):
    return ic12 + f"{random.randint(1000, 9999)}"

# Folding hash function
def folding_hash(ic, table_size):
    return sum(int(ic[i:i+4]) for i in range(0, len(ic), 4)) % table_size

# Insert ICs into hash table with separate chaining
def simulate_insertion(ic_list, table_size):
    table = [[] for _ in range(table_size)]
    collisions = 0
    for ic in ic_list:
        index = folding_hash(ic, table_size)
        if table[index]:
            collisions += 1
        table[index].append(ic)
    return table, collisions

# Print first 11 + last 4 slots of the hash table
def print_table(table):
    for i in range(11):
        if table[i]:
            print(f"table[{i}] --> {' --> '.join(table[i])}")
        else:
            print(f"table[{i}]")
    print("...")
    for i in range(len(table) - 4, len(table)):
        if table[i]:
            print(f"table[{i}] --> {' --> '.join(table[i])}")
        else:
            print(f"table[{i}]")

# Run simulation for either 12 or 16 digit ICs
def run_simulation(ic_length):
    print(f"\n===== Running Simulation for IC Length: {ic_length} digits =====\n")
    rounds = 10
    size1, size2 = 1009, 2003
    coll_1009, coll_2003 = [], []

    for round_num in range(1, rounds + 1):
        ic_list = [generate_ic_12() for _ in range(1000)]
        if ic_length == 16:
            ic_list = [convert_to_16(ic) for ic in ic_list]

        table1, c1 = simulate_insertion(ic_list, size1)
        table2, c2 = simulate_insertion(ic_list, size2)

        # Print tables only in round 1
        if round_num == 1:
            print(f"Hash Table with size {size1}:")
            print_table(table1)
            print(f"\nHash Table with size {size2}:")
            print_table(table2)
            print()

        print(f"Round {round_num}:")
        print(f"  Hash Table Size {size1} → Collisions: {c1}")
        print(f"  Hash Table Size {size2} → Collisions: {c2}")

        coll_1009.append(c1)
        coll_2003.append(c2)

    # Calculate average
    avg1 = sum(coll_1009) / rounds
    avg2 = sum(coll_2003) / rounds

    print(f"\n----- Average Collisions for IC Length {ic_length} -----")
    print(f"  Hash Table Size {size1} → Average Collisions: {avg1:.2f}")
    print(f"  Hash Table Size {size2} → Average Collisions: {avg2:.2f}")
    print("=" * 57)

# Run simulations for both lengths
run_simulation(12)
run_simulation(16)
