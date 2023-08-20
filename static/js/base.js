
function showMenu() {
    // function for showing menu side bar when it is closed
    x = window.matchMedia('(max-width: 700px)')
    if (x.matches) {
        document.querySelector('.nav_panel').style.display = 'flex'
        document.querySelector('#show_menu').style.display = 'none'
        document.querySelector('#hide_menu').style.display = 'block'
        document.querySelector('.nav_panel').style.position = 'fixed'
        document.querySelector('.nav_panel').style.zIndex = '30'
        document.querySelector('.nav_panel').style.width = '70%'
        document.querySelector('.main').style.zIndex = '-5'
    } else {
        document.querySelector('.nav_panel').style.display = 'none'
        document.querySelector('.header').style.width = '100%'
        document.querySelector('.main').style.width = '100%'
        document.querySelector('#show_menu').style.display = 'none'
        document.querySelector('#hide_menu').style.display = 'block'
    }
}


function hideMenu() {
    // function for hiding menu side bar when it is open
    x = window.matchMedia('(max-width: 700px)')
    if (x.matches) {
        document.querySelector('.nav_panel').style.display = 'none'
        document.querySelector('#show_menu').style.display = 'block'
        document.querySelector('#hide_menu').style.display = 'none'
        document.querySelector('.main').style.zIndex = '0'
    } else {
        document.querySelector('.nav_panel').style.display = 'flex'
        document.querySelector('.header').style.width = '80%'
        document.querySelector('.main').style.width = '80%'
        document.querySelector('#show_menu').style.display = 'block'
        document.querySelector('#hide_menu').style.display = 'none'
    }
}


// the below event will happen on the "new_item_1.html" page
function social_fun(data) {
    /**this function will fire when we select `social media` as our category when creating new item. What it does is, it will only display the `#plat_social' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category */
    document.querySelector('.selected_category').value = data.value
    document.querySelector('.selected_platform').value = null
    document.querySelector('#plat_social').style.display = 'block'
    document.querySelector('#plat_cloud').style.display = 'none'
    document.querySelector('#plat_card').style.display = 'none'
    document.querySelector('#plat_other').style.display = 'none'
    document.querySelector('.selected_platform_span').style.display = 'block'
}


function cloud_fun(data) {
    /**this function will fire when we select `cloud` as our category when creating new item. What it does is, it will only display the `#plat_cloud' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category */
    document.querySelector('.selected_category').value = data.value
    document.querySelector('.selected_platform').value = null
    document.querySelector('#plat_social').style.display = 'none'
    document.querySelector('#plat_cloud').style.display = 'block'
    document.querySelector('#plat_card').style.display = 'none'
    document.querySelector('#plat_other').style.display = 'none'
    document.querySelector('.selected_platform_span').style.display = 'block'
}


function card_fun(data) {
    /**this function will fire when we select `card` as our category when creating new item. What it does is, it will only display the `#plat_card' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category */
    document.querySelector('.selected_category').value = data.value
    document.querySelector('.selected_platform').value = null
    document.querySelector('#plat_social').style.display = 'none'
    document.querySelector('#plat_cloud').style.display = 'none'
    document.querySelector('#plat_card').style.display = 'block'
    document.querySelector('#plat_other').style.display = 'none'
    document.querySelector('.selected_platform_span').style.display = 'block'
}


function other_fun(data) {
    /**this function will fire when we select `other` as our category when creating new item. What it does is, it will only display the `#plat_other' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category */
    document.querySelector('.selected_category').value = data.value
    document.querySelector('.selected_platform').value = null
    document.querySelector('#plat_social').style.display = 'none'
    document.querySelector('#plat_cloud').style.display = 'none'
    document.querySelector('#plat_card').style.display = 'none'
    document.querySelector('#plat_other').style.display = 'block'
    document.querySelector('.selected_platform_span').style.display = 'block'
}


// the below event will happen on the "new_item_1.html" page also
function plat_select_fun(data) {
    /**this function is for giving a value to our '.selected_platform`, of which of what so ever platform we select (it will take an argument of data from that radio) */
    if (data.value == 'custom') {
        document.querySelector('.custom_platform_span').style.display = 'block'
        document.querySelector('.selected_platform').value = data.value

        // adding input tag in the `custom_platform_span` span tag
        document.querySelector('.custom_platform_span').innerHTML ='<br> Custom platform: <input type="text" name="custom_platform" placeholder="Type custom platform name" required>'
    } else {
        document.querySelector('.custom_platform_span').style.display = 'none'
        document.querySelector('.selected_platform').value = data.value
        document.querySelector('.custom_platform_span').innerHTML = ''
    }
}


function validateCategoryValue(category_value) {
    // function for validating category data value on the front end page `new_item_1.html
    data = category_value.value

    // our list of categories from database
    categories = document.querySelector('.categories').value

    if (categories.includes(data)) {
        document.querySelector('.selected_category_error').style.display = 'none'
    } else {
        document.querySelector('.selected_category_error').style.display = 'block'
        document.querySelector('.selected_category_error').style.color = 'red'
        document.querySelector('.selected_category_error').style.fontStyle = 'italic'
        document.querySelector('.selected_category_error').style.fontWeight = 'bold'
    }
}


function validatePlatformValue(platform_value) {
    // function for validating platform data value on the front end page `new_item_1.html
    data = platform_value.value

    // our list of platforms from database
    platforms = document.querySelector('.platforms').value
    
    if (platforms.includes(data)) {
        document.querySelector('.selected_platform_error').style.display = 'none'
    } else {
        document.querySelector('.selected_platform_error').style.display = 'block'
        document.querySelector('.selected_platform_error').style.color = 'red'
        document.querySelector('.selected_platform_error').style.fontStyle = 'italic'
        document.querySelector('.selected_platform_error').style.fontWeight = 'bold'
    }
}


function validatePasscodeValue(field_two) {
    // function for validating passcode data value on the front end page (setting and updating passcode)
    field_one = document.querySelector('.passcode_ingredient').value

    if (field_two.value !== field_one) {
        document.querySelector('.selected_passcode_error').style.display = 'block'
        document.querySelector('.selected_passcode_error').style.color = 'red'
        document.querySelector('.selected_passcode_error').style.fontStyle = 'italic'
        document.querySelector('.selected_passcode_error').style.fontWeight = 'bold'
        document.querySelector('.selected_passcode_success').style.display = 'none'
    } else {
        document.querySelector('.selected_passcode_error').style.display = 'none'
        document.querySelector('.selected_passcode_success').style.display = 'block'
        document.querySelector('.selected_passcode_success').style.color = 'green'
        document.querySelector('.selected_passcode_success').style.fontWeight = 'bold'
    }
}
