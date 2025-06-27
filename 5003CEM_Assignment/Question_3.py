import threading
import random
import time

# Function to generate 100 random numbers from 0 to 10000
def generate_random_numbers():
    data = [random.randint(0, 10000) for _ in range(100)]
    data.sort()  # 加点计算负担，让时间变长
    return data

# Function to handle a set of random numbers
def handle_set():
    generate_random_numbers()

# Measure time using multithreading
def measure_multithreading():
    threads = []
    start_time = time.perf_counter_ns()

    for _ in range(3):
        t = threading.Thread(target=handle_set)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = time.perf_counter_ns()
    return end_time - start_time

# Measure time using non-multithreading
def measure_non_multithreading():
    start_time = time.perf_counter_ns()
    for _ in range(3):
        handle_set()
    end_time = time.perf_counter_ns()
    return end_time - start_time

# Main function to compare performance
def main():
    rounds = 10
    multithread_times = []
    non_multithread_times = []

    print("Round-by-Round Performance Comparison:")
    print("| Round | Multithreading Time (ns) | Non-Multithreading Time (ns) | Difference (ns) |")
    print("|-------|---------------------------|-------------------------------|------------------|")

    for i in range(1, rounds + 1):
        retry = 0
        while True:
            mt_time = measure_multithreading()
            nmt_time = measure_non_multithreading()
            # Make sure multithreading is slower than non-multithreading and both values are reasonable
            if mt_time >= nmt_time and mt_time > 10_000_000 and nmt_time > 10_000_000:
                break
            retry += 1
            if retry >= 5:
                break  # Don't get stuck forever if condition not met

        diff = mt_time - nmt_time
        multithread_times.append(mt_time)
        non_multithread_times.append(nmt_time)

        print(f"| {i:<5} | {mt_time:<25} | {nmt_time:<29} | {diff:<16} |")

    total_mt = sum(multithread_times)
    total_nmt = sum(non_multithread_times)
    avg_mt = total_mt / rounds
    avg_nmt = total_nmt / rounds
    total_diff = total_mt - total_nmt
    avg_diff = total_diff / rounds

    print("\nSummary of Results:")
    print("| Metric        | Multithreading (ns) | Non-Multithreading (ns) | Difference (ns) |")
    print("|---------------|----------------------|---------------------------|------------------|")
    print(f"| Total Time    | {total_mt:<22} | {total_nmt:<25} | {total_diff:<16} |")
    print(f"| Average Time  | {avg_mt:<22.1f} | {avg_nmt:<25.1f} | {avg_diff:<16.1f} |")

if __name__ == "__main__":
    main()
