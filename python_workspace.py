d = {0: 13.12, 3: -1.1111, 2: 2.12}

print(d)
d = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
print(d)
