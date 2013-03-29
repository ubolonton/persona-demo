var demo = demo || {};

$.extend(demo, {
  log: function(tag, data) {
    console.log(tag + "  ========================================");
    console.log(data);
  },

  setUp: function(email) {
    navigator.id.watch({
      loggedInUser: email ? email : null,

      onlogin: function(assertion) {
        $.ajax({
          type: "POST",
          url: "/auth/login",
          data: {assertion: assertion},
          success: function(response, status, xhr) {
            demo.log("Login ok", response);
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
          url: "/auth/logout",

          success: function(response, status, xhr) {
            demo.log("Logout ok", response);
          },

          error: function(xhr, status, err) {
            demo.log("Logout error", err);
          }
        });
      }
    });
  }
});
