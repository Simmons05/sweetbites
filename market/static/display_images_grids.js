//Display images in html using javascript function
imageFoods=[
    {url:"/static/food/Cookie.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/barbeque-mix.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/brooke-lark-oaz.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/cake-candy.jpg",description:"Cake candy",price:"on Order Food page"},
    {url:"/static/food/cool-crunchies.jpg",description:"Cool crunchies",price:"on Order Food page"},
    {url:"/static/food/french-dish.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/hot-dog.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/Korean-succi-dish.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/mexican-kik-dish.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/pizza.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/puddin-melon.jpg",description:"View",price:"on Order Food page"},
    {url:"/static/food/Tortilla.jpg",description:"View",price:"on Order Food page"},
];
var foodContainer=document.getElementById("tab2");
imageFoods.forEach(food=>{
    const banner=document.createElement('div');
    banner.classList.add("image-frame");

    const imgElement=document.createElement("img");
    imgElement.src=food.url;
    
    const price=document.createElement("p");
    price.textContent=food.price;

    const description=document.createElement("p");
    description.textContent=food.description;

    banner.appendChild(imgElement);
    banner.appendChild(description);
    banner.appendChild(price);
    foodContainer.appendChild(banner);

    imgElement.onclick=function(){
        //document.forms[0].style.display="block";
        window.location.assign("order_food");
    }
});

imageRooms=[
    {url:"/static/rooms/beds-1Adult.jpeg",description:"View specs",price:"on booking page"},
    {url:"/static/rooms/beds-1Adult-A.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-1Adult-B.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-1Adult-C.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-1Adult-D.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-1child.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-2children.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-A.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-B.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-C.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-D.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-E.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-F.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-G.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-H.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-I.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-J.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-K.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-L.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-M.jpeg",description:"View specs",price:" on booking page"},
    {url:"/static/rooms/beds-2Adults-N.jpeg",description:"View specs",price:" on booking page"}
];


var roomContainer=document.getElementById("tab4");
imageRooms.forEach(room=>{
    const banner=document.createElement('div');
    banner.classList.add("image-frame");

    const imgElement=document.createElement("img");
    imgElement.src=room.url;
    
    const price=document.createElement("p");
    price.textContent=room.price;

    const description=document.createElement("p");
    description.textContent=room.description;

    banner.appendChild(imgElement);
    banner.appendChild(description);
    banner.appendChild(price);
    roomContainer.appendChild(banner);

    
    /*var clsb=document.getElementById("close");
    clsb.onclick=function(){
        if(document.forms[0].style.display=="block"){
            document.forms[0].style.display="none";
        }
    }*/
    imgElement.onclick=function(){
        window.location.assign("order_room");
    }
});

const content=document.querySelector('#tab4');
let scrollPos=0;

function autoScroll(){
    scrollPos+=1;
    content.scrollTo(0,scrollPos);
    if(scrollPos>=content.scrollHeight-content.clientHeight){
        scrollPos=0;
    }
}
//setInterval(autoScroll,50);

