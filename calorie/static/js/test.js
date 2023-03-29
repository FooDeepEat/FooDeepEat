function previewImages(input) {
    var previewContainer = document.querySelector('.preview-container');
    previewContainer.innerHTML = '';
    if (input.files) {
        var filesAmount = input.files.length;
        for (var i = 0; i < filesAmount; i++) {
            var reader = new FileReader();
            reader.onload = function(event) {
                var img = document.createElement('img');
                img.setAttribute('src', event.target.result);
                previewContainer.appendChild(img);
            }
            reader.readAsDataURL(input.files[i]);
        }
    }
}

var dropArea = document.querySelector('.foodbox');

dropArea.addEventListener('dragover', function(e) {
    e.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', function(e) {
    e.preventDefault();
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', function(e) {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    var files = e.dataTransfer.files;
    var input = document.querySelector('#file-upload');
    input.files = files;
    previewImages(input);
});
