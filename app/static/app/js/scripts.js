 // JavaScript to handle sidebar toggling
 document.getElementById("toggleBtn").addEventListener("click", function() {
    var sidenav = document.getElementById("mySidenav");
    var main = document.getElementById("contenido");
    if (sidenav.style.left === "-200px") {
    sidenav.style.left = "0";
    main.style.marginLeft = "200px";
    } else {
    sidenav.style.left = "-200px";
    main.style.marginLeft = "0";
    }
});

 document.getElementById("lectura").addEventListener("click", function() {
    var boton1 = document.getElementById("lectura");
    var boton2 = document.getElementById("detener");
    var icono1 = document.getElementById("off");
    var icono2 = document.getElementById("on");
    boton1.style.display ="none";
    boton2.style.display ="block";
    icono1.style.display ="none";
    icono2.style.display ="block";
});

document.getElementById("detener").addEventListener("click", function() {
    var boton1 = document.getElementById("lectura");
    var boton2 = document.getElementById("detener");
    var icono1 = document.getElementById("off");
    var icono2 = document.getElementById("on");
    boton1.style.display ="block";
    boton2.style.display ="none";
    icono1.style.display ="block";
    icono2.style.display ="none";
});