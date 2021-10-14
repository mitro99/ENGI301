import time

start = time.perf_counter()
print(start)
i = 0
while(time.perf_counter() <= start + 1.5):
    i += 1
    print(i)
    time.sleep(0.01)


end = time.perf_counter()
print(end)