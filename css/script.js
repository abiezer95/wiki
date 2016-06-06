$(document).ready(function(){
	$(".login").css("display", "none"),
	$(".registrar").css("display", "none");
})

function reg(){
	$(".login").css("display", "none"),
	$(".registrar").show("fast")
}function login(){
	$(".registrar").css("display", "none"),
	$(".login").show("fast")
}

function cerrar(){
	$(".login").hide("fast"),
	$(".registrar").hide("fast")
}
var i=0;
function edit(){
	if(i==0){
	$(".content").html('<h2>Wiki Time - post</h2><form method="post" ><textarea rows="10" cols="100" placeholder="Escribe tu articulo aqui" name="text" id="limpiar" required></textarea><br><br><button>Postear</button></form><br><button  onclick=\'$("#limpiar").val("");$("#limpiar").focus();\'>Limpiar todo</button>'),
	$(".edit").html("Esconder Edit |");
	$(".login").hide("fast"),
	$(".registrar").hide("fast"),
	$("textarea").focus();
	i=1;
	}else{
		$(".content").html('<b style="opacity:0.8;font-size:25px;font-weight:lighter;text-decoration:underline;">Publicaciones</b>'),
		$(".edit").html("Mostrar Edit |");
		$(".login").hide("fast"),
	$(".registrar").hide("fast")
i=0;
	}	
}

