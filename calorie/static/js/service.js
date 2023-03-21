function previewImage(input){
    if(input.files && input.files[0]){
        var reader = new FileReader();
        reader.onload = function(e){
            document.getElementById("showFood").src = e.target.result;
        };
        reader.readAsDataURL(input.files[0]);
    } else{
        document.getElementById('showFood').src="";
    }
}

const inputElement = document.getElementById("file-upload")
const previewElement = document.getElementById("showFood")

inputElement.addEventListener("change", (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onloadend = () => {
        previewElement.src = reader.result;
    };

    if (file){
        reader.readAsDataURL(file);
    } else {
        previewElement.src = "#";
    }
});


function toggleInputField(){
	const inputField = document.getElementById("inputField");
	const confirmButton = document.getElementById("confirmButton");
	const editButton = document.getElementById("editButton");
    const inputElement = document.getElementById('inputField');
            inputElement.addEventListener('input', function() {
            this.value = this.value.replace(/[^0-9]/g, ''); // 숫자가 아닌 것은 제거
});
	if (inputField.readOnly){
		// 입력창을 수정 가능하게
		inputField.readOnly = false;
		editButton.style.display="";
		confirmButton.style.display="none";
		inputField.focus();
	}else {
		// 입력창을 readonly로
		inputField.readOnly = true;
		editButton.style.display = "none";
		confirmButton.style.display = "";
	}
}

// 

function foodInfo() {
    let 부대찌개 = {foodname:'부대찌개',kcal:156,carbonhydrates:'11.1g',protein:'7g',fat:'9.5g'}
    let 호박죽 = {foodname:'호박죽',kcal:70,carbonhydrates:'15g',protein:'1.5g',fat:'1g'}
    let foods = [부대찌개, 호박죽];

    let foodsMapped = foods.map(food => ({
      foodname: food.foodname,
      kcal: food.kcal,
      carbonhydrates: food.carbonhydrates,
      protein: food.protein,
      fat: food.fat
    }));

    return foodsMapped;
  }

  function printFoodInfo() {
    let foodsMapped = foodInfo();
    let 부대찌개Info = foodsMapped.find(food => food.foodname === '부대찌개');

    alert(`음식명: ${부대찌개Info.foodname}\n열량: ${부대찌개Info.kcal}\n탄수화물: ${부대찌개Info.carbonhydrates}\n단백질: ${부대찌개Info.protein}\n지방: ${부대찌개Info.fat}`);
  }

