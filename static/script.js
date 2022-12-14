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
  up:false,
  down:false,
  right:false,
  left:false
}

window.addEventListener('keydown', (press) => {
  if (press.key == 'ArrowUp' && !pressed.up) {
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


