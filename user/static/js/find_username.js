function checkName() {
  var nameInput = document.getElementsByName("name")[0];
  var nameMessage = document.getElementById("name-message");

  if (nameInput.value == "") {
    nameMessage.innerHTML = "이름을 입력해주세요.";
    nameMessage.style.color = "red";
    nameMessage.style.fontSize = "12px";
    nameInput.style.borderColor = "red";
    nameInput.style.fontSize = "12px";
  } else {
    nameMessage.innerHTML = "";
    nameInput.style.borderColor = "";
    nameInput.style.fontSize = "";
  }
}

function checkBirthday() {
  var birthInput = document.getElementsByName("birth_date")[0];
  var birthMessage = document.getElementById("birth-message");

  if (birthInput.value == "") {
    birthMessage.innerHTML = "생년월일을 입력해주세요.";
    birthMessage.style.color = "red";
    birthMessage.style.fontSize = "12px";
    birthInput.style.borderColor = "red";
    birthInput.style.fontSize = "12px";
  } else {
    birthMessage.innerHTML = "";
    birthInput.style.borderColor = "";
    birthInput.style.fontSize = "";
  }
}

function checkTel() {
  var telInput = document.getElementsByName("number")[0];
  var telMessage = document.getElementById("tel-message");

  if (telInput.value == "") {
    telMessage.innerHTML = "휴대폰 번호를 입력해주세요.";
    telMessage.style.color = "red";
    telMessage.style.fontSize = "12px";
    telInput.style.borderColor = "red";
    telInput.style.fontSize = "12px";
  } else {
    telMessage.innerHTML = "";
    telInput.style.borderColor = "";
    telInput.style.fontSize = "";
  }
}

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
  