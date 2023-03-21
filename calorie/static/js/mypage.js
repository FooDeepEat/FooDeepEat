// pie-chart
var canvas = document.getElementById("pie-canvas");
var ctx = canvas.getContext("2d");
var centerX = canvas.width / 2;
var centerY = canvas.height / 2;
var radius = 80;
var startAngle = 0;
var endAngle = 2 * Math.PI;
var colors = ["#ff6384", "#36a2eb", "#ffce56"];
var data = [60, 30, 10];
var total = data.reduce(function(sum, value) {
    return sum + value;
}, 0);
var angles = data.map(function(value) {
    return (value / total) * 2 * Math.PI;
});

function drawPieChart() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    data[0] = parseInt(document.getElementById("pie-carb").value);
    data[1] = parseInt(document.getElementById("pie-protein").value);
    data[2] = parseInt(document.getElementById("pie-fat").value);
    total = data.reduce(function(sum, value) {
        return sum + value;
    }, 0);
    angles = data.map(function(value) {
        return (value / total) * 2 * Math.PI;
    });

    for (var i = 0; i < angles.length; i++) {
        endAngle = startAngle + angles[i];
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.fillStyle = colors[i];
        ctx.fill();
        startAngle = endAngle;
    }
}
drawPieChart();
document.getElementById("pie-carb").addEventListener("input", drawPieChart);
document.getElementById("pie-protein").addEventListener("input", drawPieChart);
document.getElementById("pie-fat").addEventListener("input", drawPieChart);

// 오늘의 한 마디 입력 시 적용되는 코드
const commentInput = document.getElementById("comment");
const dateInput = document.getElementById("currentDate");


// 달력 선택 시 url 변경되는 코드
document.getElementById('currentDate').value = new Date().toISOString().substr(0, 11);
document.getElementById('currentDate').addEventListener('change', function() {
    var date = this.value;
    window.location.href = '/some/path?date=' + date;
});

// 사용자가 날짜를 선택하면 해당 날짜에 저장된 정보를 가져옵니다.
dateInput.addEventListener("change", () => {
const selectedDate = dateInput.value;
// 서버로 데이터를 전송하는 코드를 작성합니다.
// 이 코드는 AJAX 또는 fetch API를 사용하여 구현할 수 있습니다.
fetch(`http://your-server-url.com/get-data?date=${selectedDate}`)
    .then(response => response.text())
    .then(data => commentInput.value = data)
    .catch(error => console.error(error));
});