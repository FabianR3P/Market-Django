var botonProduct = document.getElementsByName('boton-product');

botonProduct.forEach(function(boton){
    boton.addEventListener('click',function(){

        //alert(this.value);
        var s = this.value;
        var st = String(s)
        console.log("Hola desde la funcion de los botones");
        console.log(s);
        console.log(st);
        cod = st.slice(0,2);
        var pric = st.slice(3,4);
        console.log(cod);
        console.log(pric);
        resultado.value =  cod;
        price.value = pric;

    })
});
function mandarDatos(){
  //alert(botonUser);
    document.formulario1.submit();
}

const botonNumeros = document.getElementsByName('data-number');
const botonDelete = document.getElementsByName('data-delete')[0];
var opeActual ='';

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
