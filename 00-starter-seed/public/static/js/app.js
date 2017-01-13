$(document).ready(function() {
     var lock = new Auth0Lock(AUTH0_CLIENT_ID, AUTH0_DOMAIN, {
        auth: {
          redirectUrl: AUTH0_CALLBACK_URL
        }
     });

    $('.btn-login').click(function(e) {
      e.preventDefault();
      lock.show();
    });


    $('.btnjugar').click(function(e) {
        e.preventDefault();
        post('/jugarPrimeraVez', {});
    });

    $(document).on('click', '#comojugar2', function() {
        sessionStorage.setItem("parte","comojugar");
        post('/index', {});
    })

    $(document).on('click', '#sobre2', function() {
        sessionStorage.setItem("parte","sobre2");
        post('/index', {});
    })
    $(document).on('click', '#contact2', function() {
        sessionStorage.setItem("parte","contact2");
        post('/index', {});
    })

    $(document).on('click', '.btn-logout', function(e) {
        e.preventDefault();
        console.log("click en salir");
        if (confirm("¿Está seguro?"))
        {
            console.log("fin");
            sessionStorage.clear();
            post('/logout', {});
        }
        else
            return false;
    })

});
