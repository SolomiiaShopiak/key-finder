import librosa
import numpy as np
import scipy.linalg


class KeyFinder():
    PITCH_MAP = {0: 'C', 1: 'C#', 2: 'D', 3: 'D#', 4: 'E', 5: 'F',
                 6: 'F#', 7: 'G', 8: 'G#', 9: 'A', 10: 'A#', 11: 'B'}

    def __init__(self, file):

        # template major and minor profiles as described here:
        # https://www.researchgate.net/publication/226939732_A_Theory_of_Tonal_Hierarchies_in_Music
        major_profile = np.asarray([6.35, 2.23, 3.48, 2.33, 4.38, 
                            4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        minor_profile = np.asarray([6.33, 2.68, 3.52, 5.38, 2.60,
                            3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

        y, sr = librosa.load(path=file, sr=None)
        y_harmonic, _ = librosa.effects.hpss(y)
        chromogram = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr, bins_per_octave=24)
        
        #pitch class distribution
        pcd = chromogram.sum(axis=1)
        
        #subtracting the mean
        pcd -= np.mean(pcd)
        major_profile -= np.mean(major_profile)
        minor_profile -= np.mean(minor_profile)
        
        #taking l2 norms
        pcd_norm = scipy.linalg.norm(pcd)
        maj_norm = scipy.linalg.norm(major_profile)
        min_norm = scipy.linalg.norm(minor_profile)
        
        #taking cirulant matrix to create all 12 rotations of major and minor profiles
        major_profile = scipy.linalg.circulant(major_profile).T
        minor_profile = scipy.linalg.circulant(minor_profile).T
        
        #calculating Pearson correlation coefficients for major and minor profiles
        self.maj_corr_coeffs = major_profile.dot(pcd) / (pcd_norm * maj_norm)
        self.min_corr_coeffs = minor_profile.dot(pcd) / (pcd_norm * min_norm)

    
    # prints estimated key 
    def key(self) -> None:
        maj_min_coeffs = np.concatenate((self.maj_corr_coeffs, self.min_corr_coeffs))
        i = np.argmax(maj_min_coeffs)
        print(f'\nMost likely: {self.PITCH_MAP[i % 12]} {"major" if i < 12 else "minor"}')
        alt_i = np.argsort(maj_min_coeffs)[-2]
        print(f'Also possible: {self.PITCH_MAP[alt_i % 12]} {"major" if alt_i < 12 else "minor"}')


    # prints the correlation coefficients associated with each major and minor key
    def corr_table(self) -> None:
        print('\nMajor key coefficients:')
        for i, coeff in enumerate(self.maj_corr_coeffs):
            print(f'{self.PITCH_MAP[i]}: {coeff:.2f}')

        print('\nMinor key coefficients:')
        for i, coeff in enumerate(self.min_corr_coeffs):
            print(f'{self.PITCH_MAP[i]}: {coeff:.2f}')


def main():
    file = input('Enter path to the audio file: ')
    
    song = KeyFinder(file)
    song.corr_table()
    song.key()

if __name__ == '__main__':
    main()
