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

            document.getElementById('id_postal_code').value = data.zonecode;
            document.getElementById('id_city').value = fullAddr;
            document.getElementById('id_address').focus();
        }// oncomplete: function(data) end
    }).open(); // new daum.Postcode end
}// function daumPostCode() end
