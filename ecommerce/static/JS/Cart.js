/*The "user" keyword is from Django Authentication class
where there can only be 1 user object. Even if the script calls "users" object
it only means a "user" object with sepcial attributes.
Reference documentation:
https://docs.djangoproject.com/en/4.1/topics/auth/default/ */

var updateBtns = document.getElementsByClassName('update-cart');

for(var i=0; i< updateBtns.length;i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, "action: ", action)

        console.log('USER: ', user)
        if(user === 'AnonymousUser'){
            addCookieItem(productId, action)
        }else{
            updateUserOrder(productId, action)
        }
    })
}

//handle AnonymousUser user for cart and purchase
function addCookieItem(productId, action){
    console.log('Not logged in')
    if(action =='add'){
        if(cart[productId]===undefined){
            cart[productId] = {'quantity':1}
        }else{
            cart[productId]['quantity'] += 1;
        }
    }

    if(action == 'remove'){
        cart[productId]['quantity']-=1;
        if(cart[productId]['quantity']<=0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('Cart: ', cart)

    document.cookie = 'cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}


function updateUserOrder(productId, action){
    console.log('USER: ', user, ' is logged in. Sending data..')

    var url = '/update_item/' /*Send the data to update_item page*/
    /*fetch(the target path, what kind of data are we sending to)*/
    fetch(url, {
        method: 'POST',/*type of post request */
        /*The data that pass in */
        headers: {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },/*body data has to be a string for backend*/
        body:JSON.stringify({'productId': productId, 'action': action})
    })/* */
    /*handle a promise after the request is sent*/
    .then((response)=>{/*-> go to update item in views.py */
        return response.json()
    })

    .then((data)=>{/*<- comes back from updateItem in views.py*/
        console.log('data: ', data)
        //reload the page
        /*TODO: make an effecient way to only reload certain html elements */
        location.reload()
    })
}