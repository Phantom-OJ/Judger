import multiprocessing
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import random
import time

def worker(x, y, z):
    sleepTime=random.randint(0,5)
    print("本次测评需要%d秒结束"%(sleepTime))
    time.sleep(sleepTime)
    pass # Do whatever here

def collectMyResult(result):
    print("Got result {}".format(result))

def abortable_worker(func, *args, **kwargs):
    timeout = kwargs.get('timeout', None)
    print("timeout:",timeout)
    p = ThreadPool(1)
    res = p.apply_async(func, args=args)
    try:
        out = res.get(timeout)  # Wait timeout seconds for func to complete.
        return out
    except multiprocessing.TimeoutError:
        print("Aborting due to timeout")
        raise

if __name__ == "__main__":
    pool = multiprocessing.Pool(4)
    featureClass = [[100,k,1] for k in range(0,100,1)] #list of arguments
    for f in featureClass:
      abortable_func = partial(abortable_worker, worker, timeout=3)
      pool.apply_async(abortable_func, args=f,callback=collectMyResult)
    pool.close()
    pool.join()