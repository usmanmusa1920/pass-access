
function show_val_progress(){
    // this a function that show user an illustration of passcode validation
    passcode = document.querySelector('.input').value
    if (passcode.length > 8){
        // displaying authentication illustration
        document.querySelector('.authentic').style.display = 'flex';
        document.querySelector('.auth_process').style.display = 'flex';

        // hiding
        document.querySelector('.vault').style.display = 'none';
        document.querySelector('.p_auth_1').style.display = 'none';
        document.querySelector('.p_auth_2').style.display = 'none';
        // hiding button
        document.querySelector('.btn').style.display = 'none';
        document.querySelector('.input').style.display = 'none';

        // hiding alert divs
        document.querySelector('.alert_info').style.display = 'none';
        document.querySelector('.alert_success').style.display = 'none';
        document.querySelector('.alert_warning').style.display = 'none';
    }
}
