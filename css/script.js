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
	$(".edit").html("Esconder Edit |"),
	$(".login").hide("fast"),
	$(".registrar").hide("fast"),
	$("textarea").focus();
	$("textarea").css("display", "block");
	i=1;
	}else{
		$(".edit").html("Mostrar Edit |"),
		$(".login").hide("fast"),
		$(".registrar").hide("fast");
		$("textarea").css("display", "none");	
i=0;
	}	
}

