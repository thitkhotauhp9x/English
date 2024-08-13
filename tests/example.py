import multiprocessing
import threading
import os
import time


def hello_from_thread():
    print(f"Hello from thread {threading.current_thread()}!")


def hello_from_process():
    print(f"Hello from child process {os.getpid()}!")


def main_thread():
    hello_thread = threading.Thread(target=hello_from_thread)
    hello_thread.start()

    total_threads = threading.active_count()
    thread_name = threading.current_thread().name

    print(f"Python is currently running {total_threads} thread(s)")
    print(f"The current thread is {thread_name}")

    hello_thread.join()


def main_process():
    hello_process = multiprocessing.Process(target=hello_from_process)
    hello_process.start()

    print(f"Hello from parent process {os.getpid()}!")
    hello_process.join()


def print_fib(number: int) -> None:

    def fib(n: int) -> int:
        if n == 1:
            return 0
        if n == 2:
            return 1
        return fib(n - 1) + fib(n - 2)

    print(f"fib({number}) is {fib(number)}")


def fibs_no_threading():
    print_fib(40)
    print_fib(40)


def fibs_with_threads():
    fortieth_thread = threading.Thread(target=print_fib, args=(40,))
    forty_first_thread = threading.Thread(target=print_fib, args=(40,))

    fortieth_thread.start()
    forty_first_thread.start()

    fortieth_thread.join()
    forty_first_thread.join()


start = time.time()
fibs_with_threads()
end = time.time()
print(f"Completed in {end - start:.4f} seconds.")

start = time.time()
fibs_no_threading()
end = time.time()
print(f"Completed in {end - start:.4f} seconds.")

# if __name__ == "__main__":
#     print_fib(40)
#     # main_thread()
#     # main_process()
