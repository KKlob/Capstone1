document.onload = function () {
    const $userFormBtn = $('button #form_submit');

    $userFormBtn.on('submit', () => {
        $('#flashed_msgs').empty();
    });
}

function handleAddWallet(evt) {
    // handles adding wallet request
    evt.preventDefault();
    let addr = $('#addwalletbar').val();
    $('#addwalletbar').val("");

    let wallet = addWallet(addr);
    wallet.then(resp => {
        if (Object.keys(resp).includes("error")) {
            alert(resp['error']);
        }
        else {
            displayWalletData(resp)
        }
    }).catch(err => { console.log(err) });
}

async function addWallet(addr) {
    try {
        let resp = await axios.post('/api/add_addr', { wallet: addr })
        return resp['data'];
    } catch (e) {
        console.log("Rejected!", e);
        return undefined;
    }
}

function displayWalletData(data) {
    // takes in wallet data, creates html and appends it to page
    let $wallets = $('#wallet_section');

    let $row = $('<div>').addClass("row justify-content-center mt-2")
    let $col_contain = $('<div>').addClass("col-12 col-md-6 col-lg-4");

    // Build basic card
    let $card = $('<div>').addClass("card");
    $card.append($('<div>').addClass("card-title text-center").append($('<h5>')));
    $card.append($('<div>').addClass("card-text text-center").append($('<p>')));

    // Clone card for addrs, append to clone of $col_contain, append to $row
    let $addr_card = $card.clone();
    let $col_clone = $col_contain.clone();

    $addr_card.find('.card-title').children('h5').text("Wallet Address");
    $addr_card.find('.card-text').children('p').text(data['wallet_address']);
    $col_clone.append($addr_card);
    $row.append($col_clone);

    // Clone card for eth_total, append to $con_contain

    let $eth_card = $card.clone();
    $col_clone = $col_contain.clone();

    $eth_card.find('.card-title').children('h5').text("Eth Total");
    $eth_card.find('.card-text').children('p').text(data['eth_total']);
    $col_clone.append($eth_card);
    $row.append($col_clone);

    // append $row to $wallets
    $wallets.append($row);
}

$('#addwalletform').on('submit', handleAddWallet);