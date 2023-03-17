// 달력 선택 시 url 변경되는 코드
document.getElementById('currentDate').value = new Date().toISOString().substr(0, 10);
document.getElementById('currentDate').addEventListener('change', function() {
    var date = this.value;
    window.location.href = '/some/path?date=' + date;
});

// 오늘의 한 마디 입력 시 적용되는 코드
const commentInput = document.getElementById("comment");
const dateInput = document.getElementById("currentDate");

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