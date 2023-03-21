function checkFields(event) {
    const name = document.getElementsByName("name")[0].value;
    const birth_date = document.getElementsByName("birth_date")[0].value;
    const email = document.getElementsByName("email")[0].value;
  
    if (name === "" || birth_date === "" || email === "") {
      alert("이름, 생년월일, 이메일을 모두 입력해주세요.");
      event.preventDefault(); // 폼 제출 방지
    }
  
    const pattern = /^\d{4}-\d{2}-\d{2}$/;
    if (!pattern.test(birth_date)) {
      alert("생년월일은 yyyy-mm-dd 형식으로 입력해주세요.");
      document.getElementsByName("birth_date")[0].value = ""; // 입력된 값 지우기
      event.preventDefault();
    }
}

function addHyphen(element) {
  let ele = element.value.split('-').join('');    // '-' 제거
  if (ele.length > 4) {
    ele = ele.substring(0, 4) + '-' + ele.substring(4);
  }
  if (ele.length > 7) {
    ele = ele.substring(0, 7) + '-' + ele.substring(7);
  }
  element.value = ele;
}

