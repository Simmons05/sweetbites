
var cont=document.getElementById("bar");
cont.onclick=function(){
    var tht=document.getElementById("container");
    var menu=document.getElementById("menu");
    if(menu.style.display=="block"){
        tht.style.width="100%";
        menu.style.display="none";
    }else{
        tht.style.width="calc(80% - 10px)";
        menu.style.display="block";
    }
}

//calculate bills
let priceElements=document.querySelectorAll("table tbody tr td:last-child");
let sum=0;
priceElements.forEach(pe=>{
    sum+=parseFloat(pe.innerText.replace('Kes',''));
});
document.getElementsByTagName("p")[3].innerText="Current bill:\nKes "+sum;
//alert(sum);

window.onload=function(){
    //opening tabs on menu item click
    //pages section
    var tab1=document.getElementById("tab1");
    var tab2=document.getElementById("tab2");
    var tab3=document.getElementById("tab3");
    var tab4=document.getElementById("tab4");

    //menu buttons
    var t1=document.getElementById("t1");
    var t2=document.getElementById("t2");
    var t3=document.getElementById("t3");
    var t4=document.getElementById("t4");

    //functions
    t1.onclick=function () {
        tab1.style.display="grid";tab2.style.display="none";tab3.style.display="none";tab4.style.display="none";
    }
    t2.onclick=function () {
        tab1.style.display="none";tab2.style.display="grid";tab3.style.display="none";tab4.style.display="none";
    }

    t3.onclick=function () {
        tab1.style.display="none";tab2.style.display="none";tab3.style.display="block";tab4.style.display="none";
    }

    t4.onclick=function () {
        tab1.style.display="none";tab2.style.display="none";tab3.style.display="none";tab4.style.display="grid";
    }


    const widgets=document.querySelectorAll('.widget');
    widgets.forEach(widget=>{
        widget.addEventListener('mouseover',()=>{
            alert("working out!!");
            widgets.forEach(otherWidget=>{
                if(otherWidget!==widget){
                    let rect=otherWidget.getBoundingClientRect();
                    let x=widget.getBoundingClientRect().left-rect.left;
                    let y=widget.getBoundingClientRect().top-rect.top;
                    alert("mouse in");
                    otherWidget.style.transform='translate(${x}px,${y}px)';
                }
            });
        });
        widget.addEventListener('mouseout',()=>{
            widgets.forEach(otherWidget=>{
                otherWidget.style.transform='translate(0px,0px)';
            })
        });
    });

}


