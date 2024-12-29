window.onload=function(){
    var btns=document.querySelectorAll("table:last-child tbody tr td:first-child .chbox");
    var rows=document.querySelectorAll("table:last-child tbody tr");

    rows.forEach(row=>{
        row.addEventListener('click',function(){
            btns.style.display="block";
            btns.forEach(btn=>{
                btn.addEventListener('click',function(){
                    if(btn.checked){
                        alert(row.innerHTML);
                    }
                });
            });
        });
    });
    alert(125);
    var button=document.querySelector("#selector button");

    button.onclick=function(){
        document.querySelector("#selector").style.display="none";
    }
}