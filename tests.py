# import random
#os.urandom

# zeros = []
# for i in range(5):
#     zeros.append('\x00')

# In line list
# zeros = [ '\x00' for i in range(5) ]
# zeros = [ 5*i for i in range(5) ]
# zeros = [ 5*i for i in range(5) if i > 2 ]
# zeros = [ '\x7a' for i in range(5) ]

# print(zeros)
# print(" Hi".join(zeros))
# print(",".join(zeros))
# print("".join(zeros))

# chr / ord
# print(chr(234))
# print(chr(70))
# print(ord('m'))
# print(chr(109))

# random
# print(random.randint(8,24))
# print(random.randint(8,24))
# print(random.randint(8,24))
# print(random.randint(8,24))
# print(random.randint(8,24))

# help(random)

A = [1,2,3,4,5,6]
print(A[:3])
print(A[3:])
print(A[-1:])
print(A[len(A)-1:])
print(A[:-1])
print(A[:len(A)-1])