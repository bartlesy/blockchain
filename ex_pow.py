from hashlib import sha256

# say PoW is hash of int x * int y must end in 0
# x is given, must find first y st hash(xy)[-1] == 0

x = 5
y = 0

while sha256("%d".encode() % (x * y)).hexdigest()[-1] != "0":
    y += 1

print(y)
