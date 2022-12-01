function print_out() {
  $.get("/printout");
  alert("printing!");
}

function led_on() {
  $.get("/digital/write/40/HIGH");
  alert("LED! ON");
}

function led_off() {
  $.get("/digital/write/40/LOW");
  alert("LED! ON");
}