import numpy as np
from functools import partial

t1 = np.array([[0.,0.,0.,0.,0.,0.,0.,0.,0.,0.],[1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]])
t2 = np.random.rand(2, 10)

# probablistically mutate a vector in place
# assume values in vector normalized to [0, 1]

def mutate(prob, v):
  if np.random.rand() < prob:
    r = np.random.randint(len(v))
    v[r] = np.random.rand()
    return v

# take an input matrix and probability,
# mutate each vector in the matrix

def mutateAll(m, prob):
  return np.apply_along_axis(partial(mutate, prob), 1, m)

# take two vectors and crossover at random point
# return pair of resulting vectors

def crossover(v1, v2):
  r = np.random.randint(1, len(v1)) 
  a = np.append(v1[:r], v2[r:])
  b = np.append(v1[r:], v2[:r])
  return (a, b) 

# take a vector of values and a goal vector
# return euclidean distance between vectors

def fitness(v, g):
  return np.linalg.norm(v-g)

print(t1)
print(mutateAll(t1, 1.))
