import os, time
import whisper
import winsound
from utils import countdown_timer, record_audio, transcribe_audio


def main():
    print("Whisper 모델을 불러오는 중입니다...")
    model = whisper.load_model("base")  # 한번만 로드
    output_dir = "./res-q{}"
    for i in [0, 2, 3, 4,]:
        os.makedirs(output_dir.format(i), exist_ok=True)

    while True:
        # 문제 유형 입력 및 시간 설정
        while True:
            qtype = input("문제 유형을 입력하세요 (1 / 2 / 3 / 4): ").strip()
            if qtype == '1':
                prep_time, answer_time = 15, 45
                break
            if qtype == '2' or qtype == '3':
                prep_time, answer_time = 30, 60
                break
            elif qtype == '4':
                prep_time, answer_time = 20, 60
                break
            elif qtype == '0':
                prep_time, answer_time = 0, 60
                break
            else:
                print("1, 2, 3, 4 중 하나를 입력하세요.")

        attempt = 1
        current_time = time.strftime("%Y%m%d_%H%M%S")
        while True:
            print(f"\n[문제 {qtype}] (시도 {attempt})")
            if qtype == '2' or qtype == '3':
                print("삐 소리 후, 문제를 읽어주세요.")
                time.sleep(1)  # 잠시 대기
                winsound.Beep(1000, 500)
                countdown_timer(45, "문제를 읽어주세요:")
                print("문제 읽기가 끝났습니다.")
                winsound.Beep(1000, 500)
            if qtype != '0':
                print("리스닝을 들은 후, Enter를 누르면 준비시간이 시작됩니다.")
                input("Enter를 누르세요...")
                print(f"\n삐 소리 후, {prep_time}초 준비시간이 시작됩니다.")
                time.sleep(1)
                winsound.Beep(1000, 500)
                countdown_timer(prep_time, "준비 중:")
            safe_filename = f"{qtype}_{current_time}_try{attempt}.wav"
            response_path = os.path.join(output_dir.format(qtype), safe_filename)
            print(f"삐 소리 후, {answer_time}초간 답변을 녹음합니다!")
            time.sleep(1)  # 잠시 대기
            winsound.Beep(1000, 500)
            record_audio(response_path, answer_time)

            print("\n[YOUR ANSWER]")
            transcript = transcribe_audio(model, response_path, lang='en')
            print(transcript)

            user_input = input(
                "\n다음 문제는 'next', 종료는 'quit', 같은 문제 다시 도전은 'again'을 입력하세요: "
            ).strip().lower()
            if user_input == 'next':
                break  # 바깥 while True로 돌아가서 qtype을 다시 입력받음
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