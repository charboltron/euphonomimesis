import matplotlib.pyplot as plt
import numpy as np


def display_ffts(yfs, num_samples):    
    for yf in yfs:
        T = 1.0 / num_samples
        xf = np.linspace(0.0, 1.0/(2.0*T), num_samples/2)
        # fig, ax = plt.subplots()
        plt.plot(xf, 2.0/num_samples * np.abs(yf[:num_samples//2]))
        # print(2.0/num_samples * np.abs(yf[:num_samples//2]))
    plt.show()

def display_fitness(min_fitnesses, num_fitnesses):
    plt.plot(np.arange(0, num_fitnesses), min_fitnesses)
    plt.show()
