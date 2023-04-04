var ShoppingCart = function(){
    function createCookie(name, value, days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + value + expires + "; path=/";
    }

    function readCookie(name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for(var i=0;i < ca.length;i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }

    var items = []
    var cukiname = "ShpCrt"

    return{
        init: function() {
            rawItems = readCookie(cukiname)
            if (rawItems){
                try {
                    items = JSON.parse(decodeURIComponent(rawItems))
                } catch(e) {
                    items = []
                }
                items = items || []
            }
        },
        addItem: function(id, quantity, extraData) {
            items.push({id: id, quantity: quantity, data: extraData})
            createCookie(cukiname, encodeURIComponent(JSON.stringify(items)), 2)
        },
        removeItem: function(index) {
            items.splice(index, 1)
            createCookie(cukiname, encodeURIComponent(JSON.stringify(items)))
        },
        emptyCart: function() {
            items = []
            createCookie(cukiname, encodeURIComponent(JSON.stringify(items)))
        },
        getItems: function(){
            return items
        }
    }
}