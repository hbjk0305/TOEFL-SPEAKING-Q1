import random
import time
import sounddevice as sd
from scipy.io.wavfile import write
import sys

def countdown_timer(seconds, message):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{message} {mins:02d}:{secs:02d}"
        print(timer_display, end='\r')
        time.sleep(1)
    print(' ' * len(timer_display), end='\r')  # 타이머 지우기

def get_random_question(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    return random.choice(lines)

def record_audio(filename, duration, fs=16000):
    print(f"녹음 시작! ({duration}초)")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    countdown_timer(duration, "녹음 중:")  # 녹음 중에도 타이머 표시
    sd.wait()
    write(filename, fs, recording)
    print("녹음 종료. 파일 저장:", filename)

def main():
    question_file = 'q1-questions.txt'
    question = get_random_question(question_file)
    print("\n[문제]")
    print(question)
    print("\n15초 준비시간이 시작됩니다.")
    countdown_timer(15, "준비 중:")  # 준비 타이머

    print("이제 45초간 답변을 녹음합니다!")
    record_audio('res-q1/{}.wav'.format(question.split('\t')[0], 45)  # 녹음 타이머

if __name__ == "__main__":
    main()
