toggleSpan = document.getElementById('toggleFunc');
toggleBtn = document.getElementById('toggleBtn');
table = document.querySelector('.table-view');



toggleBtn.onclick = function(){ 
    if (table.classList.contains('hidden')){
        toggleSpan.innerHTML = 'Hide';
        table.classList.remove('hidden'); 
    }else{
        toggleSpan.innerHTML = 'View';
        table.classList.add('hidden'); 
    }
}