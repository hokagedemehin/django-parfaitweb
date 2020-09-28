var updateBtns = document.querySelectorAll('.update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product;
        var action = this.dataset.action;
        var record = this.dataset.record;
        console.log('values from button',productId, action);
        

        if (user == 'AnonymousUser') {
            addCookieItem(productId, action, record);
        } else {
            console.log(user);
            updateUserOrder(productId, action, record);
        }
        });
    
}

function addCookieItem(productId, action, record){
    console.log('user not authenticated from add cookie item at cart.js');
    rec = record;
    if(action == 'add'){
        if(cart[productId] == undefined){
            cart[productId] = {'quantity': 1, 'records': record};
        }else {
            cart[productId]['quantity'] += 1;
            cart[productId]['records'] -= 1;
            
        }
    }
    
    else if(action == 'remove'){
        cart[productId]['quantity'] -= 1;
        cart[productId]['records'] += 1;
        if (cart[productId]['quantity'] <= 0 ){
            cart[productId]['records'] += rec;
            console.log('item will be cleared');
            
            delete cart[productId];
        }
    }

    else if(action == 'add' && cart[productId]['quantity'] == rec){
        cart[productId]['quantity'] = rec;
    }

    if(action == 'clear'){
        cart[productId]['records'] += rec;
        console.log('item will be cleared with close button');
        delete cart[productId];
    }

    console.log('cartalog js:', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}

// if action == 'add' and orderItem.quantity < rec:
//         orderItem.quantity = (orderItem.quantity + 1)
//         product.records = (int(product.records) - 1)
//         print(product.records, rec)
//         product.save()
//     elif action == 'remove':
//         orderItem.quantity = (orderItem.quantity - 1)
//         product.records = (int(product.records) + 1)
//         print(product.records, rec)
//         product.save()
//     elif orderItem.quantity == rec and action == 'add':
//         orderItem.quantity = rec
//     orderItem.save()
    
//     if orderItem.quantity <= 0 or action == 'clear':
//         product.records = rec
//         product.save()
//         orderItem.delete()

function updateUserOrder(productId, action, record) {
    console.log('update user order log');
    var url = '/update-item/';
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type':"application/json", 'X-CSRFToken': csrftoken,}, 
        body: JSON.stringify({'productId': productId, 'action': action, 'record': record })
    })
    .then((response) => {return response.json();})
    .then((data) => {
        console.log('second then promise:', data);
        location.reload();
    });
}

// setInterval(updateUserOrder, 1000);

// #############################################################################
// Date at footer
// ################################################
const date = document.getElementById('date');
date.innerHTML = new Date().getFullYear();

const footer = document.querySelector('.foot');
footHeight = footer.getBoundingClientRect().height;
console.log(footHeight);

const main = document.querySelector('.main');
const allbody = document.querySelector('#bodytag');
const allhtml = document.querySelector('#htmltag')
winHeight = window.innerHeight;
console.log('windows: ',winHeight);
bodyHeight = allbody.getBoundingClientRect().height;
console.log('body: ',bodyHeight);
htmlHeight = allhtml.getBoundingClientRect().height;
console.log('html: ', htmlHeight);

main.style.minHeight = `calc(${winHeight}px - ${footHeight}px)`;

// const htmltag = document.querySelector('#htmltag');
// htmlheight = htmltag.clientHeight;
// console.log(htmlheight); 


// const navitem = document.querySelectorAll('.nav-item');

// navitem.forEach((item) => {
//     const btn = item.querySelector('.nav-link');
//     btn.addEventListener('click', ()=>{
//         item.classList.toggle('active');
//         item.classList.
//         console.log('item clicked');
//     });
// });

// (function() {
//     var nav = document.getElementById('nav'),
//         anchor = nav.getElementsByTagName('a'),
//         current = window.location.pathname.split('/')[1];
//         for (var i = 0; i < anchor.length; i++) {
//         if(anchor[i].href == current) {
//             anchor[i].classList.toggle('active')
//             console.log(anchor[i]);
//         }
//     }
// })();

function setNavigation() {
    let current_location = location.pathname.split('/')[1];
    if (current_location === "") 
        return document.querySelector('#home').classList.toggle('active');
    let menu_items = document.querySelector("nav").getElementsByTagName("a");
    for (let i = 0, len = menu_items.length; i < len; i++) {
      if (menu_items[i].getAttribute("href").indexOf(current_location) !== -1) {
        // menu_items[i].className = "active";
        menu_items[i].classList.toggle('active');
        console.log(menu_items[i]);
      }
    }
  }
  setNavigation();


const topLink = document.querySelector('.top-link');
window.addEventListener('scroll', ()=>{
    const scrollHeight = window.pageYOffset;

    if (scrollHeight > 700) {
        topLink.classList.remove('tw-invisible')
        topLink.classList.add('tw-visible');
    }
    else {
        topLink.classList.remove('tw-visible');
        topLink.classList.add('tw-invisible');
    }
});