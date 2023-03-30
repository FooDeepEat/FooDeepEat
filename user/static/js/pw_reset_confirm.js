function checkPassword() {
    var passwordInput1 = document.getElementById("new_password1");
    var passwordInput2 = document.getElementById("new_password2");
    var passwordMessage = document.getElementById("password-message");
    var matchMessage = document.getElementById("password-match-message");
    var submitButton = document.querySelector(".submit_new_pw");
    var regex = /^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$/;

    // 8~12자리 영문과 숫자 조합
    
    // Check if password matches the regex
    if (regex.test(passwordInput1.value)) {
      passwordMessage.innerHTML = "비밀번호 조건 ㅇㅋㅇㅋ 통과";
      passwordMessage.style.color = "blue";
      
      // Check if passwords match
      if (passwordInput1.value === passwordInput2.value) {
        matchMessage.innerHTML = "ㅇㅋㅇㅋ 비번 일치함";
        matchMessage.style.color = "blue";
        submitButton.disabled = false;
      } else {
        matchMessage.innerHTML = "비번 다름;";
        matchMessage.style.color = "red";
        submitButton.disabled = true;
      }
    } else {
      passwordMessage.innerHTML =
        "영문, 숫자, 특수문자로 이루어진 8~12자리의 비밀번호를 설정하십시오.";
      passwordMessage.style.color = "red";
      passwordInput1.style.borderColor = "red";
      submitButton.disabled = true;
    }
}