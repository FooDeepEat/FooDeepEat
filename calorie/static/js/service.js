
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
        divElement.appendChild(del);



        previewContainer.appendChild(divElement);
      };
    }
  }
});


const infoDelBtn = document.querySelectorAll('.info_del');

for(let i=0; i<infoDelBtn.length; i++) {
  infoDelBtn[i].addEventListener('click', function() {
    const infoLi = this.parentNode;
    infoLi.parentNode.removeChild(infoLi);
  });
}
