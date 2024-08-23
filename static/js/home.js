const button = document.querySelector('div.search-box button');
const keyword = document.querySelector('div.search-box input');



function searchKeyword() {
    // routing
    location.href = `/search?keyword=${keyword.value}`   
}


button.addEventListener('click', searchKeyword);
    