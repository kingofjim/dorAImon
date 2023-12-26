import pyaudio
import wave
import time
import threading


class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recording_thread = None

    def start_recording(self):
        self.audio_data = []
        self.is_recording = True

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100

        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)

        print("Recording...")
        while self.is_recording:
            data = self.stream.read(CHUNK)
            self.audio_data.append(data)

        print("Finished recording.")

    def stop_recording(self):
        self.is_recording = False

    def save_audio(self, file_name):
        if len(self.audio_data) > 0:
            wf = wave.open(file_name, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.audio_data))
            wf.close()
            print(f"Audio saved as '{file_name}'")

    def start_recording_thread(self):
        self.recording_thread = threading.Thread(target=self.start_recording)
        self.recording_thread.start()

    def stop_recording_thread(self):
        self.stop_recording()
        self.recording_thread.join()


# # Usage example:
# recorder = AudioRecorder()
# time.sleep(1)
# recorder.start_recording_thread()
#
# # Simulate recording for 5 seconds
# time.sleep(5)
#
# recorder.stop_recording_thread()
# recorder.save_audio("recorded_audio.wav")  # Save recorded audio to a WAV file
