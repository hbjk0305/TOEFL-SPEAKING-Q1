import os, time
import whisper

from utils import countdown_timer, record_audio, transcribe_audio

# ...existing code...

def main():
    print("Whisper 모델을 불러오는 중입니다...")
    model = whisper.load_model("base")  # 한번만 로드
    output_dir = "./res-q{}"
    for i in [2,3,4]:
        os.makedirs(output_dir.format(i), exist_ok=True)

    # 문제 유형 입력 및 시간 설정
    while True:
        qtype = input("문제 유형을 입력하세요 (2, 3, 4): ").strip()
        if qtype == '2' or qtype == '3':
            prep_time, answer_time = 30, 60
            break
        elif qtype == '4':
            prep_time, answer_time = 20, 60
            break
        else:
            print("2, 3, 4 중 하나를 입력하세요.")

    attempt = 1
    current_time = time.strftime("%Y%m%d_%H%M%S")
    while True:
        print(f"\n[문제 {qtype}] (시도 {attempt})")
        print(f"\n{prep_time}초 준비시간이 시작됩니다.")
        countdown_timer(prep_time, "준비 중:")
        safe_filename = f"{current_time}_try{attempt}.wav"
        response_path = os.path.join(output_dir.format(qtype), safe_filename)
        print(f"이제 {answer_time}초간 답변을 녹음합니다!")
        record_audio(response_path, answer_time)

        print("\n[YOUR ANSWER]")
        transcript = transcribe_audio(model, response_path, lang='en')
        print(transcript)

        user_input = input(
            "\n다음 문제는 'next', 종료는 'quit', 같은 문제 다시 도전은 'again'을 입력하세요: "
        ).strip().lower()
        if user_input == 'next':
            attempt = 1
            continue
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