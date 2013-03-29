var demo = demo || {};

$.extend(demo, {
  log: function(tag, data) {
    console.log(tag + "  ========================================");
    console.log(data);
  },

  setUp: function(baseUrl, email) {
    navigator.id.watch({
      loggedInUser: email ? email : null,

      onlogin: function(assertion) {
        $.ajax({
          type: "POST",
          url: baseUrl + "/auth/login",
          data: {assertion: assertion},
          success: function(response, status, xhr) {
            if (response.error) {
              alert(response.error);
            } else {
              demo.log("Login ok", response);
              window.location.reload();
            }
          },
          error: function(xhr, status, err) {
            navigator.id.logout();
            demo.log("Login error", err);
          }
        });
      },

      onlogout: function() {
        $.ajax({
          type: "POST",
          url: baseUrl + "/auth/logout",

          success: function(response, status, xhr) {
            if (response.error) {
              alert(response.error);
            } else {
              demo.log("Logout ok", response);
              window.location.reload();
            }
          },

          error: function(xhr, status, err) {
            demo.log("Logout error", err);
          }
        });
      }
    });
  }
});

$(function() {
  $("button#persona-login").click(function() {
    navigator.id.request();
  });

  $("button#persona-logout").click(function() {
    navigator.id.logout();
  });
});
