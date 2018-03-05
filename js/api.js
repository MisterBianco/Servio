var file = "";
var magicNum =  41943040;
var filetable = document.querySelector("#filetable");

function readBlob(filesize) {
    var reader = new FileReader();

    reader.onload = function(e) {
        fetch('http://localhost:8080/api/files', { // Your POST endpoint
            method: 'POST',
            mode: "cors",
            headers: {"Filename": file['name']},
            body: e.currentTarget.result
        })
        .then(response => response.json())
        .then(function(success) {
            getfiles();
            // Call to get all files and display to dom
        })
        .catch(error => console.log(error)
    )};

    var blob = file.slice(0, filesize);
    reader.readAsBinaryString(blob);

}

function requestfile(filename) {
    fetch('http://127.0.0.1:8080/files', { // Your POST endpoint
        method: 'GET',
        mode: "cors",
        headers: {
            "Filename": filename,
        },
    })
    .then(function(resp) {
        return resp.blob();
    })
    .then(function(blob) {
        download(blob, filename);
    });
}

function getfiles() {

    $("#filetable tr").remove();

    fetch('http://127.0.0.1:8080/api/files', { // Your POST endpoint
        method: 'GET',
        mode: "cors",
        headers: {},
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(json) {
        console.log(json);
        for (var filename in json) {
            console.log("Filename="+filename);

            var row = filetable.insertRow(filetable.rows.length);

            var cell1 = row.insertCell(0);
            var cell2 = row.insertCell(1);
            var cell3 = row.insertCell(2);
            var cell4 = row.insertCell(3);

            cell1.innerHTML = json[filename]['filename'];
            cell2.innerHTML = json[filename]['filesize']+"b";
            cell3.innerHTML = "<button type='button' class='btn btn-outline-primary' onclick='downloadrow(this)'>Download</button>";
            cell4.innerHTML = "<button type='button' class='btn btn-outline-danger' onclick='deleterow(this)'>Delete</button>";
        }
    });
}

function downloadrow(el) {
    var n = el.parentNode.parentNode.cells[0].textContent;
    fetch('http://127.0.0.1:8080/api/files', { // Your POST endpoint
        method: 'GET',
        mode: "cors",
        headers: {
            "Filename": n,
        },
    })
    .then(function(resp) {
        return resp.blob();
    })
    .then(function(blob) {
        download(blob, n);
    });
}

function deleterow(el) {
    var n = el.parentNode.parentNode.cells[0].textContent;

    fetch('http://127.0.0.1:8080/api/files', { // Your POST endpoint
        method: 'DELETE',
        mode: "cors",
        headers: {
            "Filename": n,
        },
    })
    .then(function(resp) {
        return resp.json();
    })
    .then(function(json) {
        console.log("TEST");
        getfiles();
    });
}

getfiles();

document.querySelector('#uploadbutton').addEventListener('click', function(evt) {
    var files = document.getElementById('files').files;
    if (!files.length) {
        alert('Please select a file!');
        return;
    }

    file = files[0];
    document.querySelector('#files').value = "";
    readBlob(file.size);
});

document.querySelector('#files').addEventListener('change', function(evt) {
    var files = document.getElementById('files').files;
    file = files[0];
    if (file.size >  magicNum) {  // 1MB
        alert('File upload limit exceeded.');
        evt.target.value = "";
        return;
    }
    getfiles();
});
