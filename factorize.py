from multiprocessing import cpu_count
from timeit import default_timer
import logging
import concurrent.futures


logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    

def factorize_all(number):
    x_list = []
    x = 1
    while x <= number:
        if number % x == 0:
            x_list.append(x)
        x += 1
    print(x_list)


if __name__ == '__main__':
    t1 = default_timer()
    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        results = list(executor.map(factorize_all, (128, 255, 99999, 10651060)))
    delta = default_timer() - t1
    logging.info(f"Process run time {delta}")
    

# a, b, c, d  = factorize(128, 255, 99999, 10651060)

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]