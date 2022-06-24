let tagField = document.getElementById('_tags');

let added_tags = document.querySelector('.added_tags');
let hiddenField = document.getElementById('_hiddenTagField');

let form = document.getElementById('addBookForm');


tagField.addEventListener('input',function(ev){
    if (ev.data == " " && tagField.value.trim().length > 0){
        added_tags.style.visibility = 'visible'
        _p = document.createElement('p')
        _p.addEventListener('click',function(){
            l = hiddenField.value.split(" ")
            console.log(l," ",l.indexOf(this.innerText.toString()));
            l.splice(l.indexOf(this.innerText.toString()),1);
            this.remove()
            hiddenField.value = l.join(" ")
        })
        _p.innerText = tagField.value
        added_tags.appendChild(_p)
        hiddenField.value += tagField.value
        tagField.value = ""
    }
})

form.addEventListener('submit',function(){

    if (tagField.value.trim().length > 0)
        hiddenField.value += tagField.value.trim();
    
    if (hiddenField.value.trim().length == 0)
        hiddenField.value = 'others'
    
})
