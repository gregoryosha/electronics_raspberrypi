function print_out() {
  $.get("/printout");
  alert("printing!");
}

function sendMessage(message) {
  $.get(`/digital/write/${message}`);
}

function led_on() {
  $.get("/digital/write/40/HIGH");
}

function led_off() {
  $.get("/digital/write/40/LOW");
}

let pressed = {
  up: false,
  down: false,
  right: false,
  left: false
}

window.addEventListener('keydown', (press) => {
  if (press.key == 'ArrowUp' && !pressed.up) {
    console.log("Keydown:" + press.key);
    sendMessage('1/HIGH');
    pressed.up = true;
  }
  else if (press.key == 'ArrowDown' && !pressed.down) {
    sendMessage('2/HIGH');
    pressed.down = true;
  }
  else if (press.key == 'ArrowRight' && !pressed.right) {
    sendMessage('3/HIGH');
    pressed.right = true;
  }
  else if (press.key == 'ArrowLeft' && !pressed.left) {
    sendMessage('4/HIGH');
    pressed.left = true;
  }
})


window.addEventListener('keyup', (press) => {
  if (press.key == 'ArrowUp') {
    console.log("Keyup:" + press.key);
    sendMessage('1/LOW');
    pressed.up = false;
  }
  else if (press.key == 'ArrowDown') {
    sendMessage('2/LOW');
    pressed.down = false;
  }
  else if (press.key == 'ArrowRight') {
    sendMessage('3/LOW');
    pressed.right = false;
  }
  else if (press.key == 'ArrowLeft') {
    sendMessage('4/LOW');
    pressed.left = false;
  }
})


// Prevent scrolling on every click!

//super sweet vanilla JS delegated event handling!
// window.addEventListener("click", function (e) {
//   if (e.target && e.target.nodeName == "A") {
//     e.preventDefault();
//   }
// });

//window.addEventListener('touchmove', touchMoveHandler);
window.addEventListener('touchstart', touchStartHandler);
window.addEventListener('touchend', touchEndHandler);
window.addEventListener('touchmove', touchMoveHandler);

function touchStartHandler(event) {
  var direction = event.target.dataset.direction;
  console.log('Touch Start :: ' + direction)
  sendMessage(`${direction}/HIGH`);
}

function touchEndHandler(event) {
  var direction = event.target.dataset.direction;
  console.log('Touch End :: ' + direction)
  sendMessage(`${direction}/LOW`);
}

function touchMoveHandler(event) {
  // Set call preventDefault()
  event.preventDefault();
}

// Preventing selection
$(document).ready(function(){
  window.disableSelection();
});

$.fn.extend({
  disableSelection: function() {
      this.each(function() {
          this.onselectstart = function() {
              return false;
          };
          this.unselectable = "on";
          $(this).css('-moz-user-select', 'none');
          $(this).css('-webkit-user-select', 'none');
      });
      return this;
  }
});


