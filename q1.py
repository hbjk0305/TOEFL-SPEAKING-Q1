import random
import time
import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper

def countdown_timer(seconds, message):
    for remaining in range(seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer_display = f"{message} {mins:02d}:{secs:02d}"
        print(timer_display, end='\r')
        time.sleep(1)
    print(' ' * len(timer_display), end='\r')  # Clear timer line

def load_questions(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

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

def make_safe_filename(problem_count, question, attempt):
    # 문제 앞부분에서 특수문자 제거 및 길이 제한
    base = ''.join(c for c in question[:30] if c.isalnum() or c == ' ').rstrip().replace(' ', '_')
    return f"{problem_count}_{base}_try{attempt}.wav"

def main():
    question_file = 'q1-questions.txt'
    output_dir = "./res-q1"
    os.makedirs(output_dir, exist_ok=True)
    questions = load_questions(question_file)
    used = set()
    problem_count = 1

    print("Whisper 모델을 불러오는 중입니다...")
    model = whisper.load_model("base")  # 한번만 로드

    while True:
        available = [q for q in questions if q not in used]
        if not available:
            print("모든 문제를 다 풀었습니다!")
            break
        question = random.choice(available)
        used.add(question)
        attempt = 1

        while True:
            print(f"\n[문제 {problem_count}] (시도 {attempt})")
            print(question)
            time.sleep(15)
            print("\n15초 준비시간이 시작됩니다.")
            countdown_timer(15, "준비 중:")

            safe_filename = make_safe_filename(problem_count, question, attempt)
            response_path = os.path.join(output_dir, safe_filename)
            print("이제 45초간 답변을 녹음합니다!")
            record_audio(response_path, 45)

            print("\n[YOUR ANSWER]")
            transcript = transcribe_audio(model, response_path, lang='en')  # 'ko'로 바꾸면 한국어
            print(transcript)

            user_input = input(
                "\n다음 문제는 'next', 종료는 'quit', 같은 문제 다시 도전은 'again'을 입력하세요: "
            ).strip().lower()
            if user_input == 'next':
                problem_count += 1
                break
            elif user_input == 'quit':
                print("프로그램을 종료합니다.")
                return
            elif user_input == 'again':
                attempt += 1
                continue
            else:
                print("잘못된 입력입니다. 'next', 'again' 또는 'quit'을 입력하세요.")

if __name__ == "__main__":
    main()
