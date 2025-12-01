import SoapySDR
from SoapySDR import *  # SOAPY_SDR_ constants
import numpy as np
import time

ESPRIT imports 
from scipy.linalg import eigh, eigvals, hankel, pinv, svd
# ESPRIT functions

#   SDR CONFIGURATION

def setup_kraken_sdr(sample_rate=1e6, center_freq=100e6, gain=40):
    sdr = SoapySDR.Device(dict(driver="kraken"))
    chan = 0  # single channel for now
    
    sdr.setSampleRate(SOAPY_SDR_RX, chan, sample_rate)
    sdr.setFrequency(SOAPY_SDR_RX, chan, center_freq)
    sdr.setGain(SOAPY_SDR_RX, chan, gain)

    # Start streaming
    rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [chan])
    sdr.activateStream(rx_stream)
    
    return sdr, rx_stream

#   CONTINUOUS CAPTURE LOOP

def run_realtime_esprit(block_size=4096,
                        sample_rate=1e6,
                        center_freq=100e6,
                        n_sinusoids=3):

    # Setup SDR 
    sdr, stream = setup_kraken_sdr(sample_rate, center_freq)
    
    buff = np.zeros(block_size, np.complex64)
    
    print("🔄 Starting continuous ESPRIT processing…")
    print("Press CTRL+C to stop.\n")

    while True:
        # Read new block of IQ samples
        sr = sdr.readStream(stream, [buff], block_size)
        if sr.ret != block_size:
            print("Warning: Underflow/Overflow")
            continue
        
        # Apply ESPRIT   
        freqs = estimate_frequencies_esprit(
            buff.astype(np.complex128),
            fs=sample_rate,
            n_real_sinusoids=n_sinusoids
        )
        
        if freqs.size == 0:
            print("No frequencies detected.")
        else:
            print(f"Detected: {freqs + center_freq} Hz")

if __name__ == "__main__":
    run_realtime_esprit()

