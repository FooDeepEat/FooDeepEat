const fileInput = document.getElementById('file-upload');
const previewContainer = document.querySelector('.preview-container');

fileInput.addEventListener('change', (event) => {
  previewContainer.innerHTML = '';

  if (event.target.files) {
    const filesAmount = event.target.files.length;

    for (let i = 0; i < filesAmount; i++) {
      const fileReader = new FileReader();
      const file = event.target.files[i];

      fileReader.readAsDataURL(file);

      fileReader.onload = (event) => {
        const divElement = document.createElement('li');
        divElement.classList.add('info_li');

        const imgElement = document.createElement('img');
        imgElement.setAttribute('src', event.target.result);
        imgElement.setAttribute('alt', file.name);

        const txtElement = document.createElement('p');
        txtElement.classList.add('info_img');
        txtElement.appendChild(imgElement);
        divElement.appendChild(txtElement);

        const nameElement = document.createElement('p');
        nameElement.classList.add('info_txt');
        nameElement.textContent = file.name;
        divElement.appendChild(nameElement);


        const del = document.createElement('a');
        del.classList.add('info_del');
        del.setAttribute('href', '#none');
        del.setAttribute('onclick', 'deleteInfo(this)');
        divElement.appendChild(del);

        previewContainer.appendChild(divElement);
      };
    }
  }
});


function deleteInfo(btn){
    const infoLi = btn.parentNode;
    infoLi.parentNode.removeChild(infoLi);
}




const previewImage = document.querySelector('.preview-container');
const imagePreview = document.querySelector('#showFood');


previewImage.addEventListener('click',function(event){
    const target = event.target;

    if(target.classList.contains('info_img')){
        const imgSrc = target.querySelector('img').src;
        showImage(imgSrc); 
    }else{             
        const imgSrc = target.src;
        let parentNode = target.parentNode
        while(parentNode && !imgSrc){
            if(parentNode.querySelector('img')){
                return false;
            }else{
                parentNode=parentNode.parentNode;
            }
        }      
        showImage(imgSrc);
    }
});

function showImage(imgSrc){    
    imagePreview.src=imgSrc;
    document.getElementById('showFood').src=imgSrc;
}