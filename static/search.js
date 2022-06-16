/** Handles passing search term to back end and processing returned JSON response */

const $results_div = $('#search_results');
const $data_div = $('#search_append');

function handleSearch(evt) {
    // Handles serach submission
    evt.preventDefault();
    let term = $('#searchbar').val();

    if ($results_div.hasClass("d-none")) {
        $results_div.removeClass("d-none");
        $data_div.html("");
    }
    else {
        $data_div.html("");
    }

    let data = sendSearchRequest(term);
    data.then(resp => { displaySearchData(resp) })
        .catch(err => { console.log(err) });
}

async function sendSearchRequest(term) {
    // Takes in serach term, sends requst to backend. Expects JSON returned.\
    try {
        let resp = await axios.get(`/api/search?term=${term}`);
        return resp["data"];
    } catch (e) {
        console.log("Rejected!", e);
        return undefined;
    }
}

function buildSearchHtml(data) {
    // handles building all html for search results, based on category of data
    // $html will be what we append each $data_card to
    let $html = $('<div>').addClass("row justify-content-center");

    // create all the pieces of a full $data_card, build it, then clone this full element for each data piece necessary.
    let $col = $('<div>').addClass("col-12 col-md-6 mt-2");
    let $card = $('<div>').addClass("card");
    let $h5 = $('<h5>').addClass("card-title text-center");
    let $p = $('<p>').addClass("text-center");

    //Build $data_card
    $card.append($h5).append($p);
    let $data_card = $col.append($card);

    function correctTitle(cat, key) {
        // Formats text based on key passed in
        if (cat == "block") {
            switch (key) {
                case "difficulty":
                    return "Block Difficulty";
                case "es_link":
                    return "Etherscan.io Link";
                case "miner":
                    return "Miner Address";
                case "number":
                    return "Block Number";
                case "timestamp":
                    return "Timestamp";
                case "transactions":
                    return "# of Transactions";
            }
        }
        if (cat == "tx") {
            switch (key) {
                case "hash":
                    return "Tx Hash";
                case "blockNumber":
                    return "Block Number";
                case "from":
                    return "Sender";
                case "to":
                    return "Receiver";
                case "value":
                    return "Eth Transfered";
                case "es_link":
                    return "Etherscan.io Link";
            }
        }
        if (cat == "address") {
            switch (key) {
                case "eth_balance":
                    return "Ethereum Balance";
                case "address":
                    return "Wallet Address";
                case "eth_txs":
                    return "Normal Txs";
                case "token_txs":
                    return "Internal Txs";
                case "es_link":
                    return "Etherscan.io Link";
            }
        }
    }

    function buildCards($html, data) {
        for (let key in data) {
            if (key !== "category") {
                let $cDataCard = $data_card.clone();
                $cDataCard.find('h5').text(correctTitle(data["category"], key));
                if (key == "es_link") {
                    $cDataCard.find('p').append($('<a>').attr("href", `https://${data[key]}`).attr("target", "_blank").attr("rel", "noopener noreferrer").text(data[key]));
                }
                else if (key == "eth_txs" || key == "token_txs") {
                    $cDataCard.find('p').text(data[key].length);
                }
                else {
                    $cDataCard.find('p').text(data[key]);
                }
                $html.append($cDataCard);
            }
        }
        return $html;
    }

    if (data['category'] === "block") {
        // clone $data_card and fill in necessary data. each clone gets appened to $html
        // build header card for results
        let $headCard = $data_card.clone();
        $headCard.removeClass("col-12 col-md-6").addClass("col-8");
        $headCard.find('h5').text("Block Information");
        $headCard.find('p').remove();
        $html.append($headCard);

        $html = buildCards($html, data);
    }

    else if (data.category == "tx") {
        // clone $data_card and fill in necessary data. each clone gets appened to $html
        // build header card for results
        let $headCard = $data_card.clone();
        $headCard.removeClass("col-12 col-md-6").addClass("col-8");
        $headCard.find('h5').text("Transaction Info");
        $headCard.find('p').remove();
        $html.append($headCard);

        $html = buildCards($html, data);
    }

    else if (data.category == "address") {
        // clone $data_card and fill in necessary data. each clone gets appened to $html
        // build header card for results
        let $headCard = $data_card.clone();
        $headCard.removeClass("col-12 col-md-6").addClass("col-8");
        $headCard.find('h5').text("Wallet Address Info");
        $headCard.find('p').remove();
        $html.append($headCard);

        $html = buildCards($html, data);
    }

    else {
        $p = $('<p>').text(data["invalid"]);
        $html.append($p);
    }

    return $html;
}

function displaySearchData(data) {
    // Handles displaying data appropriately
    let $html = buildSearchHtml(data);
    $data_div.append($html);
}

$('#searchForm').on('submit', handleSearch);