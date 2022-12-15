function print_out() {
  $.get("/printout");
  alert("printing!");
}

function sendMessage(message) {
  if(message =='up'){
    message = '1/HIGH';
  }
  else if(message = 'down') {
    message = '2/HIGH';
  }
  else if(message = 'right') {
    message = '3/HIGH';
  }
  else if(message = 'left') {
    message = '4/HIGH'
  }
  $.get(`/digital/write/${message}`);
}

let pressed = {
  up:false,
  down:false,
  right:false,
  left:false
}

//Arrow key up and down events
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

/*
//on click functionality
document.body.addEventListener("click", function (e) {
  if (e.target && e.target.nodeName == "A") {
    e.preventDefault();
  }
});

function touchStartHandler(event) {
  var direction = event.target.dataset.direction;
  console.log('Touch Start :: ' + direction)
  sendMessage(direction);
}

function touchEndHandler(event) {
  var direction = event.target.dataset.direction;
  console.log('Touch End :: ' + direction)
  sendMessage('1/LOW');
}


document.querySelectorAll('.control').forEach(item => {
  item.addEventListener('touchstart', touchStartHandler);
  
})

document.querySelectorAll('.control').forEach(item => {
  item.addEventListener('touchend', touchEndHandler)
})

*/
