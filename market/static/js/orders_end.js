//Script para mandar los numeros de las cantidades

var botonNumeros = document.getElementsByName('data-number');
const botonDelete = document.getElementsByName('data-delete')[0];
var result = document.getElementById('result');
const dot = document.getElementsByName('data-dot');


var opeActual ='';
tiempo = 1000;
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}
botonNumeros.forEach(function(boton){
    boton.addEventListener('click',function(){
        s = boton.innerText;
        //alert(boton.innerText)
        agregarNumero(s);
    })
});
botonDelete.addEventListener('click',function(){
    clear();
    actualizarDisplay();
});

dot.forEach(function(boton){
  boton.addEventListener('click',function(){
    darComa();
  })
});

function agregarNumero(num){
    opeActual = opeActual.toString() + num.toString();
    actualizarDisplay();
    sleep(250);

}

function clear(){
    opeActual = '';
}

function darComa(){
  alert("entra a e esta funcion")
    if(num1 == 0) {
        num1 = '0.';
      } else if(num1.indexOf('.') == -1) {
          num1 += '.';
        }
            actualizarDisplay();
        }
function actualizarDisplay(){
    result.value = opeActual;
}
