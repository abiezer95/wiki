$(document).ready(function(){
	$(".login").css("display", "none"),
	$(".registrar").css("display", "none");
	$("#content").css("display", "none");
	$(".load").css("display", "none");
	$(".comment").css("display", "none");
});

function pub(p, user, id){
	$("#content2").css({"-webkit-filter": "blur(3px)", "filter": "blur(3px)"}),
	$("#content").css("display", "block"),
	$(".load").css({"display": "block", "width": "400px", "height": "50px","left": "35%"}),
	$(".load").html("<center><img src='/images/loading.gif' width='50'></center>");
	$(".id").val("")
p=p.replace("\n", "")
var pub="<br><center><h3>Publicacion hecha por "+user+"</h3><hr><br><b>"+p+"</b><br><button onclick='cerrar()'>Cerrar</button></center>";
var inter=setInterval(function(){
		$(".load").css({"width": "500px", "height": "400px", "left": "15%"}),
		$(".comment").css({"display": "block", "width": "400px", "height": "500px"}),
		$(".load").html(pub);
		$(".id").val(id)
		clearInterval(inter);
	},2000);
}

function reg(){
	$(".login").css("display", "none"),
	$(".registrar").show("fast")
}function login(){
	$(".registrar").css("display", "none"),
	$(".login").show("fast")
}

function cerrar(){
	$("#content2").css({"-webkit-filter": "blur(0px)", "filter": "blur(0px)"}),
	$(".login").hide("fast"),
	$(".registrar").hide("fast")
	$("#content").css("display", "none");
	$(".load").css("display", "none");
	$(".comment").css("display", "none");
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

