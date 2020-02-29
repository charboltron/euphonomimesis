import numpy as np
import math

# probablistically mutate a vector
# assume values in vector normalized to [0, 1]

def mutate(v, prob):
  if np.random.rand() < prob:
    r = np.random.randint(len(v))
    v[r] = np.random.rand()
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
  a = np.append(v1[:r], v2[r:])
  b = np.append(v1[r:], v2[:r])
  return (a, b) 

# take a matrix of values and a goal vector
# return normalized euclidean distances between vectors

def fit_all(m, g):
  f = lambda v: np.linalg.norm(v-g)
  v = np.apply_along_axis(f, 1, m)
  return v / math.sqrt(len(g))
