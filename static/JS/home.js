import { getSpinner, getBookOptionsMenu, htmlToDomElement, getCookie } from './helper.js'
import * as util from './util.js'

let tags,tags_str;
let index = 0;

let selected_books = [];
let selection_enabled = false;

let select_books_options = Array.from(document.querySelectorAll('.select-books-options'));
let selected_books_count_text = document.getElementById('select-books-count-text');



// Get tags from server as cookies
let ck = document.cookie;

tags_str = ck.slice(ck.indexOf('tags='),ck.indexOf(';',ck.indexOf('tags=')))
tags = tags_str.split('=')[1].slice(3,-2).split("'\\054 '")
tags = tags.filter(el => el.trim().length > 0);
let default_categories = ['recent_books', 'fav_books']
tags = default_categories.concat(tags)


// switch all books select buttons to current select buttons state (hidden or visible)
const selectButtonsToCurrentState = function(iterable_items){
    let item_list = Array.from(iterable_items)
    if (selection_enabled){
        iterable_items.forEach(item => {
            item.style.backgroundColor = util.select_box_uncheck_color;
            item.style.visibility = 'visible';
        })
    }else{
        iterable_items.forEach(item => {
            item.style.backgroundColor = util.select_box_uncheck_color;
            item.style.visibility = 'hidden'
        })
    }
}

// change color of select button of all books (blue or gray)
const changeSelectButtonValue = function(head_element, _color, _id){
    let items_list = Array.from(head_element.querySelectorAll(`input[value ='${_id}'] ~ .book-select`));
    items_list.forEach(item => {
        item.style.backgroundColor = _color;
    })
}

// code to make carousel first slide active
function setFirstCarouselActive(item){
    item.firstElementChild.classList.add("active");
}


function loadNext(obs){
    if (index < tags.length){
        let _tag = tags[index].replace(/[^A-Za-z_]/g,"")
        loadBooksForTag(obs,_tag);
        index++;
    }
}


// load books with specified tag using ajax
function loadBooksForTag(observer,tag){
    let spinner = getSpinner();

    let rows_container = document.getElementById("bookshelf-rows-box");
    let xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let res = htmlToDomElement(this.response);
            let no_books = res.querySelector("input[name='no-books']");

            if (no_books){
                if (index < tags.length){
                    loadNext(observer)
                }else{
                    rows_container.appendChild(res);
                }
            }else{
                let row_el = res;
                setFirstCarouselActive(row_el.querySelector('.carousel-inner'));
                
                observer.disconnect();
                observer.observe(row_el);
                rows_container.appendChild(row_el);
                
                selectButtonsToCurrentState(row_el.querySelectorAll('.select-box'));
                selected_books.forEach(bk_id => {
                    changeSelectButtonValue(row_el, util.select_box_checked_color, bk_id);
                })
            }

            if (this.response == "NIL"){
                loadNext(observer);
            }else{
                
            }
            spinner.remove();

        }
    };
    xhr.open("GET", `${tag}`, true);       
    xhr.send();

    rows_container.appendChild(spinner);
}


function startIntersectionObserver(){
    let options = {
        root: null,
        rootMargin: '0px',
        threshold: 1.0
    }
    
    let observer = new IntersectionObserver(function(entries,observer){

        if (entries[0].isIntersecting && index < tags.length){
            loadNext(this);
        }
    }, options);

    // let target = document.querySelector('.row-border');
    // observer.observe(target);
    loadNext(observer);
}

startIntersectionObserver();


Array.from(document.querySelectorAll('.carousel-inner')).forEach(item => setFirstCarouselActive(item));

let carouselNum = 0

Array.from(document.querySelectorAll('.carousel')).forEach(cc => {
    carouselNum++;
    let _id = `carouselExampleControls${carouselNum}`
    cc.setAttribute('id',_id)
    Array.from(cc.getElementsByTagName('button')).forEach(btn => {
        btn.setAttribute('data-bs-target','#' + _id)
    })
})


// reload page when user switch from other browser tab to this web tab
document.addEventListener("visibilitychange", function() {
    // if (document.visibilityState === 'visible') {
    //     this.location.reload();
    // }
  });


// mouse hover on book card
function MouseOnBookCard(el,ev){
    let card_options = Array.from(el.querySelectorAll('.book-card-options'));
    card_options.forEach(item => {
        
        if (ev.type == 'mouseenter'){
            item.style.visibility = 'visible';
        }else if (ev.type == 'mouseleave'){
            item.style.visibility = 'hidden';
        }
    })
}

window.MouseOnBookCard = MouseOnBookCard;


// show menu (options) for book on right click 
function RightClickBookCard(ev){
    ev.preventDefault();



    // let row_content_last = document.querySelector('.book-row-content');
    // let options_menu = getBookOptionsMenu();

    // // options_menu.style.top = ev.offsetY;
    // row_content_last.appendChild(options_menu);
    // console.log(options_menu.style-position);

    // console.log(ev);
}

window.RightClickBookCard = RightClickBookCard;



function toggleSelectBook(ev,book_id){
    let bg = ev.target.style.backgroundColor;
    let _color = null;
    if (bg != util.select_box_checked_color){
        selected_books.push(book_id);
        changeSelectButtonValue(document, util.select_box_checked_color, book_id);
        selected_books_count_text.innerText = selected_books.length;
    }
    else{
        selected_books.splice(selected_books.indexOf(book_id), 1);
        changeSelectButtonValue(document, util.select_box_uncheck_color, book_id);
        selected_books_count_text.innerText = selected_books.length;
    }

}
window.toggleSelectBook = toggleSelectBook;


// enable books selection (show select button on all books)
function toggleBooksSelection(ev){
    ev.preventDefault();
    let all_circles = Array.from(document.querySelectorAll('.select-box'));
    if (selection_enabled){

        select_books_options.forEach(item => {
            item.style.display = 'none';
        });
        selected_books = [];
        selected_books_count_text.innerText = 0;
        selection_enabled = false
    }
    else{
        select_books_options.forEach(item => item.style.display = 'contents');
        selected_books_count_text.innerText = selected_books.length;
        selection_enabled = true
    }

    selectButtonsToCurrentState(all_circles)
}
window.toggleBooksSelection = toggleBooksSelection;


function setHrefToSelectedBooks(aTag){
    aTag.href = `${aTag.name}-multiple-books/${selected_books.join('/')}/`
}
window.setHrefToSelectedBooks = setHrefToSelectedBooks;


document.getElementById('share').addEventListener('click', function(){
    let url = `multiple-books/${this.name}/`

    fetch(url, {
        method: "post",
        headers: {
            'Content-Type': 'text/plain',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: selected_books.join('/'),

    }).then((res) => {
        if (res.ok){
            return res.text()
        }else{
            console.log("something is wrong with this");
        }
    }).then(resText => {
        console.log(resText);
    }).catch(err => {
        console.log(err);
    })
});


function showPdf(ev,aTag){
    // ev.preventDefault()
    // let curr_link = aTag.href;
    // console.log(curr_link)
    // let xhr = new XMLHttpRequest()
    
    // xhr.open("GET",aTag.href,false)
    // xhr.send()

}
window.showPdf = showPdf;

