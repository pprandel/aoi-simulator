from heapq import heappush, heappop, nlargest

a = []
for i in range(10):
    heappush(a, i+5)
heappush(a, 2)
print(heappop(a))
print(heappop(a))
print(nlargest(1, a)[0])