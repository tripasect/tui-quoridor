import numpy as np

a = np.array([1, 2, 3], dtype='int64')
print(a)


b = np.array([[1.0, 5.0, 6.0], [1.0, 5.0, 9.0]], dtype='float16')
print(b)

# get dimension
print(a.ndim)
print(b.ndim)


# get shape
print(a.shape)
print(b.shape)
# shape tells you the way the array is in and out


# get type
print(a.dtype)
print(b.dtype)


# get item size (how many bytes per each item)
print(a.itemsize)
print(b.itemsize)


# get size (how many items in total (all times, including the nested ones))
print(a.size)
print(b.size)


# so total size would be
print(a.size * a.itemsize)
print(b.size * b.itemsize)

# or the easier way
print(a.nbytes)
print(b.nbytes)


a = np.array([[0,1,2,3,4,5,6], [7,8,9,10,11,12,13]])
print(a)
print("shape:", a.shape)


# getting an item from your array
print(a[1, 1])


# getting an entire row
print(a[1, :])


# the first component is row and the second is column
# so it's (row, column)


# getting an entire column
print(a[:, 3])


# getting a little more fancy [startindex:endindex:step]
print(a[0, 0:-1:2])
print(a[1, 0:-1:2])


# changing something is as easy as redefining the item
# you can change an entire column or row
# if you define a long list to be a single object, all members of
# that list will be changed to that single object. But,
# if you define a long list to be another long list, they
# must have the same shape AKA the same size or length.
a[1, :] = 156, 156, 156, 156, 156, 156, 156
print(a)


# all zero's matrix
print(np.zeros((5,3,2,3), dtype='int8'))


# all 1's matrix
print(np.ones((3,3,3), dtype='int16'))


# all {something} matrix
print(np.full((2,2), 'a'))


# the identity matrix motherfucker
print(np.identity(12, dtype='int8'))


# repeating an array
print(np.repeat(8, 8))

arr = np.array([[1,2,3]])
print(np.repeat(arr, 10, axis=0))


# making
#  1 1 1 1 1
#  1 0 0 0 1
#  1 0 9 0 1
#  1 0 0 0 1
#  1 1 1 1 1

# starting from all zeros
ex = np.zeros((5, 5), dtype='int8')
ex[0, :] = 1
ex[-1, :] = 1
ex[:, 0] = 1
ex[:, -1] = 1
ex[2, 2] = 9
print(ex)

# starting from all ones
ex = np.ones((5, 5), dtype='int8')
ex[1:-1, 1:-1] = 0
ex[2,2] = 9
print(ex)

# construct the inside and then put it in
ex = np.ones((5,5), dtype='int8')
z = np.zeros((3,3), dtype='int8')
z[1, 1] = 9
ex[1:-1, 1:-1] = z
print(ex)


# matrix multiplication
a = np.ones((2, 3))
b = np.full((3, 2), 3)
print(np.matmul(a, b))


# getting determinant
c = np.identity(3)
print(np.linalg.det(c))


# statistics
stats = np.array([[1, 2, 3], [4, 5, 6]])
print(stats)
print(np.min(stats)) # min
print(np.max(stats)) # max

print(np.min(stats, axis=1))

stats = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print(stats)
print(stats.ndim)
print(np.min(stats, axis=2))
print(np.sum(stats, axis=0))
### I didn't understand how this axis variable really works. I reckon
### when I learned a little bit more about matrices it's gonna be easier.


# reshaping
before = np.array([[1, 2, 3, 4], [0, 0, 0, 0], [5, 6, 7, 8]])
print(before)
print(before.shape)
print(before.reshape((12, 1)))
print(before.reshape((6, 2)))
print(before.reshape((2, 2, 3)))



# vertical stacking
v1 = np.ones((1, 4))
v2 = np.zeros((1, 4))
v = np.vstack([v1, v2])
print(v)

# horizontal stacking
v1 = np.ones((2, 4))
v2 = np.zeros((2, 4))
v = np.hstack([v1, v2])
print(v)


# you can also import data from file and then do all sorts of cool stuff
# with booleans, check qualities of your inputs and make a matrix of
# your booleans. Fun stuff.




