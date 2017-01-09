
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

var loginMenu = '<div class="masthead clearfix">' +
               ' <div class="inner" id="menulogin">'+
          '<h3 class="masthead-brand">Tesis</h3>' +

          '<nav>' +
            '<ul class="nav masthead-nav">' +
              '<li class="active"><a href="#" id="login" class="menu__link">Iniciar sesión con facebook</a></li>' +
              '<li><a href="#">Algo mas?</a></li>' +
              '<li><a href="#">Contact</a></li>' +
            '</ul>' +
          '</nav>' +
        '</div>' +
      '</div>'

// var div_session3 = '<div class="inner" id="menulogueado">' +
//           '<h3 class="masthead-brand" id="daleBienvenida" >Tesis</h3>' +
//           '<nav>' +
//             '<ul class="nav masthead-nav">' +
//               '<li class="active"><a href="#" id="comenzarJugar"> Comenzar!</a></li>' +
//               '<li><a href="#">Contact</a></li>' +
//               '<li><a href="#" id="logout">Cerrar sesión</a></li>' +
//             '</ul>' +
//           '</nav>' +
//         '</div>' +
//       '</div>'

var div_session3 = '<li class="active" id="comenzarJugar"><a href="#">Jugar</a></li>' +
        '<li><a href="#">Algo m&aacute;s?</a></li>' +
        '<li><a href="#">Contacto</a></li>' +
        '<li><a href="#" id="logout">Cerrar sesión</a></li>';

  var btn_jugar =  '<a href="" id="btncentral-jugar" class="btn btn-primary btn-xl page-scroll login">Jugar!</a>';

var btn_jugar2 =  '<a href="" id="btnabajo-jugar" class="btn btn-default btn-xl sr-button login">Jugar!</a>'


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

          sessionStorage.SessionName = "SessionData";
          sessionStorage.setItem("SessionName",response.name);
          //console.log(response.name);
          //console.log("que hay en session?2");
          var usernameSession = sessionStorage.getItem("SessionName");
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
            menu.innerHTML = menuOriginal;

          // $('#menulogueado').after(loginMenu);
          // $('#menulogueado').remove();
           post('/login', {});

        })
      }
      })

    }
    $(document).on('click', '#comenzarJugar', function() {
        var usernameSession = sessionStorage.getItem("SessionName");
//        console.log(usernameSession)

        //      user = $('#usuario').text()
       post('/jugarPrimeraVez', {usuario: usernameSession});
//       console.log("primera vez")

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

})
