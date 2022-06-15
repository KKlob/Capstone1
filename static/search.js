/** Handles passing search term to back end and processing returned JSON response */

function handleSearch(evt) {
    // Handles serach submission
    evt.preventDefault();
    let term = $('#searchbar').val();
    let data = sendSearchRequest(term);
}

async function sendSearchRequest(term) {
    // Takes in serach term, sends requst to backend. Expects JSON returned.\
    try {
        let resp = await axios.get(`/api/search?term=${term}`);
        console.log(resp);
    } catch (e) {
        console.log("Rejected!", e);
    }
}


$('#searchForm').on('submit', handleSearch);