import pigpio
import wave
import struct
import time

# Configuration
PWM_PIN = 17  # GPIO pin for PWM output
WAV_FILE = "cat_purr.wav"  # Path to your cat purring WAV file

# Open the WAV file
try:
    wav = wave.open(WAV_FILE, "rb")
except FileNotFoundError:
    print(f"Error: File '{WAV_FILE}' not found.")
    exit()

# Ensure file is mono, 16-bit PCM
channels = wav.getnchannels()
sampwidth = wav.getsampwidth()
framerate = wav.getframerate()
nframes = wav.getnframes()

if channels != 1 or sampwidth != 2:
    print("Error: WAV file must be mono and 16-bit PCM.")
    wav.close()
    exit()

print(f"WAV file info: {channels} channel, {sampwidth * 8}-bit, {framerate} Hz, {nframes} frames.")

# Read all frames and unpack them into signed 16-bit integers
data = wav.readframes(nframes)
wav.close()
samples = struct.unpack("%dh" % nframes, data)


# Function to convert a sample (-32768..32767) to a duty cycle (0..255)
def sample_to_duty(sample):
    # Shift sample to range 0...65535 then scale to 0...255.
    return int((sample + 32768) * 255 / 65535)


# Initialize pigpio and set the PWM pin as output
pi = pigpio.pi()
if not pi.connected:
    print("Error: Could not connect to pigpio daemon.")
    exit()

pi.set_mode(PWM_PIN, pigpio.OUTPUT)

# Optionally, set a PWM frequency (this example uses software PWM frequency).
# Note: The effective frequency when updating via set_PWM_dutycycle will depend on your loop timing.
pi.set_PWM_frequency(PWM_PIN, 8000)  # Adjust frequency as needed

print("Playing cat purr sound via PWM on GPIO 17...")

# Play the audio: loop through each sample and update PWM duty cycle.
# For smoother playback, the WAV file should be at a low sample rate (e.g. 8000 Hz).
sample_interval = 1.0 / framerate

start_time = time.time()
for i, sample in enumerate(samples):
    duty = sample_to_duty(sample)
    pi.set_PWM_dutycycle(PWM_PIN, duty)

    # Sleep for the duration of one sample.
    # Note: time.sleep() may not be very precise at very small intervals.
    time.sleep(sample_interval)

    # Optional: Stop early if needed (for testing)
    # if i > framerate * 5: break  # play only 5 seconds

print("Playback complete.")
pi.set_PWM_dutycycle(PWM_PIN, 0)
pi.stop()

