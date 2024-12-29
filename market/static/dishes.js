
window.onload=function(){

    var images=document.querySelectorAll('.picture img');
    var popform=document.forms[0];

    images.forEach(image=>{
        image.addEventListener('click',function(){
            const imageName=image.getAttribute('src').replace("static/food/","");
            const price=image.getAttribute('data-price');
            const description=image.getAttribute('data-description');
            //const userdf=document.querySelector("#userid");

            popform.elements.photo.value=imageName;
            popform.elements.price.value=price;
            popform.elements.quantity.value=1;
            popform.elements.total.value="Kes "+((price.replace("Kes","")*popform.elements.quantity.value));
            popform.elements.name.value=description;
            //popform.elements.name.value=userdf.innerHTML;
            popform.elements.quantity.addEventListener('mouseleave',function(){
                popform.elements.total.value="Kes "+((price.replace("Kes","")*popform.elements.quantity.value));
            });
            popform.style.display="block";
        });
    });

}

document.getElementById("closebtn").onclick=function(){
    var popform=document.forms[0];
    popform.style.display="none";
}