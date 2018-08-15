var canvas, context, tool;

// window.onload를 통해 시작시에 function()실행
window.onload = function(){

  // getElementById메서드로 canvas요소를 표시할 DOM을 호출
  canvas = document.getElementById('drawCanvas');

  // canvas그리기를 수행하기 위해 getContext()메서드를 호출
  context = canvas.getContext('2d');
  context.lineWidth = 5;// 선굵기 초기 설정

  // 마우스 움직임에 따른 그리기 이벤트 등록
  tool = new tool_pencil();
  canvas.addEventListener('mousedown', ev_canvas, false);
  canvas.addEventListener('mousemove', ev_canvas, false);
  canvas.addEventListener('mouseup',   ev_canvas, false);
}

// 숫자 인식
function predictBoard()
   {
     let formdata = new FormData();

     // toDataURL를 통해 PNG타입의 base64인코딩이 된 data url형식의 문자열 반환
     // data url을 dataURItoBlob함수를 통해 Blob객체를 return
     formdata.append("image", dataURItoBlob(canvas.toDataURL('image/png')));
     let request = new XMLHttpRequest();//서버와 클라이언트 요청처리를 위한 객체

     request.onload = function(){
       // 200은 서버가 클라이언트의 요청을 성공적으로 처리했을 때 return 하는 숫자
      if (this.status == 200){
      let answer = request.response.prediction// 서버의 응답을 get
      document.getElementById('show').innerText = answer;// 예측 결과 출력
      }
      else{
        document.getElementById('show').innerText = 'No access';
      }
     }
     request.responseType = 'json';
     request.open('POST', '/classify', true);// url 세팅
     console.log(formdata);// 디버깅을 위해 로깅
     request.send(formdata);// POST방식으로 서버에 request
   }

// FormData에 바이너리 파일로 변환된 data url을 세팅
function dataURItoBlob(dataURI){
var byteString;
if (dataURI.split(',')[0].indexOf('base64') >= 0)
    byteString = atob(dataURI.split(',')[1]);
else
    byteString = unescape(dataURI.split(',')[1]);

var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

var ia = new Uint8Array(byteString.length);
for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
}
return new Blob([ia], {type:mimeString});
}

// 그림판에 그린 그림 저장
function saveBoard()
   {
      var link = document.createElement('a');
      link.download = "canvas.png";
      link.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");;
      link.click();
   }

// 그림판 그림 지우기
function clearBoard()
   {
     context.clearRect(0, 0, canvas.width, canvas.height);
     context.beginPath();
     document.getElementById('show').innerText = "Blank";
   }

// 그림판 선굵기 변경
function changeLineWidth(width)
   {
     context.lineWidth = width;
   }

// 그리기 펜 움직임 설정
function tool_pencil ()
{
    var tool = this;

    this.started = false;
    this.mousedown = function (ev)
    {
        context.beginPath();
        context.moveTo(ev._x, ev._y);
        tool.started = true;
    };

    this.mousemove = function (ev)
    {
        if (tool.started)
        {
            context.lineTo(ev._x, ev._y);
            context.stroke();
        }
    };

    this.mouseup = function (ev)
    {
      if (tool.started){
            tool.mousemove(ev);
            tool.started = false;
      }
    };
}

function ev_canvas (ev)
{
    if (ev.layerX || ev.layerX == 0)
    {
      ev._x = ev.layerX;
      ev._y = ev.layerY;
    }
    else if (ev.offsetX || ev.offsetX == 0)
    {
      ev._x = ev.offsetX;
      ev._y = ev.offsetY;
    }
    var func = tool[ev.type];
    if (func) {
        func(ev);
    }
}
