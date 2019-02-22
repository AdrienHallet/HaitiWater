document.addEventListener("DOMContentLoaded", function(event) {

    let coll = document.getElementsByClassName("collapsible");

    for (let i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function() {
            console.log('click');
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.maxHeight){
                content.style.display = 'none';
                content.style.maxHeight = null;
            } else {
                content.style.display = 'block';
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    }
});
