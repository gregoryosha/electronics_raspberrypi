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
window.addEventListener("click", function (e) {
  if (e.target && e.target.nodeName == "A") {
    e.preventDefault();
  }
});

window.addEventListener('touchmove', touchMoveHandler);

const pad_buttons = document.querySelectorAll('.control');
pad_buttons.forEach(item => {
  item.addEventListener('touchstart', touchStartHandler);
  item.addEventListener('touchend', touchEndHandler);
  item.addEventListener('touchmove', touchMoveHandler);
})

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

// let dpads = Array.prototype.slice.call(
//     document.getElementsByClassName("d-pad"),
//     0
//   ),
//   opads = Array.prototype.slice.call(
//     document.getElementsByClassName("o-pad"),
//     0
//   ),
//   els = dpads.concat(opads);
// function dir(dir) {
//   for (let i = 0; i < els.length; i++) {
//     const el = els[i],
//       d = el.className.indexOf("d-") !== -1,
//       what = d ? "d-pad" : "o-pad";
//     console.log(what);
//     el.className = what + " " + dir;
//   }
// }
// document.body.onkeyup = function (e) {
//   switch (e.which) {
//     case 37:
//       dir("left");
//       break;
//     case 39:
//       dir("right");
//       break;
//     case 38:
//       dir("up");
//       break;
//     case 40:
//       dir("down");
//       break;
//   }
// };
