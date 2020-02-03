window.Superlits = {};
window.Superlits.initialize = function() {
    var inputbox = $('input[name="text"')
    inputbox.on('keypress', function(){
        $('.has-error').hide();
    });
    inputbox.on('click', function () {
        $('.has-error').hide();
    });
};