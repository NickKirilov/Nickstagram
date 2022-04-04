const comment_form = document.querySelectorAll('form');
const comment_btns = document.querySelectorAll('.comment')

function toggleCommentForm(form){
    if (form.style.display === 'none'){
        form.style.display = 'inline-block';
    } else if(form.style.display === 'inline-block') {
        form.style.display = 'none';
    }

}

for(let i = 0;i<comment_btns.length; i++){
    comment_form[i].addEventListener('submit', ()=>toggleCommentForm(comment_form[i]))
    comment_btns[i].addEventListener('click', ()=>toggleCommentForm(comment_form[i]))
}
