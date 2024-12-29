const imageData=[
    {url:'static/rooms/beds-1Adult.jpeg',description:'Bed for 1 Adult',price:'2500'},
    {url:'static/rooms/beds-1Adult-A.jpeg',description:'Bed for 1 Adult',price:'2500'},
    {url:'static/rooms/beds-1Adult-B.jpeg',description:'Bed for 1 Adult',price:'2500'},
    {url:'static/rooms/beds-1Adult-C.jpeg',description:'Bed for 1',price:'2500'},
    {url:'static/rooms/beds-1Adult-D.jpeg',description:'Bed for 1',price:'2500'},
    {url:'static/rooms/beds-2Adults.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-A.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-B.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-C.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-D.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-E.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-F.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-G.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-H.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-I.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-J.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-K.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-L.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-M.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-N.jpeg',description:'Bed for 2 Adults',price:'2500'},
    {url:'static/rooms/beds-2Adults-1child.jpeg',description:'Bed for 2 Adults,2 children',price:'2500'},
    {url:'static/rooms/beds-2Adults-2children.jpeg',description:'Bed for 2 Adults,2 children',price:'2500'}
];

const imageContainer=document.getElementById('fram');
/*
imageData.forEach(data=>{
    const frame=document.createElement('div');
    frame.classList.add('picture');

    const imgElement=document.createElement('img');
    imgElement.src=data.url;
    //imgElement.alt=data.description;

    const description=document.createElement('h2');
    description.textContent=data.description;

    const price=document.createElement('h3');
    price.textContent=data.price;

    frame.appendChild(imgElement);
    frame.appendChild(description);
    frame.appendChild(price);
    imageContainer.appendChild(frame);

});
*/


window.onload=function(){
    var images=document.querySelectorAll('.picture img');
    var popform=document.forms[0];

    images.forEach(image=>{
        image.addEventListener('click',function(){
            const imageName=image.getAttribute('src').replace("static/rooms/","");
            const price=image.getAttribute('data-price');
            const description=image.getAttribute('data-description');

            const prevDate=new Date(document.forms[0].check_in_date.value);
            const nextDate=new Date(document.forms[0].check_out_date.value);

            popform.elements.photo.value=imageName;
            popform.elements.price.value=price;
            popform.elements.quantity.value=1;
            popform.elements.name.value=description;

            //calculate difference
            const diffTime=nextDate.getTime()-prevDate.getTime();
            //convert difference to days
            const duration=Math.abs(Math.round(diffTime/(1000*3600*24)));
            popform.elements.total.value="Kes "+((price.replace("Kes","")*duration));

            document.forms[0].check_out_date.addEventListener('change',function(){
                const prevDate=new Date(document.forms[0].check_in_date.value);
                const nextDate=new Date(document.forms[0].check_out_date.value);
                
                //calculate difference
                const diffTime=nextDate.getTime()-prevDate.getTime();
                //convert difference to days
                const duration=Math.abs(Math.round(diffTime/(1000*3600*24)));
                popform.elements.total.value="Kes "+((price.replace("Kes","")**duration));
            });
            document.forms[0].check_in_date.addEventListener('change',function(){
                const prevDate=new Date(document.forms[0].check_in_date.value);
                const nextDate=new Date(document.forms[0].check_out_date.value);
                
                if(prevDate.getDate()<new Date().getDate()){
                    alert("Chosen an Invalid date. Try Today onwards!!");
                    popform.elements.check_in_date.innerHTML=prevDate;
                }else{
                    //calculate difference
                    const diffTime=nextDate.getTime()-prevDate.getTime();
                    //convert difference to days
                    const duration=Math.abs(Math.round(diffTime/(1000*3600*24)));
                    popform.elements.total.value="Kes "+((price.replace("Kes","")*duration));
                }
            });
            popform.style.display="block";
        });
    });
    images.forEach(function(room){
        const isBooked=room.querySelector('.padlock')!==null;
        if(isBooked){
            room.style.border='1px solid red';
        }
    });
    document.addEventListener('DOMContentLoaded',function(){
        const imageInput=document.querySelectorAll('#imag');
        imageInput.forEach(imp=>{
            const saveBtn=document.getElementById("btnsub");
            saveBtn.addEventListener('click',function(event){
                event.preventDefault();
                imp.disabled=true;
                document.forms[0].submit();
            });
        });

    });
}

var popform=document.forms[0];
document.getElementById("closebtn").onclick=function(){
    popform.style.display="none";
}