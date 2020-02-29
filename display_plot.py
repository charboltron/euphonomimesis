import matplotlib.pyplot as plt
import numpy as np


def display_fft(yf, num_samples):    
    
    T = 1.0 / num_samples
    xf = np.linspace(0.0, 1.0/(2.0*T), num_samples/2)
    fig, ax = plt.subplots()
    ax.plot(xf, 2.0/num_samples * np.abs(yf[:num_samples//2]))
    print(2.0/num_samples * np.abs(yf[:num_samples//2]))
    plt.show()