/** JavaScript file */
function show_menu(){
    /** 
     * Function for showing menu side bar when it is closed.
    */

    x = window.matchMedia('(max-width: 700px)');

    if (x.matches){
        document.querySelector('.nav_panel').style.display = 'flex';
        document.querySelector('#show_menu').style.display = 'none';
        document.querySelector('#hide_menu').style.display = 'block';
        document.querySelector('#hide_menu').style.cursor = 'pointer';
        document.querySelector('.nav_panel').style.position = 'fixed';
        document.querySelector('.nav_panel').style.zIndex = '30';
        document.querySelector('.nav_panel').style.width = '70%';
    }
    else{
        document.querySelector('.nav_panel').style.display = 'none';
        document.querySelector('.header').style.width = '100%';
        document.querySelector('.main').style.width = '100%';
        document.querySelector('#show_menu').style.display = 'none';
        document.querySelector('#hide_menu').style.display = 'block';
    };
}


function hide_menu(){
    /**
     * Function for hiding menu side bar when it is open.
    */

    x = window.matchMedia('(max-width: 700px)');

    if (x.matches){
        document.querySelector('.nav_panel').style.display = 'none';
        document.querySelector('#show_menu').style.display = 'block';
        document.querySelector('#hide_menu').style.display = 'none';
        document.querySelector('.main').style.zIndex = '0';
    }
    else{
        document.querySelector('.nav_panel').style.display = 'flex';
        document.querySelector('.header').style.width = '80%';
        document.querySelector('.main').style.width = '80%';
        document.querySelector('#show_menu').style.display = 'block';
        document.querySelector('#hide_menu').style.display = 'none';
    };
}


// The below event will happen on the "new_item_1.html" page
function social_fun(data){
    /**
     * This function will fire when we select `social media` as our category when creating new item. What it does is, it will only display the `#plat_social' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category.
    */

    document.querySelector('.selected_category').value = data.value;
    document.querySelector('.selected_platform').value = null;
    document.querySelector('#plat_social').style.display = 'block';
    document.querySelector('#plat_cloud').style.display = 'none';
    document.querySelector('#plat_card').style.display = 'none';
    document.querySelector('#plat_other').style.display = 'none';
    document.querySelector('.selected_platform_span').style.display = 'block';
}


function cloud_fun(data){
    /**
     * This function will fire when we select `cloud` as our category when creating new item. What it does is, it will only display the `#plat_cloud' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category.
    */

    document.querySelector('.selected_category').value = data.value;
    document.querySelector('.selected_platform').value = null;
    document.querySelector('#plat_social').style.display = 'none';
    document.querySelector('#plat_cloud').style.display = 'block';
    document.querySelector('#plat_card').style.display = 'none';
    document.querySelector('#plat_other').style.display = 'none';
    document.querySelector('.selected_platform_span').style.display = 'block';
}


function card_fun(data){
    /**
     * This function will fire when we select `card` as our category when creating new item. What it does is, it will only display the `#plat_card' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category.
    */

    document.querySelector('.selected_category').value = data.value;
    document.querySelector('.selected_platform').value = null;
    document.querySelector('#plat_social').style.display = 'none';
    document.querySelector('#plat_cloud').style.display = 'none';
    document.querySelector('#plat_card').style.display = 'block';
    document.querySelector('#plat_other').style.display = 'none';
    document.querySelector('.selected_platform_span').style.display = 'block';
}


function other_fun(data){
    /**
     * This function will fire when we select `other` as our category when creating new item. What it does is, it will only display the `#plat_other' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category.
    */

    document.querySelector('.selected_category').value = data.value;
    document.querySelector('.selected_platform').value = null;
    document.querySelector('#plat_social').style.display = 'none';
    document.querySelector('#plat_cloud').style.display = 'none';
    document.querySelector('#plat_card').style.display = 'none';
    document.querySelector('#plat_other').style.display = 'block';
    document.querySelector('.selected_platform_span').style.display = 'block';
}


// The below event will happen on the "new_item_1.html" page also
function plat_select_fun(data){
    /**
     * This function is for giving a value to our '.selected_platform`, of which of what so ever platform we select (it will take an argument of data from that radio).
    */

    if (data.value == 'custom'){
        document.querySelector('.custom_platform_span').style.display = 'block';
        document.querySelector('.selected_platform').value = data.value;

        // adding input tag in the `custom_platform_span` span tag
        document.querySelector('.custom_platform_span').innerHTML ='<br> Custom platform: <input type="text" name="custom_platform" placeholder="Type custom platform name" required>';
    }
    else{
        document.querySelector('.custom_platform_span').style.display = 'none';
        document.querySelector('.selected_platform').value = data.value;
        document.querySelector('.custom_platform_span').innerHTML = '';
    };
}


function validate_category_value(category_value){
    /**
     * Function for validating category data value on the front end page `new_item_1.html.
    */

    data = category_value.value;

    // our list of categories from database
    categories = document.querySelector('.categories').value;

    if (categories.includes(data)){
        document.querySelector('.selected_category_error').style.display = 'none';
    }
    else{
        document.querySelector('.selected_category_error').style.display = 'block';
        document.querySelector('.selected_category_error').style.color = 'red';
        document.querySelector('.selected_category_error').style.fontStyle = 'italic';
        document.querySelector('.selected_category_error').style.fontWeight = 'bold';
    };
}


function validate_platform_value(platform_value){
    /**
     * Function for validating platform data value on the front end page `new_item_1.html.
    */

    data = platform_value.value;

    // our list of platforms from database
    platforms = document.querySelector('.platforms').value;
    
    if (platforms.includes(data)){
        document.querySelector('.selected_platform_error').style.display = 'none';
    }
    else{
        document.querySelector('.selected_platform_error').style.display = 'block';
        document.querySelector('.selected_platform_error').style.color = 'red';
        document.querySelector('.selected_platform_error').style.fontStyle = 'italic';
        document.querySelector('.selected_platform_error').style.fontWeight = 'bold';
    };
}


function validate_passcode_value(field_two){
    /**
     * Function for validating passcode data value on the front end page (setting and updating passcode).
    */

    field_one = document.querySelector('.passcode_ingredient').value;

    if (field_two.value !== field_one){
        document.querySelector('.selected_passcode_error').style.display = 'block';
        document.querySelector('.selected_passcode_error').style.color = 'red';
        document.querySelector('.selected_passcode_error').style.fontStyle = 'italic';
        document.querySelector('.selected_passcode_error').style.fontWeight = 'bold';
        document.querySelector('.selected_passcode_success').style.display = 'none';
    }
    else{
        document.querySelector('.selected_passcode_error').style.display = 'none';
        document.querySelector('.selected_passcode_success').style.display = 'block';
        document.querySelector('.selected_passcode_success').style.color = 'green';
        document.querySelector('.selected_passcode_success').style.fontWeight = 'bold';
    };
}


function restrict_window_click(){
    /** 
     * A request validator function, that will restrict user from clicking anywhere. It is used directly when supervisor submitting student logbook as well as when sending messages.
    */

    document.querySelector('.dew').style.display = 'flex';
    document.querySelector('.container').style.position = 'fixed';
}


function val_required_fields(e, field, agree=false){
    /** 
     * Function for request validator, that will restrict user from clicking anywhere by the help of `restrict_window_click` function above. It check if fields required are empty, then it won`t restrict the window activities, else it will.
     * 
     * The `fields` are the list of fields need to validate (required).
     * 
     * The `agree` should be true if an only a form to submit required to checked a `checkbox`.
     * 
     * The `e` is the button that is clicked.
    */

    // separating with comma `,` which make it a list.
    fields_to_check = field.split(',');

    // values of the `fields_to_check` to use and compare if there are any invalid one.
    d_store = [];

     // Fields tags to use for html query.
     // `input` is for text, checkbox and radio type.
     // `textarea` for comment fields of student logbook or siwes document.
     // `select` for selecting students when coordinato givinig them a supervisor, or when admin giving supervisors to a coordinator.
    fields_tag_to_check = document.querySelectorAll('input, textarea, select');

    fields_tag_to_check.forEach(element => {
        // checking each field by detecting if it name exist in the `fields_to_check` list.
        if (fields_to_check.includes(element.name)){

            // error color
            if (element.value == '' || element.value == null || element.value == false){
                element.style.border = 'solid red 3px';
            }
            else{
                element.style.border = 'none';
            };

            // validate email field, if found
            if (element.type == 'email'){
                // global search of email validation, which validate email that doesn't start with white-space or @ symbol (one or more character), plus @ symbol, plus not white-space or @ symbol (one or more character), plus . character, plus white-space or @ symbol (one or more character)
                reg = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

                // all email fields
                val_email = document.querySelectorAll('input[type="email"]');

                val_email.forEach(eml => {
                    if (eml.value.match(reg)){
                        element.style.border = 'none';
                    }
                    else{
                        d_store.push(false);
                        element.style.border = 'solid red 3px';
                    };
                });
            };

            // for checkbox
            if(element.name == 'agree'){
                if (element.checked == true || element.checked === true){
                    d_store.push('agree');
                };

                // If the form to submit required to checked the `checkbox`. The inner condition will check the value of the `checkbox`, if it is false, then it will append in valid value to the `d_store` list and that will prevent the validation event to trigger.
                if (agree == true){
                    if (element.checked == false || element.checked === false){
                        d_store.push(false);
                    };
                };
            }
            else{
                // if it is not checkbox and not radio button. Note: sometimes checkbox and radio button is not required in a form.
                if(element.type != 'radio'){
                    // In other to avoiding adding radio buttons values, since it own is implemented down below.
                    d_store.push(element.value);
                };
            };
        };
    });

    // for radio buttons, mostly used when assigning list of supervisors to a departmental coordinator, or coordinator assigning supervisor to students.
    if (fields_to_check.includes('radio')){
        radio_inputs = document.querySelector('input[type="radio"]:checked');

        if (radio_inputs != null){
            d_store.push(radio_inputs.value);
        }
        else{
            d_store.push(false);
        };
    };

    // for country field in signup form
    try{
        country = document.querySelector('#id_country');
        // error color
        if (country.value == '' || country.value == null || country.value == false){
            country.style.border = 'solid red 3px';
            d_store.push(false);
        }
        else{
            country.style.border = 'none';
        };
    }
    catch(err){
        // pass
        // alert(err.message)
    };
    
    // checking if any unwanted value exist in our `d_store` list.
    if (d_store.includes('') || d_store.includes(null) || d_store.includes(false)){
        // pass and do nothing `restrict_window_click` won't trigger-up!
    }
    else{
        // if all validation pass, this will follow 🚀 ✅ that is good.
        // e.style.display = 'None';
        restrict_window_click();
    };
}


function show_val_progress(e, field){
    /**
     * This a function that show user an illustration of passcode validation.
    */

    passcode = document.querySelector('input[name="passcode"]').value;
    if (passcode.length > 8){

        // validator function
        val_required_fields(e, field);
        
        // hiding alert
        document.querySelectorAll('.alert_info, .alert_success, .alert_warning').forEach( e => {
            e.style.display = 'none';
        });

        try{
            document.querySelector('.p_multi').style.display = 'none';
        }
        catch(err){
            // pass
            // alert(err.message)
        };
        
        // hiding button
        document.querySelector('.btn').style.display = 'none';
        document.querySelector('.next_p').style.display = 'none';
        document.querySelectorAll('.input').forEach(e => {
            e.style.display = 'none';
        })

        // hiding alert divs
        document.querySelector('.alert_info').style.display = 'none';
        document.querySelector('.alert_success').style.display = 'none';
        document.querySelector('.alert_warning').style.display = 'none';
    };
}


function hide_sensitive(){
    /** Hide sensitive information function */

    document.querySelectorAll('.box_inn input').forEach(e => {
        e.type = 'password';
        e.style.border = 'none';
    });
}


function show_sensitive_value(e){
    /** Show a single sensitive information value */

    // hide all previous open sensitive information
    hide_sensitive();
    
    p = e.parentElement;
    p.firstElementChild.type = 'text';
    // p.children[0].type = 'text';

    // hide the current open sensitive information after 7 seconds
    setTimeout(hide_sensitive, 7000);
}
