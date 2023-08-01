document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    xhr.onload = function() {
        console.log(xhr.responseText);
    }
    xhr.send(formData)
})