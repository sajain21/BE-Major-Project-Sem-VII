import librosa
import soundfile
import pickle
import numpy as np


def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(X))
            result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(
                y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(
                S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(
                X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
    return result


if __name__ == '__main__':
    # filename = "C:/Users/Acer/Downloads/Speech emotion recognition/modelForPrediction1.h5"
    # loading the model file from the storage
    # loaded_model = pickle.load(open(filename, 'rb'))
    loaded_model = pickle.load(open("C:/Users/Acer/Downloads/Speech emotion recognition/modelForPrediction1.h5", 'rb'))
    feature = extract_feature("F:/Projects/ML Based Comprehensive Application To Enhance Soft Skills/Speech Emotion Recognition/speech-emotion-recognition-ravdess-data/Actor_01/03-01-01-01-01-01-01.wav", mfcc=True, chroma=True, mel=True)
    feature = extract_feature("F:/Projects/ML Based Comprehensive Application To Enhance Soft Skills/Speech Emotion Recognition/speech-emotion-recognition-ravdess-data/Actor_02/03-01-01-01-01-02-02.wav", mfcc=True, chroma=True, mel=True)
    feature = feature.reshape(1, -1)
    prediction = loaded_model.predict(feature)
    print(prediction)
