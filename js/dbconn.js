var magicNum =  41943040;
var file = "";

function readBlob(filesize) {
    var reader = new FileReader();

    reader.onload = function(e) {

    fetch('http://127.0.0.1:8080/files', { // Your POST endpoint
        method: 'POST',
        mode: "cors",
        headers: {"Filename": file['name']},
        body: e.currentTarget.result
    })
    .then(response => response.json())
    .then(function(success) {
        alert("File ID: "+success);
        document.querySelector("#fileid").innerHTML = success;
    })
    .catch(error => console.log(error)
    )};

    var blob = file.slice(0, filesize);
    reader.readAsBinaryString(blob);
}

document.querySelector('#files').addEventListener('change', function(evt) {
    var files = document.getElementById('files').files;
    file = files[0];
    if (file.size >  magicNum) {  // 1MB
        alert('File upload limit exceeded.');
        evt.target.value = "";
        return;
    }
});

document.querySelector('#uploadbutton').addEventListener('click', function(evt) {
    var files = document.getElementById('files').files;
    if (!files.length) {
        alert('Please select a file!');
        return;
    }

    file = files[0];
    readBlob(file.size);
});


function requestfile(fileid) {
    fetch('http://127.0.0.1:8080/files', { // Your POST endpoint
        method: 'GET',
        mode: "cors",
        headers: {
            "Filename": fileid,
        },
    })
    .then(function(resp) {
        return resp.blob();
    })
    .then(function(blob) {
        download(blob, document.querySelector("#saveasinput").value);
    });
}

document.querySelector('#downloadbutton').addEventListener('click', function(evt) {
    var fileid = document.getElementById('fileidentifier').value;
    if (!fileid) {
        alert('Please enter a file code!');
        return;
    }

    requestfile(fileid);
});
