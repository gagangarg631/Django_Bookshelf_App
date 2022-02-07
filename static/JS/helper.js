let book_options_menu_html = `<div id="contextMenu" class="context-menu">
<ul>
    <li><a href="#">Element-1</a></li>
    <li><a href="#">Element-2</a></li>
    <li><a href="#">Element-3</a></li>
    <li><a href="#">Element-4</a></li>
    <li><a href="#">Element-5</a></li>
    <li><a href="#">Element-6</a></li>
    <li><a href="#">Element-7</a></li>
</ul>
</div>`

let spinner_html = `<div class="fac spinner" style="height: 100px;">
    <button class="btn btn-primary" type="button" disabled>
    <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
    Loading...
    </button>
</div>
`

export function htmlToDomElement(html){
    let temp = document.createElement('div');
    temp.insertAdjacentHTML('afterbegin',html);
    return temp.firstElementChild;
}

export function getSpinner(){
    return htmlToDomElement(spinner_html);
}

export function getBookOptionsMenu(){
    return htmlToDomElement(book_options_menu_html)
}

export function getCookie(_key){
    let cookies = document.cookie.split(';');
    for (let i = 0;i < cookies.length; i++){
        let ck = cookies[i];

        if (ck.substring(0, ck.indexOf('=')).trim() == _key){
            return ck.slice(ck.indexOf('=') + 1);
        }
    }
}