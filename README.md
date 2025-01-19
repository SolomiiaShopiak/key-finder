# Musical key finder
A python project that analyses the key of a song using one of the template-based key finding algorithms - the Krumhansl and Schmuckler algorithm.
### Short outline of the algorithm:
- obtain the pitch class distribution of a piece of music you want to analyse;
- compute the Pearson correlation coefficient of X and Y, where X - pitch class distribution and Y - pre-definded by Krumhansl major and minor profiles; correlation coefficient is computed for each possible major and minor key by pairing the pitch class values to the profile values for the key in question;
- the estimated key then is the key with the highest correlation coefficient.

*Pitch class distribution is basically a distribution of 12 pitch classes (C, C♯, D, D♯, E, F, F♯, G, G♯, A, A♯, B) in a piece of music; or else how much notes from each pitch class are present in that piece.

**[Detailed description of the algorithm](http://rnhart.net/articles/key-finding/).

***[Where do the profiles come from? (see 3.3)](https://www.researchgate.net/publication/226939732_A_Theory_of_Tonal_Hierarchies_in_Music).

### Dependencies
```
librosa
numpy
scipy
```

### Usage
Run in the command line:
```
python3 keyfinder.py
Enter path to the audio file: your/path/here
```
Python iterpreter:
```python3
import keyfinder
song = keyfinder.KeyFinder("your/path/here")
song.corr_table()
song.key()
```

### Examples

#### [1. The Swan by Camille Saint-Saëns](https://youtu.be/_Oxcs1izoDc?si=HP_D8ps-uD7x2caA)
We will analyse "The Swan", the 13th movement of The Carnival of the Animals by Camille Saint-Saëns.
```python3
swan = keyfinder.KeyFinder("The-Carnival-of-the-Animals-The-Swan.mp3")
```
We can get all 24 correlation coefficients using function corr_table().
```python3
swan.corr_table()
```
```
Major key coefficients:
C: 0.58
C#: -0.67
D: 0.43
D#: -0.32
E: 0.08
F: 0.03
F#: -0.38
G: 0.90
G#: -0.47
A: -0.03
A#: -0.24
B: 0.09

Minor key coefficients:
C: 0.20
C#: -0.35
D: 0.06
D#: -0.47
E: 0.68
F: -0.33
F#: -0.17
G: 0.23
G#: -0.10
A: 0.27
A#: -0.67
B: 0.65
```
Or we can get the estimated key (and the second most likely key) right away using key() function.
```python3
swan.key()
```
```
Most likely: G major
Also possible: E minor
```
The program has shown that the key of "The Swan" is G major, which is indeed known to be [the key of this piece](https://www.hooktheory.com/theorytab/view/camille-saint-saens/carnival-of-the-animals---the-swan).
#### [2. Indian Summer by The Doors](https://youtu.be/klrKliyfHKs?si=8hJZkIQf7heBFAYn)
Next we will analyse "Indian Summer" by The Doors.
```python3
indian_summer = keyfinder.KeyFinder("Indian-Summer.mp3")
indian_summer.corr_table()
indian_summer.key()
```
```
Major key coefficients:
C: -0.13
C#: -0.35
D: 0.80
D#: -0.12
E: -0.21
F: 0.03
F#: -0.20
G: 0.23
G#: -0.42
A: 0.50
A#: 0.19
B: -0.32

Minor key coefficients:
C: -0.26
C#: -0.19
D: 0.68
D#: -0.01
E: -0.13
F: -0.52
F#: 0.39
G: 0.30
G#: -0.47
A: 0.15
A#: -0.21
B: 0.26

Most likely: D major
Also possible: D minor
```
We can see that the key estimated by the program is [correct](https://tunebat.com/Info/Indian-Summer-The-Doors/2hdeaGl9nT3UoQIgSqctHj).
