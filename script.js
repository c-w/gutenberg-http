(function($) {

var KeyCode = {
  ENTER: 13
};

// from https://davidwalsh.name/javascript-debounce-function
function debounce(func, wait, immediate) {
  var timeout;
  return function() {
    var context = this, args = arguments;
    var later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};

function executeRequest(request, $responseNode) {
  $responseNode.removeClass('hidden error success');
  $responseNode.html('<div class="loader">Loading...</div>');

  $.getJSON(request)
  .done(function(response) {
    $responseNode.text(JSON.stringify(response, null, 2));
    $responseNode.addClass('success');
  })
  .fail(function(response) {
    var error = response.responseJSON;
    $responseNode.text(JSON.stringify(error, null, 2));
    $responseNode.addClass('error');
  });
}

$(document).ready(function() {
  $('.example .request').each(function() {
    var requestNode = this;
    var $requestNode = $(requestNode);
    var $responseNode = $($requestNode.data('target'));
    var request = requestNode.textContent.trim();
    $requestNode.keyup(debounce(function(ev) {
      var newRequest = requestNode.textContent.trim();
      var keycode = ev.keyCode || ev.which;
      if (keycode === KeyCode.ENTER || newRequest !== request) {
        executeRequest(newRequest, $responseNode);
        request = newRequest;
      }
    }, 250, true));
  });
});

}(jQuery))
