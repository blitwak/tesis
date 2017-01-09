
$(function() {
   (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";

    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));
 

  var app_id = '717620135073477';
  var scopes = "public_profile,email";

  var usuarioLog = ""

var loginMenu = '    <li class="active" id="login-link"><a href="#"  class="login">Iniciar sesión con facebook</a></li>'+
    '    <li><a href="#comojugar">Cómo jugar?</a></li>'+
    '           <li><a href="#sobre">De que trata la tesis?</a></li>'+
    '           <li><a href="#contact">Contacto</a></li>'


var div_session3 = '<li class="active" id="comenzarJugar"><a href="#">Jugar</a></li>' +
'    <li><a href="#comojugar">Cómo jugar?</a></li>'+
 '   <li><a href="#sobre">De que trata la tesis?</a></li>'+
  ' <li><a href="#contact">Contacto</a></li>'+
        '<li><a href="#" id="logout">Cerrar sesión</a></li>';

  var btn_jugar =  '<a href="#" id="btncentral-jugar" class="btn btn-primary btn-xl page-scroll login">Jugar!</a>';
var btn_jugar2 =  '<a href="#" id="btnabajo-jugar" class="btn btn-default btn-xl sr-button login">Jugar!</a>'

    var btn_central_login = '<a href="" id="login-link1" class="btn btn-primary btn-xl page-scroll login">Ingresar con Facebook</a>';
    var btn_abajo_login = '<a href="" id="login-link2" class="btn btn-default btn-xl sr-button login">Ingresar con Facebook</a>'


    var menuOriginal =      '<li class="active" id="login-link"><a href="#"  class="login">Iniciar sesión con facebook</a></li>' +
    '<li><a href="#">Algo m&aacute;s?</a></li>' +
    '<li><a href="#">Contacto</a></li>';

  window.fbAsyncInit = function() {

      FB.init({
        appId      : app_id,
        status     : true,
        cookie     : true, 
        xfbml      : true, 
        version    : 'v2.8'
      });


//      FB.getLoginStatus(function(response) {
  //      statusChangeCallback(response, function() {});
    //  });
    };

    var statusChangeCallback = function(response, callback) {
      console.log(response);
      
      if (response.status === 'connected') {
          getFacebookData();
      } else {
        callback(false);
      }
    }

    var checkLoginState = function(callback) {
      FB.getLoginStatus(function(response) {
          callback(response);
      });
    }

    var getFacebookData =  function() {
      FB.api('/me', function(response) {
          console.log("hola!!");

        // $('#menulogin').after(div_session3);
          var menu= document.getElementById('menu-links');
          menu.innerHTML = div_session3;

          var menu= document.getElementById('btn-central');
          menu.innerHTML = btn_jugar;

          var menu= document.getElementById('btn-abajo');
          menu.innerHTML = btn_jugar2;
//http://stackoverflow.com/questions/18076013/setting-session-variable-using-javascript
          sessionStorage.SessionName = "SessionData";
          sessionStorage.setItem("SessionName",response.name);
          //console.log(response.name);
          //console.log("que hay en session?2");
          var usernameSession = sessionStorage.getItem("SessionName");
            //console.log(sessionStorage.getItem("SessionName"))
          //console.log(usernameSession)
          var texto = "Hola " + usernameSession + "!";
//          console.log(texto);
          $('#saludo').text(texto);

      });
    }

    var facebookLogin = function() {
      checkLoginState(function(data) {
        if (data.status !== 'connected') {
          FB.login(function(response) {
            if (response.status === 'connected')
              getFacebookData();
          }, {scope: scopes});
        }
        else
        {
          getFacebookData()
        }
      })
    }

    var facebookLogout = function() {
      checkLoginState(function(data) {
        if (data.status === 'connected') {
        FB.logout(function(response) {
            var menu = document.getElementById('menu-links');
            menu.innerHTML = loginMenu;

            $('#saludo').text("Inicio");

            var menu= document.getElementById('btn-central');
            menu.innerHTML = btn_central_login;

            var menu= document.getElementById('btn-abajo');
            menu.innerHTML = btn_abajo_login;

            //http://stackoverflow.com/questions/15804462/how-to-clear-localstorage-sessionstorage-and-cookies-in-javascript-and-then-ret
            sessionStorage.clear();
            console.log("fin")
          // $('#menulogueado').after(loginMenu);
          // $('#menulogueado').remove();



        })
      }
      })

    }

    $(document).on('click', '#comojugar2', function() {
  //      var usernameSession = sessionStorage.getItem("SessionName");
//        console.log(usernameSession)
        console.log("como jugar2")
        sessionStorage.setItem("parte","comojugar");
        post('/comojugar2', {});
    })




    $(document).on('click', '#comenzarJugar', function() {
        var usernameSession = sessionStorage.getItem("SessionName");
//        console.log(usernameSession)
        console.log("nav")
       post('/jugarPrimeraVez', {usuario: usernameSession});
    })

    $(document).on('click', '#btncentral-jugar', function() {
        var usernameSession = sessionStorage.getItem("SessionName");
//        console.log(usernameSession)
        console.log("central")
        post('/jugarPrimeraVez', {usuario: usernameSession});
    })

    $(document).on('click', '#btnabajo-jugar', function() {
        var usernameSession = sessionStorage.getItem("SessionName");
//        console.log(usernameSession)
        console.log("abajo")
        post('/jugarPrimeraVez', {usuario: usernameSession});
    })

    $(document).on('click', '#login-link', function(e) {
      e.preventDefault();
	 facebookLogin();
    })


    $(document).on('click', '#login-link1', function(e) {
        e.preventDefault();
        facebookLogin();
    })

    $(document).on('click', '#login-link2', function(e) {
        e.preventDefault();
        facebookLogin();
    })


    $(document).on('click', '#logout', function(e) {
      e.preventDefault();
      console.log($('#usuario').text());
      if (confirm("¿Está seguro?"))
        facebookLogout();
      else 
        return false;
    })

    $(document).on('click', '#logout2', function(e) {
        e.preventDefault();
        console.log($('#usuario').text());
        if (confirm("¿Está seguro?"))
        {
            facebookLogout();
            sessionStorage.clear();
            post('/login', {});
        }
        else
            return false;
    })

})
