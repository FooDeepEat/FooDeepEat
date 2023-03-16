// 404.html 10초 기다리면 main으로 넘어가는 스크립트
var count = 10;
var countdownElement = document.getElementById("countdown");

var countdownInterval = setInterval(function() {
  count--;
  countdownElement.textContent = count;

  if (count == 0) {
    clearInterval(countdownInterval);
    window.location.href = "main.html";
  }
}, 1000); // 1 second


