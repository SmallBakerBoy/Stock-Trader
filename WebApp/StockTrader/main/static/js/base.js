function csrf() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function  buy() {

}

function  sell() {
    
}

function add_watchlist() {

}

function switch_watchlist() {

}

function create_portfolio() {
    var settings = {type: 'create', user: document.getElementById('user-id').value}
    fetch('/home/create',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    )
}

function update_portfolio() {
    var settings = {type: 'update', user: document.getElementById('user-id').value}
    fetch('/home/create',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    )
}

