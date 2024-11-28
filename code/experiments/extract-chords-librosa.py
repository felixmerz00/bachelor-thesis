import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Load the MP3 file
filename = '/Users/felixmerz/Documents/Git_Repositories/bachelor-thesis/data/audio/blurred-lines-vs-got-to-give-it-up.mp3'
filename = '/Users/felixmerz/Documents/Git_Repositories/bachelor-thesis/data/audio/extract-chords/Bruno Mars - The Lazy Song.mp3'
y, sr = librosa.load(filename, sr=None)

# Extract harmonic component (to emphasize tonal aspects)
y_harmonic = librosa.effects.harmonic(y)

# Compute the chromagram
chromagram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)

# Plot the chromagram
plt.figure(figsize=(10, 4))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', cmap='coolwarm', sr=sr)
plt.colorbar()
plt.title('Chromagram')
plt.tight_layout()
plt.show()

# Chord estimation using peak analysis (example logic)
def get_chords_from_chromagram(chromagram):
    chord_labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    chords = []
    for frame in chromagram.T:
        # Find the note with the highest energy in each frame
        chord_idx = np.argmax(frame)
        chords.append(chord_labels[chord_idx])
    return chords

# Get a list of estimated chords
chords = get_chords_from_chromagram(chromagram)

# Print the first few chords as an example
print("Detected Chords:", chords[:50])
