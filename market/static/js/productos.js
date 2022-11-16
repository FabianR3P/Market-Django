// TECLADO DE PRODUCTOS
var botonProduct = document.getElementsByName('boton-product');

botonProduct.forEach(function(boton){
    boton.addEventListener('click',function(){

        //alert(this.value);
        var s = this.value;
        var st = String(s)
        console.log("Hola desde la funcion de los botones");
        cod = st.slice(0,2);
        var pric = st.slice(3,4);
        console.log(cod);
        console.log(pric);
        resultado.value =  cod;
        price.value = pric;

    })
});

//Botones de ABARROTES

var botonProductAb = document.getElementsByName('boton-productAb');

botonProductAb.forEach(function(boton){
    boton.addEventListener('click',function(){

        //alert(this.value);
        resultado.value =  this.value;
        price.value = '1';


    })
});

//opera crucial excite wish seek absorb citizen subway weapon fiber shadow behind

const botonNumeros = document.getElementsByName('data-number');
const botonDelete = document.getElementsByName('data-delete')[0];
var result = document.getElementById('result');
var botonswitch = document.querySelector('.switch-input');
var botonenviar = document.querySelector('.botonenviar')
var opeActual ='';
var tiempo = 0;
var rev = false;
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}
//Encendido de un off - on
if( localStorage.var_switch == "true"){
  botonswitch.setAttribute("checked","checked");
  botonenviar.setAttribute("disabled","");
  tiempo = 900;

}else {
  botonenviar.setAttribute("onclick","mandarDatos()");
  tiempo = 4000
}
    function yesboton(){
      var_switch = true;
      localStorage.var_switch = var_switch;
    }

    function noboton(){
      var_switch = false;
      localStorage.var_switch = var_switch;
    }

//Encendido de un off - on

//TELCADO NUMERICO

botonNumeros.forEach(function(boton){
    boton.addEventListener('click',function(){
        //alert(boton.innerText);
        agregarNumero(boton.innerText);
        setTimeout(function(){
          if(tiempo == 1){
          agregarNumero()
        }else{mandarDatos()}
      },tiempo); // 1000ms = 1

    })
});
botonDelete.addEventListener('click',function(){
    clear();
    actualizarDisplay();
});

function agregarNumero(num){
    opeActual = opeActual.toString() + num.toString();
    actualizarDisplay();
    sleep(250);

}

function clear(){
    opeActual = '';
}

function actualizarDisplay(){
    result.value = opeActual;
}

function pruebasTeclado(){
  console.log("Mande datos");
  alert("Mande datos");
}

function mandarDatos(){
    document.formulario1.submit();
}

clear();
//TERMINA TECLADO NUMERICO

//mensajes tiempo en pantalla

//setTimeout(function(){
  //if($('#msg').length >0){
    //$('#msg').remove();
  //}
//},3000)

