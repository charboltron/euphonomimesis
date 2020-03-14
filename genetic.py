import numpy as np
import math

# probablistically mutate a vector
# assume values in vector normalized to [0, 1]

def mutate(v, prob):
  big = max(v)
  for item in v:
    if np.random.rand() < prob:
      r = np.random.randint(len(v))
      item += (np.random.rand()-0.5)*(item/2)
  np.clip(v, 0, big)
  return v

# take an input matrix and probability,
# mutate each vector in the matrix

def mutate_all(m, prob):
  f = lambda v: mutate(v, prob)
  return np.apply_along_axis(f, 1, m)

# take two vectors and crossover at random point
# return pair of resulting vectors

def crossover(v1, v2):
  r = np.random.randint(1, len(v1)) 
  # print("cross", r)
  a = np.append(v1[:r], v2[r:])
  b = np.append(v2[:r], v1[r:])
  return (a, b) 

# intersperse genes
def crossover2(v1, v2):
  aList = []
  bList = []
  a1 = v1[::2]
  a2 = v1[1::2]
  b1 = v2[::2]
  b2 = v2[1::2]
  for one, two in zip(a1, b2):
      aList.append(one)
      aList.append(two)
  for one, two in zip(b1, a2):
      bList.append(one)
      bList.append(two)
  return (np.array(aList), np.array(bList)) 

def crossover3(v1, v2):
  aList = []
  bList = []
  switch = False
  r = np.random.randint(1, len(v1)) 
  a = np.array_split(v1, r)
  b = np.array_split(v2, r)
  for x, y in zip(a, b):
    if switch:
      aList.append(x)
      bList.append(y)
    else:
      aList.append(y)
      bList.append(x)
    switch = not switch
  return (np.array(aList), np.array(bList)) 

# take a matrix of values and a goal vector
# return normalized euclidean distances between vectors

def fit_all(m, g):
  # print(len(m))
  # print(len(g))

  epsilon = .01
  f = lambda v: np.linalg.norm(v-g)
  v = np.apply_along_axis(f, 1, m)
  
  # for vec in m:  this is what linalg.norm(v-g) does
  #   error = 0.0
  #   for j in range(len(vec)): 
  #     error += pow(vec[j]-g[j], 2)
  #   errors.append(math.sqrt(error))

  for e in v:
    if e <= epsilon:
      print("Goal.")

  # print(f'norm v = {v/sum(v)}, sum of normed = {sum(v/sum(v))}')
  # print(f'v = {v}')

  return v/sum(v)
