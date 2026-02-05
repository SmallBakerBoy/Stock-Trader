function csrf() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function create_popup(ticker,mode){
    document.getElementById('popup').hidden = false;

    document.getElementById('selected_company').innerHTML = ticker
    document.getElementById('ticker').value = ticker
    document.getElementById(mode).checked = true
}

function collapse(id){
    document.getElementById(id).hidden = true;
}

function  update(event) {
    event.preventDefault()

    let settings = {type: document.querySelector('input[name="action"]:checked')?.id, 
                    company: document.getElementById('ticker').value, 
                    amount: document.getElementById('slider').value, 
                    user: document.getElementById('user-id').value,
                }
    fetch('/update/',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    )
}


function add_watchlist() {

}

function switch_watchlist() {

}

function dynamic_search(query) {
    let settings = {query : query}
    fetch('/search/',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    })
    .then(response => response.json())
    .then(results => search_list(results))
    .catch(() => error('search_results'))
}

function search_list(results) {
    let list = document.getElementById('search_results')
    let html = ''

    results.forEach((result) => {
        html += `<li><p>${result}</p><button onclick='create_popup("${result}","buy")'>Buy</button></li>`
    })
    list.innerHTML = html
}

function toggle_dropdown(name) {
    let id = name.concat('-dropdown')
    let dropdown = document.getElementById(id)
    let info = document.getElementById(name.concat('-info'))

    dropdown.hidden = !(dropdown.hidden)

    if (!dropdown.hidden) {
    let settings = {ticker: name}
    fetch('/company/',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    ).then(response => response.json())
    .then(company_data => display(company_data,name))
    .catch(() => error(name.concat('-info')))
    }
}

function display(company_data,name){
    let info = document.getElementById(name.concat('-info'))
    let html =''

    keys = Object.entries(company_data)
    keys.forEach(([key,value]) => {
        html += `<p>${key} : ${value}</p>`
    })
    info.innerHTML = html

}

function error(element){
    let info = document.getElementById(element)
    info.innerHTML = '<p>Data could not be retrieved</p>'
}

function create_portfolio() {
    let settings = {type: 'create', user: document.getElementById('user-id').value}
    fetch('/home/create',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    ).then(response => success())
}

function update_portfolio() {
    let settings = {type: 'update', user: document.getElementById('user-id').value}
    fetch('/home/create',
        {method: 'POST',
            headers: {'Content-type':'application/json','X-CSRFToken': csrf()},
            body: JSON.stringify(settings)
    }
    ).then(response => success())
}

function success(){
    document.getElementById('feedback').innerHTML = 'You have queued a request to update your portfolio, Please come back later to view the suggested trades. Thank you for your patience.'
}

