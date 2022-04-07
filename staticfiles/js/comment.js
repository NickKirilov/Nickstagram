const comment_form = document.querySelectorAll('.form-comment');
const comment_btns = document.querySelectorAll('.comment-btn')
const comments_div = document.querySelectorAll('#comments-div')

function toggleCommentForm(form, comments_div){
    if (form.style.display === 'none'){
        form.style.display = 'inline-block';
        if(comments_div.length !== 0){
            comments_div[0].style.display = 'inline-block';
        }
    } else if(form.style.display === 'inline-block') {
        form.style.display = 'none';
        if(comments_div.length !== 0){
            let comments = document.querySelectorAll('.comment')
            if(comments.length === 0) {
                comments_div[0].style.display = 'none';
            }
        }
    }

}

for(let i = 0;i<comment_btns.length; i++){
    comment_form[i].addEventListener('submit', ()=>toggleCommentForm(comment_form[i]));
    comment_btns[i].addEventListener('click', ()=>toggleCommentForm(comment_form[i], comments_div));
}
