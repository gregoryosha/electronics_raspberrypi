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


window.addEventListener('keydown', (press) => {
  if (press.key == 'ArrowUp') {
    sendMessage('1/HIGH');
  }
  else if (press.key == 'ArrowDown') {
    sendMessage('2/HIGH');
  }
  else if (press.key == 'ArrowRight') {
    sendMessage('3/HIGH');
  }
  else if (press.key == 'ArrowLeft') {
    sendMessage('4/HIGH');
  }
})


window.addEventListener('keyup', (press) => {
  if (press.key == 'ArrowUp') {
    sendMessage('1/LOW');
  }
  else if (press.key == 'ArrowDown') {
    sendMessage('2/LOW');
  }
  else if (press.key == 'ArrowRight') {
    sendMessage('3/LOW');
  }
  else if (press.key == 'ArrowLeft') {
    sendMessage('4/LOW');
  }
})