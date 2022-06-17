document.onload = function () {
    const $formBtn = $('button');


    $formBtn.on('submit', () => {
        $('#flashed_msgs').empty();
    });
}
