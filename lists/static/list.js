window.Superlists = {};

window.Superlists.updateItems = function(url) {
  $.get(url).done(function(response) {
    var rows = "";
    for (var i = 0; i < response.items.length; i++) {
      var item = response.items[i];
      rows += "\n<tr><td>" + (i + 1) + ": " + item.text + "</td></tr>";
    }
    $("#id_list_table").html(rows);
  });
};

window.Superlists.initialize = function(params) {
  var inputbox = $('input[name="text"]');

  inputbox.on("keypress", function() {
    $(".has-error").hide();
  });

  inputbox.on("click", function() {
    $(".has-error").hide();
  });

  if (params) {
    window.Superlists.updateItems(params.listApiUrl);

    var form = $("#id_item_form");

    form.on("submit", function(event) {
      event.preventDefault();

      var text_input = form.find('input[name="text"]').val();

      $.post(params.itemsApiUrl, {
        list: params.listId,
        text: text_input,
        csrfmiddlewaretoken: form
          .find('input[name="csrfmiddlewaretoken"]')
          .val()
      })
        .done(function() {
          $(".has-error").hide();
          window.Superlists.updateItems(params.listApiUrl);
        })
        .fail(function(response) {
          $(".has-error").show();
          try {
            if (response.responseJSON && response.responseJSON.non_field_errors) {
              $(".help-block").text(response.responseJSON.non_field_errors[0]);
            }
          } catch (e) {
            console.log(e);
          }
        });
    });
  }
};
