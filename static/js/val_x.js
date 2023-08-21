
function show_val_progress(){
    // this a function that show user an illustration of passcode validation
    passcode = document.querySelector('.input').value
    if (passcode.length > 8){
        document.querySelector('.two_1').style.display = 'flex';
        document.querySelector('.b_auth_process').style.display = 'flex';
        document.querySelector('.vault').style.display = 'none';
        document.querySelector('.h1_auth').style.display = 'none';
        document.querySelector('.p_auth').style.display = 'none';
        document.querySelector('.b_auth').style.display = 'none';
    }
}
