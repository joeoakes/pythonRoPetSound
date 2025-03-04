import pygame

# Initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)  # Max volume (range is 0.0 to 1.0)

# Load sound file
sound = pygame.mixer.Sound("cat_purr.wav")  # Replace with your file

# Play the sound
sound.play()

# Keep the program running while the sound is playing
input("Press Enter to exit...")
