function checkFields(event) {
  const name = document.getElementsByName("name")[0].value;
  const birth_date = document.getElementsByName("birth_date")[0].value;
  const number = document.getElementsByName("number")[0].value;
  const email = document.getElementsByName("email")[0].value;

  if (name === "" || birth_date === "" || number === "" || email === "") {
    alert("회원정보를 모두 입력해주세요.");
    event.preventDefault(); // 폼 제출 방지
  }

  const birthDatePattern = /^\d{4}-\d{2}-\d{2}$/;
  if (!birthDatePattern.test(birth_date)) {
    alert("생년월일은 yyyy-mm-dd 형식으로 입력해주세요.");
    document.getElementsByName("birth_date")[0].value = ""; // 입력된 값 지우기
    event.preventDefault(); // 폼 제출 방지
  }

  const telPattern = /^\d{3}-\d{3,4}-\d{4}$/;
  if (!telPattern.test(number)) {
    alert("휴대폰 번호를 올바른 형식으로 입력해주세요.");
    document.getElementsByName("number")[0].value = ""; // 입력된 값 지우기
    event.preventDefault(); // 폼 제출 방지
  }

  const emailPattern = /^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  if (!emailPattern.test(email)) {
    alert("이메일을 올바른 형식으로 입력해주세요.");
    document.getElementsByName("email")[0].value = ""; // 입력된 값 지우기
    event.preventDefault(); // 폼 제출 방지
  }
}


// 생년월일 입력
function addHyphenBirth(element) {
  let ele = element.value.split('-').join('');    // '-' 제거
  if (ele.length > 4) {
    ele = ele.substring(0, 4) + '-' + ele.substring(4);
  }
  if (ele.length > 7) {
    ele = ele.substring(0, 7) + '-' + ele.substring(7);
  }
  element.value = ele;
}


// 휴대폰번호 입력
function addHyphenTel(element) {
  let ele = element.value.split('-').join('');    // '-' 제거
  if (ele.length > 3) {
  ele = ele.substring(0, 3) + '-' + ele.substring(3);
  }
  if (ele.length > 8) {
  ele = ele.substring(0, 8) + '-' + ele.substring(8);
  }
  element.value = ele;
  }

  // 이거는... 인증번호 6자리 코드
const verificationCodeInput = document.querySelector('#verification-code');

verificationCodeInput.addEventListener('blur', (event) => {
  const value = verificationCodeInput.value;

  if (value.length !== 6 || isNaN(value)) {
    alert('숫자 6자리를 입력하세요.');
    document.getElementsByName("verification_code")[0].value = ""; // 입력된 값 지우기
    event.preventDefault(); // 폼 제출 방지
    return false; // 추가
  }
  return true; // 추가
});


// 이건 인증번호 확인 로직... 이걸 해야 인증번호 버튼이 바뀜
function showVerification() {
  document.getElementById("btn-wrap").style.display = "none";
  document.getElementById("verification-container").style.display = "block";
}
  
  