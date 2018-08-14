Tensorflow와 Flask를 사용한 그림판 숫자 인식
===
그림판에 숫자(0~9)를 그리고 convolution neural network(CNN)를 사용하여 숫자 인식.
파이썬 웹 애플리케이션인 플라스크(Flask)를 사용하였고 CNN은 Tensorflow를 사용하여 구현하였습니다.
그림판에는 선굵기 조절, 그림판 저장, 지우기, 숫자 예측 기능이 있습니다.

Requirement
---
1. Python 3.5.x
2. Tensorflow
3. Flask

Usage
---
### Command
'python app_main.py'

웹 브라우저에서 '127.0.0.1:5100' or 'localhost:5100'으로 접속

Results
---
![Alt Text](https://github.com/IzPerfect/Digit_recognition-tensorflow-flask/blob/master/image/digit_recognition.gif)

Reference Implementations
---
+ http://dol2156.tistory.com/333
+ https://github.com/MartinRep/Digit-OCR