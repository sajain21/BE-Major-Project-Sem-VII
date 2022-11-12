# 1. Convert audio to sentences
# 2. Iterate over sentences and see if it contains any bad word. SENTENCE-AUDIO-CHUNK filename in milliseconds
# 3. For the audio chunk referring to that sentence, further break the audio word-wise. WORD-AUDIO-CHUNKS filename named in milliseconds

# from_mp3
# from_flv
# from_ogg
# from_wav
# from_raw

import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
# for word recognition with timestamp
from vosk import Model, KaldiRecognizer
import wave
import json
import math
from uuid import uuid4
import requests
import shutil

SWEAR_WORDS_LIST = ['fuck', 'dick', 'asshole', 'bitch', 'bastard', 'cunt', 'piss', 'boob', 'pussy']

BASE_FETCHED_AUDIO_FOLDER = "fetched-audio"

BASE_SWEAR_CHUNKS_FOLDER = "vosk-swear-audio-chunks"

BASE_VOSK_CHUNKS_FOLDER = "vosk-audio-chunks"

GENERAL_FOLDER = "general"

BASE_PROCESSED_AUDIO_FOLDER = "processed-audio"


def get_vosk_audio_transcription_only(model, uuid, filename, extsn):

    full_text = ""

    VOSK_CHUNKS_FOLDER = uuid + BASE_VOSK_CHUNKS_FOLDER

    sound = AudioSegment.from_file(filename +"."+ extsn, extsn)

    if extsn != "wav":
        sound.export(filename+".wav", format="wav")


    chunks = split_on_silence(sound,
        # minimum silence length to be used for split
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 500ms in the beginning and the end to prevent sounding like it is abruptly cut off
        keep_silence=500,
    )


    if not os.path.isdir(VOSK_CHUNKS_FOLDER):
        os.mkdir(VOSK_CHUNKS_FOLDER)

    text_w_timeline = {}

    print("===> Translating Chunks")

    # on opening the whole audio file it doesn't work properly
    for i, audio_chunk in enumerate(chunks, start=1):

        chunk_i = "chunk"+str(i)

        text_w_timeline[chunk_i]=[]

        chunk_path = os.path.join(VOSK_CHUNKS_FOLDER, f"chunk{i}.wav")

        audio_chunk.export(chunk_path, format="wav")

        with wave.open(chunk_path, 'rb') as wf:  

            rec = KaldiRecognizer(model, wf.getframerate())

            rec.SetWords(True)

            rec.SetPartialWords(True)

            rec.SetMaxAlternatives(1)

            while True:
                data = wf.readframes(int(math.ceil(audio_chunk.duration_seconds)) * 1000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())['alternatives'][0]
                    
                    # Number of "Result" depends on "SetMaxAlternatives"
                    text_w_timeline.update(dict(chunk_i=text_w_timeline[chunk_i].append(result)))

            finalresult = json.loads(rec.FinalResult())['alternatives'][0]
            text_w_timeline.update(dict(chunk_i=text_w_timeline[chunk_i].append(finalresult)))

    print("===> FINAL :- LOOP text_w_timeline['chunk\{i\}']")
    print(text_w_timeline)

    # prepare a list of chunks with timeline for swear words in each chunk
    chunk_swear_words = {}

    if not chunk_swear_words:
        print("===> dict is empty")



    for k, chunk_timeline_array in text_w_timeline.items():
        if chunk_timeline_array != None:
            for obj in chunk_timeline_array:
                # print("obj =>", obj)
                full_text = full_text + obj['text']

    os.remove(VOSK_CHUNKS_FOLDER)

    return full_text


# USAGE :- This function is used for beeping the audio
def get_vosk_audio_transcription(model, uuid, filename, extsn):

    # print("os.path.dirname(os.path.realpath(__file__))", os.path.dirname(os.path.realpath(__file__)))

    # print("__file__", __file__)


    SWEAR_CHUNKS_FOLDER = uuid + "-" + BASE_SWEAR_CHUNKS_FOLDER

    VOSK_CHUNKS_FOLDER = uuid + "-" + BASE_VOSK_CHUNKS_FOLDER

    PROCESSED_AUDIO_FOLDER = uuid + "-" + BASE_PROCESSED_AUDIO_FOLDER

    FETCHED_AUDIO_FOLDER = uuid + "-" + BASE_FETCHED_AUDIO_FOLDER

    full_text = ""

    sound = AudioSegment.from_file(FETCHED_AUDIO_FOLDER + "/" + filename +"."+ extsn, extsn)

    if extsn != "wav":
        sound.export(FETCHED_AUDIO_FOLDER + "/" + filename+".wav", format="wav")


    # Loading english-indian model. This can be varied according to the user's country

    chunks = split_on_silence(sound,
        # minimum silence length to be used for split
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 500ms in the beginning and the end to prevent sounding like it is abruptly cut off
        keep_silence=500,
    )


    if not os.path.isdir(VOSK_CHUNKS_FOLDER):
        os.mkdir(VOSK_CHUNKS_FOLDER)

    text_w_timeline = {}

    print("===> Translating Chunks")

    # on opening the whole audio file it doesn't work properly
    for i, audio_chunk in enumerate(chunks, start=1):

        chunk_i = "chunk"+str(i)

        text_w_timeline[chunk_i]=[]

        chunk_path = os.path.join(VOSK_CHUNKS_FOLDER, f"chunk{i}.wav")

        audio_chunk.export(chunk_path, format="wav")

        with wave.open(chunk_path, 'rb') as wf:  

            rec = KaldiRecognizer(model, wf.getframerate())

            rec.SetWords(True)

            rec.SetPartialWords(True)

            rec.SetMaxAlternatives(1)

            while True:
                data = wf.readframes(int(math.ceil(audio_chunk.duration_seconds)) * 1000)
                if len(data) == 0:
                    break
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())['alternatives'][0]
                    
                    # Number of "Result" depends on "SetMaxAlternatives"
                    text_w_timeline.update(dict(chunk_i=text_w_timeline[chunk_i].append(result)))

            finalresult = json.loads(rec.FinalResult())['alternatives'][0]
            text_w_timeline.update(dict(chunk_i=text_w_timeline[chunk_i].append(finalresult)))


    print("===> FINAL :- LOOP text_w_timeline['chunk\{i\}']")
    print(text_w_timeline)

    # prepare a list of chunks with timeline for swear words in each chunk
    chunk_swear_words = {}

    for k, chunk_timeline_array in text_w_timeline.items():
        if chunk_timeline_array != None:
            for obj in chunk_timeline_array:
                # print("obj =>", obj)
                full_text = full_text + obj['text']
                if any(ele in obj['text'] for ele in SWEAR_WORDS_LIST):
                    chunk_swear_words[k] = []
                    words_timeline_array = obj['result']
                    # print("obj['result']", obj['result'])
                    for word_timeline in words_timeline_array:
                        print("chunk_swear_words[k]", chunk_swear_words[k])
                        print(word_timeline['word'], any(ele in word_timeline['word'] for ele in SWEAR_WORDS_LIST))
                        if any(ele in word_timeline['word'] for ele in SWEAR_WORDS_LIST):
                            # get it's start & end time
                            chunk_swear_words[k] = chunk_swear_words[k] + [word_timeline]
        
    print("===> chunk_swear_words")
    print(chunk_swear_words)

    if not os.path.isdir(SWEAR_CHUNKS_FOLDER):
        os.mkdir(SWEAR_CHUNKS_FOLDER)

    toxic = False

    # if swear words exist
    if chunk_swear_words:
        toxic = True
        beep = AudioSegment.from_file(GENERAL_FOLDER + "/" + "beep.wav", "wav")

        beep_extended = beep

        while beep_extended.duration_seconds < sound.duration_seconds:
            beep_extended = beep_extended + beep

        # create modified chunk{i}.wav
        for key, swear_words in chunk_swear_words.items():
            if swear_words != None:

                swear_count = 1

            try:
                # replace one swear word at a time
                for swear_word_chunk in swear_words:
                    if swear_count == 1:
                        fresh_swear_audio = AudioSegment.from_file(VOSK_CHUNKS_FOLDER + "/" + key + ".wav")

                        swear_start_time = swear_word_chunk['start'] * 1000
                        swear_end_time = swear_word_chunk['end'] * 1000
                        swear_chunk_total_time = swear_end_time - swear_start_time
                        
                        start_good_chunk = fresh_swear_audio[:swear_start_time]
                        # swear_word = swear_chunk[swear_start_time:swear_end_time]
                        end_good_chunk = fresh_swear_audio[swear_end_time:]
                        # split and beep audio.
                        swear_word_modified = beep_extended[0:swear_chunk_total_time]

                        new_chunk = start_good_chunk + swear_word_modified + end_good_chunk

                        chunk_path = os.path.join(SWEAR_CHUNKS_FOLDER, f"{key}.wav")
                        new_chunk.export(chunk_path, format="wav")
                    else:
                        processing_swear_audio = AudioSegment.from_file(SWEAR_CHUNKS_FOLDER + f"{key}.wav")

                        swear_start_time = swear_word_chunk['start'] * 1000
                        swear_end_time = swear_word_chunk['end'] * 1000
                        swear_chunk_total_time = swear_end_time - swear_start_time
                        
                        start_good_chunk = processing_swear_audio[:swear_start_time]
                        # swear_word = swear_chunk[swear_start_time:swear_end_time]
                        end_good_chunk = processing_swear_audio[swear_end_time:]
                        # split and beep audio.
                        swear_word_modified = beep_extended[0:swear_chunk_total_time]

                        new_chunk = start_good_chunk + swear_word_modified + end_good_chunk

                        chunk_path = os.path.join(SWEAR_CHUNKS_FOLDER, f"{key}.wav")
                        new_chunk.export(chunk_path, format="wav")

                    swear_count+=1
            except FileNotFoundError:
                print("File doesn't exist")
            except:
                print("Something went wrong while replacing swear words")

    # Begin with 1 second of silence
    new_audio = AudioSegment.from_file(GENERAL_FOLDER + "/" + "silent.wav", "wav")

    chunk_swear_words_keys = chunk_swear_words.keys()

    try:
        for i, chunk in enumerate(chunks, start=1):
            new_beeped_chunk = None
            if "chunk"+str(i) in chunk_swear_words_keys:
                print(f"Found TOXIC chunk{i}")
                new_beeped_chunk = AudioSegment.from_file(SWEAR_CHUNKS_FOLDER + "/" + f"chunk{i}.wav", "wav")
            
            if new_beeped_chunk != None:
                print(f"Merged TOXIC chunk{i}")
                new_audio = new_audio + new_beeped_chunk
            else:
                print(f"Merged SAFE chunk{i}")
                new_audio = new_audio + chunk
    except FileNotFoundError:
        print("File doesn't exist")
    except:
        print("Something went wrong while merging audio chunks")
    
    if not os.path.isdir(PROCESSED_AUDIO_FOLDER):
        os.mkdir(PROCESSED_AUDIO_FOLDER)

    new_audio_path = os.path.join(PROCESSED_AUDIO_FOLDER, filename+"."+extsn)
    new_audio.export(new_audio_path, format=extsn)

    data = {'full_text': full_text, 'toxic': toxic}

    # By design, rmtree fails on folder trees containing read-only files. If you want the folder to be deleted regardless of whether it contains read-only files, then use
    shutil.rmtree(VOSK_CHUNKS_FOLDER, ignore_errors=True)
    shutil.rmtree(SWEAR_CHUNKS_FOLDER, ignore_errors=True)
    shutil.rmtree(FETCHED_AUDIO_FOLDER, ignore_errors=True)

    return data
    # check if chunk exists in vosk-swear-audio-chunk. If yes then load it & append it instead


    # upload it to AWS. This cannot be undone as it will replace that audio. If the user selects don't beep then still the user will receive the beeped audio.

def analyze_audio(model, path, beep=False):
    

    uuid = str(uuid4())

    FETCHED_AUDIO_FOLDER = uuid + "-"+ BASE_FETCHED_AUDIO_FOLDER

    if not os.path.isdir(FETCHED_AUDIO_FOLDER):
        os.mkdir(FETCHED_AUDIO_FOLDER)
    
        # FETCH THE AUDIO & STORE IN THE DIRECTORY
        r = requests.get(path, allow_redirects=True)

        # our filename format on AWS doesn't have any "." except for the extension
        if path.find(".") == -1:
            print("Audio file doesn't have any extension")
            return

        # It is made sure that the file doesn't contain 2 dots as we are replacing the files with our naming convention.
        filename = path.split("/")[-1].split(".")[0]
        extsn = path.split("/")[-1].split(".")[-1]

        # extensions supported by the frontend
        valid_extsns = ["mp3", "wav", "ogg"]

        if not valid_extsns.count(extsn.lower()) > 0:
            print("Invalid audio file extension")
            return

        open(FETCHED_AUDIO_FOLDER + "/" + filename + "."+ extsn, 'wb').write(r.content)
        
        data = {}

        if beep == True:
            data = get_vosk_audio_transcription(model, uuid, filename, extsn.lower())
        else:
            data = get_vosk_audio_transcription_only(model, uuid, filename, extsn.lower())

        print("\n\n Full text is :-")
        print(data['full_text'])

        return {
            'toxic': data['toxic'],
            'dir_to_delete': uuid + "-" + BASE_PROCESSED_AUDIO_FOLDER,
            'filename': filename,
            'extsn': extsn
        }



    