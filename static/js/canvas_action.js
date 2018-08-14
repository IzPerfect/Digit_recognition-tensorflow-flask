var canvas, context, tool;
window.onload = function(){

  canvas = document.getElementById('drawCanvas');
  context = canvas.getContext('2d');
  context.lineWidth = 5;

  tool = new tool_pencil();
  canvas.addEventListener('mousedown', ev_canvas, false);
  canvas.addEventListener('mousemove', ev_canvas, false);
  canvas.addEventListener('mouseup',   ev_canvas, false);
}

function predictlocalBoard()
   {
    let formdata = new FormData();
     formdata.append("image", dataURItoBlob(canvas.toDataURL('image/png')));
     let request = new XMLHttpRequest();

     request.onload = function(){
      if (this.status == 200){
      let answer = request.response.prediction
      document.getElementById('show').innerText = answer;
      }
      else{
        document.getElementById('show').innerText = 'No access';
      }
     }
     request.responseType = 'json';
     request.open('POST', '/classify', true);
     console.log(formdata);
     request.send(formdata);
   }

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

function saveBoard()
   {
      var link = document.createElement('a');
      link.download = "canvas.png";
      link.href = canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");;
      link.click();
   }

function clearBoard()
   {
     context.clearRect(0, 0, canvas.width, canvas.height);
     context.beginPath();
     document.getElementById('show').innerText = "Blank";
   }


function changeLineWidth(width)
   {
     context.lineWidth = width;
   }

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
