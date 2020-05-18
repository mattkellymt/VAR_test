from multiprocessing import Pool, cpu_count
import time 
from progress import progress

class Parallel(object):
    def __init__(self, worker, args, message="", chunk_len=1000):
        self.start_time = time.time()
        self.input_len = len(args)
        self.message = message
        self.pool = self.make_pool(worker, args, chunk_len)

    def make_pool(self, worker, args, chunk_len):
        pool = Pool()
        results = pool.imap(worker, args, chunksize=chunk_len)
        return results

    def make_results(self):
        lap_start = time.time()
        
        for i, result in enumerate(self.pool):
            lap_start = progress(i, lap_start, self.input_len, self.start_time, self.message)
            yield result
        progress(i, lap_start, self.input_len, self.start_time, self.message, done=True)

    def __iter__(self):
        self.results = self.make_results()
        return self

    def __next__(self):
        result = next(self.results)
        return result

def f(a):
    return a

if __name__ == "__main__":
    length = 10000000
    args = list(range(length))
    p = Parallel(f, args, "Testing")
    
    start = time.time()
    results = list(p)
    print(time.time() - start)
    debug = True