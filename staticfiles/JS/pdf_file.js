window.addEventListener('beforeunload', function (e) {
    // e.preventDefault()
    console.log(e)
    bookUrl = e.srcElement.documentURI;

    let form = document.getElementById("myform");

    this.document.getElementById('bookUrlField').value = bookUrl.toString();

    const formData = new FormData(form);
    fetch('/books/pdf-closed/', {
        method: 'post',
        body: formData
    })
    .then(function(res){
        return res.text();
    }).then(function(t){
        console.log(t);
        window.location.href('/')
    })
    
    // e.returnValue = ""
});

