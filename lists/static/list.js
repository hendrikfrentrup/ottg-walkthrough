window.Superlists = {};

window.Superlists.updateItems = function(url) {
  $.get(url).done(function(response) {
    var rows = "";
    for (var i = 0; i < response.length; i++) {
      var item = response[i];
      rows += "\n<tr><td>" + (i + 1) + ": " + item.text + "</td></tr>";
    }
    $("#id_list_table").html(rows);
  });
};

window.Superlists.initialize = function(url) {
  var inputbox = $('input[name="text"]');

  inputbox.on("keypress", function() {
    $(".has-error").hide();
  });

  inputbox.on("click", function() {
    $(".has-error").hide();
  });

  if (url) {
    window.Superlists.updateItems(url);

    var form = $("#id_item_form");

    form.on("submit", function(event) {
      event.preventDefault();
      var text_input = form.find('input[name="text"]').val();
      $.post(url, {
        text: text_input,
        csrfmiddlewaretoken: form
          .find('input[name="csrfmiddlewaretoken"]')
          .val()
      })
        .done(function(response) {
          window.Superlists.updateItems(url);
        })
        .fail(function(response) {
          $(".has-error").show();
          try {
            if (response.responseJSON) {
              $(".help-block").text(response.responseJSON["error"]);
            }
          } catch (e) {
            console.log(e);
          }
        });
    });
  }
};
