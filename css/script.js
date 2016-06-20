$(document).ready(function() {
    elementosocultos();
    graphic();
});

function eliminar() {
    var id = $(".id").val();
    var url = "/eliminar/deletepost?post=" + id + "";
    $.post(url, function(e) {
            var inter = setInterval(function() {
                $("." + id + "").css("display", "none");
                //$("#feed").html(e)
                clearInterval(inter);
            }, 2000);

        }).done(function() {
            alert("Tu publicacion se Elimino correctamente");
        })
        .fail(function() {
            alert("Error al eliminar la publicacion");
        })
    $("#content2").css({
            "-webkit-filter": "blur(0px)",
            "filter": "blur(0px)"
        }),
        $(".load").css("display", "none");
    $("#content").css("display", "none");
    $("." + id + "").css({
        "background": "#FF0040",
        "color": "#fff"
    })
}

function graphic() {
    valores = $(".graphic center input").val()
    valores = valores.split(",");
    var i = 0,
        e = 20;
    var color = ["#2EFE2E", "#FE9A2E", "#FFFF00", "#0080FF"]
    for (valor in valores) {
        if (valores[i] == "") {
            var val = valores[i];
            val = 1;
        } else {
            var val = valores[i];
        }
        var valor = val / 3;
        $(".graphic .graficos").append("<section class='a" + i + "'>" + valores[i] + "</section>");
        $(".graficos .a" + i + "").css({
            "background": "" + color[i] + "",
            "left": "" + e + "px",
            "height": "" + valor + "%"
        })
        i = i + 1;
        e = e + 110 / 2;
    }
}

function privatepost(user, id) {
    var url = "/private/post?id=" + id + "&user=" + user + "";
    $("#feed img").attr("src", "/images/hide.png");
    $.post(url, function(e) {
        location.href = "pub";
    }).fail(function() {
        alert("no se ha podido ocultar la publicacion")
    })
}

function publicpost(user, id) {
    var url = "/private/post?id=" + id + "&user=" + user + "";
    $("#feed img").attr("src", "/images/hide.png");
    $.post(url, function(e) {
        location.href = "pub";
    }).fail(function() {
        alert("no se ha podido ocultar la publicacion")
    })
}

function post(p, user, id) {
    $("#content2").css({
            "-webkit-filter": "blur(3px)",
            "filter": "blur(3px)"
        }),
        $("#content").css("display", "block"),
        $(".load").css({
            "display": "block",
            "width": "400px",
            "height": "50px",
            "left": "35%"
        }),
        $(".load").html("<center><img src='/images/loading.gif' width='50'></center>"),
        $(".id").val("");
    posts = p.replace("\n", "");
    var pub = "<br><center><h3>Publicacion hecha por " + user + "</h3><hr><br><b>" + posts + "</b><br><button onclick='cerrar()'>Cerrar</button><br><br><button onclick='comment()'>Comentarios</button><button onclick='eliminar()'>Eliminar Post</button></center>";
    var inter = setInterval(function() {
        $(".load").css({
                "width": "500px",
                "height": "400px",
                "left": "30%"
            }),
            $(".load").html(pub);
        $(".id").val(id)
        clearInterval(inter);
    }, 2000);
}

function bestcomment() {
    $("#content2").css({
            "-webkit-filter": "blur(3px)",
            "filter": "blur(3px)"
        }),
        $(".bestcomment").load("/best/comments"),
        $(".bestcomment").css("display", "block")
}

function deletecomment(fecha, texto, id) {
    var url = "/eliminar/deletecomment?fecha=" + fecha + "&texto=" + texto + "";
    $.post(url, function(e) {
            var inter = setInterval(function() {
                    $("#" + id + "").css("display", "none");
                    clearInterval(inter);
                }, 1000)
                //$(".comment center").html(e)
        }).done(function(e) {
            alert("eliminado con exito");
        })
        .fail(function() {
            alert("Error al eliminar el comentario");
        })
}

function comment() {
    $(".load").css("display", "none");
    $(".comment").css({
        "top": "-500px",
        "left": "35%",
        "display": "block"
    });
    $(".comment center").html("")
    $.getJSON('/content/.json', function(data) {
        var id = $(".id").val()
        var i = 0;
        for (d in data) {
            if (id == d) {
                for (n in data[d]) {
                    comments = data[d][n].split("*/");
                    $(".comment center").append("<section id='" + comments[2] + "'>" + comments[0] + "<br><tt> - Publicado por a - " + comments[1] + " - <tt onclick='var id=\"" + comments[2] + "\";var fecha=\"" + comments[3] + "\";var texto=\"" + comments[0] + "\";deletecomment(fecha, texto, id)' style='cursor:pointer;text-decoration:underline'>click aqui para eliminar <input type='hidden' value='" + comments[2] + "'></tt></tt><hr></section>");
                    i = i + 1;
                }
            }
        }
    })
    var inter = setInterval(function() {
        $(".comment").css({
                "width": "400px",
                "height": "500px",
                "top": "55px",
                "-webkit-transition": "top 0.3s"
            }),
            clearInterval(inter);
    }, 500);
}

function reg() {
    $(".login").css("display", "none"),
        $(".registrar").show("fast")
}

function login() {
    $(".registrar").css("display", "none"),
        $(".login").show("fast")
}

function cerrar() {
    $("#content2").css({
            "-webkit-filter": "blur(0px)",
            "filter": "blur(0px)"
        }),
        $(".login").hide("fast"),
        $(".registrar").hide("fast")
    $("#content").css("display", "none");
    $(".load").css("display", "none");
    $(".comment").css("display", "none");
    $(".bestcomment").css("display", "none");
}
var i = 0;

function edit() {
    if (i == 0) {
        $(".edit").html("Esconder Edit |"),
            $(".login").hide("fast"),
            $(".registrar").hide("fast"),
            $("textarea").focus();
        $("textarea").css("display", "block");
        i = 1;
    } else {
        $(".edit").html("Mostrar Edit |"),
            $(".login").hide("fast"),
            $(".registrar").hide("fast");
        $("textarea").css("display", "none");
        i = 0;
    }
}

var elementosocultos = function() {
    $(".login").css("display", "none"),
        $(".registrar").css("display", "none");
    $("#content").css("display", "none");
    $(".load").css("display", "none");
    $(".comment").css("display", "none");
}