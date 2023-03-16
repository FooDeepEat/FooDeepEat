// 필수 개인정보 제공 동의 라디오박스 동의하지 않을 경우 메시지 출력

const radio = document.getElementById("must_agree");

if (radio.checked) {
  alert("필수 개인정보 제공에 동의해 주세요.");
}


// 다음 API 이용해서 주소 가져오기
    
function execDaumPostcode(){
    new daum.Postcode({
        oncomplete: function(data){
            var fullAddr = data.roadAddress;
            var extraAddr = '';

            if(data.userSelectedType === 'R') {
                fullAddr = data.roadAddress;
            }// if(data.userSelectedType === 'R') end
            else fullAddr = data.jibunAddress;
            
            if(data.userSelectedType === 'R'){
                if (data.bname !== '') extraAddr += data.bname;
                if (data.buildingName !== '') extraAddr += (extraAddr !== ''?','+ data.buildingName: data.buildingName);
                fullAddr += (extraAddr !== ''? '('+extraAddr+')':'');
            }// if(data.userSelectedType === 'R') end

            document.getElementById('jusocode').value = data.zonecode;
            document.getElementById('juso1').value = fullAddr;
            document.getElementById('juso2').focus();
        }// oncomplete: function(data) end
    }).open(); // new daum.Postcode end
}// function daumPostCode() end


// 비밀번호 중복 체크
function checkPassword() {
    var password = document.getElementById("getuserpassword").value;
    var confirmPassword = document.getElementById("getuserpasswordcheck").value;
    var message = document.getElementById("message");
    
    if (password !== confirmPassword) {
      message.innerHTML = "비밀번호를 확인해 주세요.";
      message.style.color = "red";
    } else {
      message.innerHTML = "";
    }
    }

    
// 아이디 중복 여부 체크와 이메일 유효성 검사
function checkId() {
// HTML 요소에서 id 값을 가져옵니다.
var id = document.getElementById("useridcheck").value;

// 서버에서 id 중복 여부를 체크하고 결과를 받아옵니다.
// 이 예시에서는 서버와의 통신 대신에 로컬에서 간단하게 구현하였습니다.
// 만약 john@gmail.com을 입력하여 중복확인하는 경우 사용할 수 없다고 경고창이 뜹니다.
var isDuplicated = (id === "john@gmail.com");

// 이메일 유효성 검사를 수행합니다.
var email = document.getElementById("useridcheck").value;
var isEmailValid = /\S+@\S+\.\S+/.test(email);

// 결과를 바탕으로 메시지를 출력합니다.
var message;
if (isDuplicated) {
  message = "사용할 수 없는 아이디입니다.";
} else if (isEmailValid) {
  message = "사용 가능한 아이디입니다.";
} else {
  message = "이메일 주소가 올바르지 않습니다.";
}
alert(message);
}

// 사진 크기 검사하는 스크립트
function checkFileSize(input) {
    const fileSize = input.files[0].size;
    const maxSize = 5 * 1024 * 1024; // 5MB
  
    if (fileSize > maxSize) {
      alert("파일 크기는 5MB 이하여야 합니다.");
      input.value = "";
    }
  }

/* django에서 작성하는 코드
from django.core.exceptions import ValidationError

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024: # 5MB
        raise ValidationError("파일 크기는 5MB 이하여야 합니다.")*/
