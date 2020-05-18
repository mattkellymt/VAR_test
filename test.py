import time 

start = time.time()
for i in range(1000000):
    pass
print(time.time() - start)

start = time.time()
for i in range(1000000):
    i % 1000
print(time.time() - start)

start = time.time()
for i in range(1000000):
    time.time()
print(time.time() - start)