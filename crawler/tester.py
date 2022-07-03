import time
from concurrent.futures import ThreadPoolExecutor


def print_sum(num1, num2):
    time.sleep(3)
    print(num1 + num2, time.ctime())


def return_square(n):
    return n ** 2


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        l_results = []
        results = executor.map(return_square, [i for i in range(1,11)])
        l_results.append(results)
        results_2 = executor.map(return_square, [i for i in range(20,31)])
        l_results.append(results_2)
        results_3 = executor.map(return_square, [i for i in range(20,31)])
        l_results.append(results_3)
        for results in l_results:
            for result in results:
                print(result)
        # executor.submit(print_sum, 1, 2)
        # executor.submit(print_sum, 2, 3)
        # executor.submit(print_sum, 3, 4)
    print('done!')


if __name__ == "__main__":
    main()
