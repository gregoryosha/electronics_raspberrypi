function print_out() {
  $.get("/printout");
  alert("printing!");
}

function sendMessage(message){
  $.get(`/digital/write/${message}`);
}

function led_on() {
  $.get("/digital/write/40/HIGH");
}

function led_off() {
  $.get("/digital/write/40/LOW");
}



window.addEventListener('keypress', (press)=>{
  console.log(press)
  if (press.key == 'ArrowRight') {
    sendMessage('40/HIGH');
  }
  else if (press.key == 'ArrowLeft') {
    sendMessage('38/HIGH');
  }
  // else if (press.key == 'd') {
  //   sendMessage('right');
  // }
  // else if (press.key == 's') {
  //   sendMessage('down');
  // }
})

window.addEventListener('keyup', (press)=>{
  if (press.key == 'ArrowRight') {
    sendMessage('40/LOW');
  }
  else if (press.key == 'ArrowLeft') {
    sendMessage('38/LOW');
  }
  // }
  // else if (press.key == 'a') {
  //   sendMessage('stop');
  // }
  // else if (press.key == 'd') {
  //   sendMessage('stop');
  // }
  // else if (press.key == 's') {
  //   sendMessage('stop');
  // }
})