//Script para mandar los numeros de las cantidades
var botonNumeros = document.getElementsByName('data-number');
const botonDelete = document.getElementsByName('data-delete')[0];
var result = document.getElementById('result');
const dot = document.getElementsByName('data-dot');
var resultdate = document.getElementById('resultdate');
var resultDay = document.getElementById('resultDay');


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

function mandarDatosOrder(){
    document.formularioOrder.submit();

}
//Script para mandar la fehca y hora del pedidos
var fecha = [2];


var botonHora = document.getElementsByName('hora');
botonHora.forEach(function(boton){
    boton.addEventListener('click',function(){
        s = boton.innerText;
        fecha[0] = s;
    })
});

var botonmin = document.getElementsByName('min');
botonmin.forEach(function(boton){
    boton.addEventListener('click',function(){
        s = boton.innerText;
        fecha[1]=s;
    })
});


var botmatutino = document.getElementsByName('matutino');
botmatutino.forEach(function(boton){
    boton.addEventListener('click',function(){
      var hoy = new Date();
        //result = hoy.getHours() + ':' + hoy.getMinutes();
         fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + Intl.DateTimeFormat('en', { day: '2-digit' }).format(hoy);
        result = '06:00';
        alert("El pedido sera para la mañana a las:" + ' ' +result + ' ' + 'del ' + fecha)
        resultDay.value = fecha;
        resultdate.value  = result;

    })
});

var botvespertino = document.getElementsByName('vespertino');
botvespertino.forEach(function(boton){
    boton.addEventListener('click',function(){
      var hoy = new Date();
        //result = hoy.getHours() + ':' + hoy.getMinutes();
        fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + Intl.DateTimeFormat('en', { day: '2-digit' }).format(hoy) ;
        result = '15:00';
        alert("El pedido sera para la tarde a las:" + ' ' +result + ' ' + 'del ' + fecha)
        resultDay.value = fecha;
        resultdate.value  = result;

    })
});

function zfill(number, width) {
    var numberOutput = Math.abs(number); /* Valor absoluto del número */
    var length = number.toString().length; /* Largo del número */
    var zero = "0"; /* String de cero */

    if (width <= length) {
        if (number < 0) {
             return ("-" + numberOutput.toString());
        } else {
             return numberOutput.toString();
        }
    } else {
        if (number < 0) {
            return ("-" + (zero.repeat(width - length)) + numberOutput.toString());
        } else {
            return ((zero.repeat(width - length)) + numberOutput.toString());
        }
    }
}
var botmatutino = document.getElementsByName('matutino-next');
botmatutino.forEach(function(boton){
    boton.addEventListener('click',function(){
      var hoy = new Date();
        //result = hoy.getHours() + ':' + hoy.getMinutes();
        a=hoy.getDate();
        b=a.toString().length;
        if (b==1) {
          fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + zfill(hoy.getDate(),2) ;
        }else {
          day_first = hoy.getDate() + 1;
          fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + day_first ;
        }

        result = '06:00';
        alert("El pedido sera para la mañana a las:" + ' ' +result + ' ' + 'del ' + fecha)
        resultDay.value = fecha;
        resultdate.value  = result;

    })
});

var botvespertino = document.getElementsByName('vespertino-next');
botvespertino.forEach(function(boton){
    boton.addEventListener('click',function(){
      var hoy = new Date();
        //result = hoy.getHours() + ':' + hoy.getMinutes();
        a=hoy.getDate();
        b=a.toString().length;
        if (b==1) {
          fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + zfill(hoy.getDate(),2) ;
        }else {
          day_first = hoy.getDate() + 1;
          fecha =  hoy.getFullYear()  + '-' + ( hoy.getMonth() + 1 ) + '-' + day_first ;
        }

        result = '15:00';
        alert("El pedido sera para la tarde a las:" + ' ' +result + ' ' + 'del ' + fecha)
        resultDay.value = fecha;
        resultdate.value  = result;

    })
});

var botonmv = document.getElementsByName('mv');
botonmv.forEach(function(boton){
    boton.addEventListener('click',function(){
        s = boton.innerText;
        fecha[2]=s;
        actualizarCampo();
    })
});


function actualizarCampo(){
    if(fecha[2]=='p.m' && fecha[0]==1){
      a= 13 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;
    }

    else if(fecha[2]=='p.m' && fecha[0]==2){
      a= 14 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==3){
      a= 15 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==4){
      a= 16 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==5){
      a= 17 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==6){
      a= 18 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==7){
      a= 19 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==8){
      a= 20 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==9){
      a= 21 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==10){
      a= 22 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==11){
      a= 23 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;

    }
    else if(fecha[2]=='p.m' && fecha[0]==12){
      a= 24 + ':'+ fecha[1];
      alert(a);
      resultdate.value = a;
    }
    else{
      a = fecha[0]+':'+fecha[1];
      alert(a);
      resultdate.value = a;

    }


}
