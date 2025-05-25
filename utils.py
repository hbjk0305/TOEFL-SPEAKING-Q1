
import time
import sounddevice as sd
from scipy.io.wavfile import write

def countdown_timer(seconds, message):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{message} {mins:02d}:{secs:02d}"
        print(timer_display, end='\r')
        time.sleep(1)
    print(' ' * len(timer_display), end='\r')  # Clear timer line

def record_audio(filename, duration, fs=16000):
    print(f"녹음 시작! ({duration}초)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    countdown_timer(duration, "녹음 중:")
    sd.wait()
    write(filename, fs, recording)
    print("녹음 종료. 파일 저장:", filename)

def transcribe_audio(model, file_path, lang='en'):
    try:
        result = model.transcribe(file_path, language=lang)
        return result['text']
    except Exception as e:
        return f"음성 인식 오류: {e}"