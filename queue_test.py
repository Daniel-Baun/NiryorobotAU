import queue

q = queue.Queue()

q.put({"round","red"})
q.put({"s","g"})

r, c = q.get()
print(r,c)
s, c = q.get()
print(s,c)
