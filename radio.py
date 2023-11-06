from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import sawtooth
import numpy as np
from time import sleep
import gpiozero as gpio

sample_rate, data = wavfile.read("test_audio.wav") # Parse the file
duration = data.shape[0] / sample_rate # The duration in seconds

carrier_frequency = 1E8 # The total carrier frequency for the transmitter. This will be 100MHz.


time = np.arange(duration * sample_rate)
carrier = np.sin(2 * np.pi * carrier_frequency * time)

highest_signal_frequency = np.abs(fft(data)).argmax() # The highest frequency in the signal

intg = np.cumsum(data)
beta = 0.7 # The modulation index
freq_dev = beta * highest_signal_frequency

y = np.cos(2*np.pi*carrier_frequency*time + 2*np.pi*freq_dev*intg)
saw = sawtooth(2 * np.pi * carrier_frequency * time)

pwm_time = np.arange(data.shape[0]) / carrier_frequency

pwm = np.zeros(data.shape[0])
pwm[y > saw] = 1
pwm[y < saw] = 0

device = gpio.output_devices.OutputDevice(17)

while True:
    for i in range(data.shape[0]):
        if pwm[i] == 1 and not device.active_high:
            device.on()
        elif pwm[i] == 0 and device.active_high:
            device.off()
        sleep(1 / carrier_frequency)
    # Switch to another audio file here, implement this later.