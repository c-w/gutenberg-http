(function($) {

var KeyCode = {
  ENTER: 13
};

var Server = window.location.search.substr(1).match(/server=([^&]*)/);
Server = Server ? decodeURIComponent(Server[1]) : 'https://gutenberg.justamouse.com';

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
  $responseNode.removeClass('hidden');

  var $responseDisplay = $responseNode.find('pre');
  $responseDisplay.removeClass('error success');
  $responseDisplay.html('<div class="loader">Loading...</div>');

  $.getJSON(Server + request)
  .done(function(response) {
    $responseDisplay.text(JSON.stringify(response, null, 2));
    $responseDisplay.addClass('success');
  })
  .fail(function(response) {
    var error = response.responseJSON;
    $responseDisplay.text(JSON.stringify(error, null, 2));
    $responseDisplay.addClass('error');
  });
}

$(document).ready(function() {
  $('.example .request').each(function() {
    var requestNode = this;
    var $requestNode = $(requestNode);
    var $responseNode = $($requestNode.data('target'));
    var request = requestNode.textContent.trim();
    $requestNode.bind('keyup click', debounce(function(ev) {
      var newRequest = requestNode.textContent.trim();
      var isChange = newRequest !== request;
      var isEnter = (ev.keyCode || ev.which) === KeyCode.ENTER;
      var isClick = ev.type === 'click' && !$responseNode.data('clickToggled');
      if (isChange || isEnter || isClick) {
        executeRequest(newRequest, $responseNode);
        request = newRequest;
        $responseNode.data('clickToggled', true);
      }
    }, 250, true));
  });

  $('.close').click(function() {
    var $close = $(this);
    var $container = $close.closest('.response-container')
    $container.addClass('hidden');
    $container.data('clickToggled', false);
  });

  var $tooltips = $('pre[contenteditable]');
  $tooltips.tooltipster({
    content: 'Edit me!',
    theme: 'tooltipster-punk',
    trigger: 'custom'
  });
  $tooltips.tooltipster('show');
  $tooltips.on('mouseenter focus', function() {
    $(this).tooltipster('hide');
  });
  $tooltips.on('click', function() {
    $tooltips.tooltipster('hide');
  });
});

}(jQuery))
