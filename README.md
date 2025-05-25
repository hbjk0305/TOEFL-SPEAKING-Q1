## Prerequisite
```
conda install -c conda-forge ffmpeg # if ffmepg is not installed
pip install -r requirements.txt
# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128    # for GPU
```

## For an independent question
q1-questions.txt is from [here](https://gist.github.com/mdibaiee/6a181163a06432f0785ccb1894b05ede).
```
python indep.py
```

## For integrated questions
```
python integrated.py
# 문제 번호 입력하면 준비시간과 녹음시간이 자동으로 설정된다.
# 문제는 제공안함. 녹음 용도로만 사용 가능.
```

## Thanks to GPT
내용 긁어다가 GPT한테 첨삭해달라고 하면 잘해준다.
(API 연결하면 진짜 편할거같은데ㅠ)

## TODO
- [ ] GPT 첨삭 API 연결하기
