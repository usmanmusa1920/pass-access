
// for showing menu side bar when it is closed
function showMenu(){
  x = window.matchMedia("(max-width: 700px)")
  if (x.matches){
    document.querySelector('.nav_panel').style.display = 'flex'
    document.querySelector('#show_menu').style.display = 'none'
    document.querySelector('#hide_menu').style.display = 'block'
    document.querySelector('.nav_panel').style.position = 'fixed'
    document.querySelector('.nav_panel').style.zIndex = '30'
    document.querySelector('.nav_panel').style.width = '70%'
    document.querySelector('.main').style.zIndex = '-5'
  }
  else{
    document.querySelector('.nav_panel').style.display = 'none'
    document.querySelector('.header').style.width = '100%'
    document.querySelector('.main').style.width = '100%'
    document.querySelector('#show_menu').style.display = 'none'
    document.querySelector('#hide_menu').style.display = 'block'
  }
}


// for hiding menu side bar when it is open
function hideMenu(){
  x = window.matchMedia("(max-width: 700px)")
  if (x.matches){
    document.querySelector('.nav_panel').style.display = 'none'
    document.querySelector('#show_menu').style.display = 'block'
    document.querySelector('#hide_menu').style.display = 'none'
    document.querySelector('.main').style.zIndex = '0'
  }
  else{
    document.querySelector('.nav_panel').style.display = 'flex'
    document.querySelector('.header').style.width = '80%'
    document.querySelector('.main').style.width = '80%'
    document.querySelector('#show_menu').style.display = 'block'
    document.querySelector('#hide_menu').style.display = 'none'
  }
}
// ===========================================================================================


// the below event will happen on the "new_item_1.html" page
// ===========================================================================================
// this function will fire when we select `social media` as our category when creating new item. What it does is, it will only display the `#plat_social' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category
function social_fun(data){
  document.querySelector('.selected_category').value = data.value
  document.querySelector('.selected_platform').value = null
  document.querySelector('#plat_social').style.display = 'block'
  document.querySelector('#plat_cloud').style.display = 'none'
  document.querySelector('#plat_card').style.display = 'none'
  document.querySelector('#plat_other').style.display = 'none'
  document.querySelector('.selected_platform_span').style.display = 'block'
}


// this function will fire when we select `cloud` as our category when creating new item. What it does is, it will only display the `#plat_cloud' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category
function cloud_fun(data){
  document.querySelector('.selected_category').value = data.value
  document.querySelector('.selected_platform').value = null
  document.querySelector('#plat_social').style.display = 'none'
  document.querySelector('#plat_cloud').style.display = 'block'
  document.querySelector('#plat_card').style.display = 'none'
  document.querySelector('#plat_other').style.display = 'none'
  document.querySelector('.selected_platform_span').style.display = 'block'
}


// this function will fire when we select `card` as our category when creating new item. What it does is, it will only display the `#plat_card' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category
function card_fun(data){
  document.querySelector('.selected_category').value = data.value
  document.querySelector('.selected_platform').value = null
  document.querySelector('#plat_social').style.display = 'none'
  document.querySelector('#plat_cloud').style.display = 'none'
  document.querySelector('#plat_card').style.display = 'block'
  document.querySelector('#plat_other').style.display = 'none'
  document.querySelector('.selected_platform_span').style.display = 'block'
}


// this function will fire when we select `other` as our category when creating new item. What it does is, it will only display the `#plat_other' div while making others display none, also making the `.selecte_platform` fields to empty always to avoid unnecessary data value of the category platform. And it set the value of the `.selected_category` fields to the value of the selected category
function other_fun(data){
  document.querySelector('.selected_category').value = data.value
  document.querySelector('.selected_platform').value = null
  document.querySelector('#plat_social').style.display = 'none'
  document.querySelector('#plat_cloud').style.display = 'none'
  document.querySelector('#plat_card').style.display = 'none'
  document.querySelector('#plat_other').style.display = 'block'
  document.querySelector('.selected_platform_span').style.display = 'block'
}
// ===========================================================================================


// the below event will happen on the "new_item_1.html" page also
// ===========================================================================================
// this function is for giving a value to our '.selected_platform`, of which of what so ever platform we select (it will take an argument of data from that radio)
function plat_select_fun(data){
  if (data.value == 'custom'){
    document.querySelector('.custom_platform_span').style.display = "block"
    document.querySelector('.selected_platform').value = data.value

    // adding input tag in the `custom_platform_span` span tag
    document.querySelector('.custom_platform_span').innerHTML = '<br> Custom platform: <input type="text" name="custom_platform" placeholder="Type custom platform name" required>'
  }
  else{
    document.querySelector('.custom_platform_span').style.display = "none"
    document.querySelector('.selected_platform').value = data.value
    document.querySelector('.custom_platform_span').innerHTML = ''
  }
}
// ===========================================================================================


// ===========================================================================================
// validating category data value on the front end page
function validateCategoryValue(category_value){
  data = category_value.value
  if (data !== 'social media' && data !== 'cloud' && data !== 'credit card' && data !== 'other'){
    document.querySelector('.selected_category_error').style.display = 'block'
    document.querySelector('.selected_category_error').style.color = 'red'
    document.querySelector('.selected_category_error').style.fontStyle = 'italic'
    document.querySelector('.selected_category_error').style.fontWeight = 'bold'
  }
  else{
    document.querySelector('.selected_category_error').style.display = 'none'
  }
}
// ===========================================================================================


// ===========================================================================================
// validating platform data value on the front end page
function validatePlatformValue(platform_value){
  data = platform_value.value
  platforms = ['aws', 'heroku', 'linode', 'facebook', 'twitter', 'instagram', 'linkedin', 'id card', 'store id', 'credit card', 'visa card', 'github', 'other']
  if (platforms.includes(data)){
    document.querySelector('.selected_platform_error').style.display = 'none'
  }
  else{
    document.querySelector('.selected_platform_error').style.display = 'block'
    document.querySelector('.selected_platform_error').style.color = 'red'
    document.querySelector('.selected_platform_error').style.fontStyle = 'italic'
    document.querySelector('.selected_platform_error').style.fontWeight = 'bold'
  }
}
// ===========================================================================================


// ===========================================================================================
// validating passcode data value on the front end page (setting passcode)
function validatePasscodeValue_set(field_two){
  field_one = document.querySelector('.passcode_ingredient').value
  
  if (field_two.value !== field_one){
    document.querySelector('.selected_passcode_error').style.display = 'block'
    document.querySelector('.selected_passcode_error').style.color = 'red'
    document.querySelector('.selected_passcode_error').style.fontStyle = 'italic'
    document.querySelector('.selected_passcode_error').style.fontWeight = 'bold'
    document.querySelector('.selected_passcode_success').style.display = 'none'
  }
  else{
    document.querySelector('.selected_passcode_error').style.display = 'none'
    document.querySelector('.selected_passcode_success').style.display = 'block'
    document.querySelector('.selected_passcode_success').style.color = 'green'
    document.querySelector('.selected_passcode_success').style.fontWeight = 'bold'
  }
}

// validating passcode data value on the front end page (updating passcode)
function validatePasscodeValue_update(field_two){
  field_one = document.querySelector('.old_passcode').value
  
  if (field_two.value !== field_one){
    document.querySelector('.selected_passcode_error').style.display = 'block'
    document.querySelector('.selected_passcode_error').style.color = 'red'
    document.querySelector('.selected_passcode_error').style.fontStyle = 'italic'
    document.querySelector('.selected_passcode_error').style.fontWeight = 'bold'
    document.querySelector('.selected_passcode_success').style.display = 'none'
  }
  else{
    document.querySelector('.selected_passcode_error').style.display = 'none'
    document.querySelector('.selected_passcode_success').style.display = 'block'
    document.querySelector('.selected_passcode_success').style.color = 'green'
    document.querySelector('.selected_passcode_success').style.fontWeight = 'bold'
  }
}
// ===========================================================================================


// function searchPlus(){
//   reg = /^\+[0-9]+$/
//   field = document.querySelector('#phone').value
//   // if (field.indexOf('+') == -1 || field[0] != '+' || field.indexOf('+') != 0){
//   if (field.match(reg)){
//     document.querySelector('.error').style.display = 'none'
//   }else{
//     document.querySelector('.error').style.display = 'block'
//     document.querySelector('.error').style.backgroundColor = 'white'
//     document.querySelector('.error').style.padding = '7px'
//     document.querySelector('.error').style.borderRadius = '3px'
//     document.querySelector('.error').style.color = 'red'
//   }
//   if(field.length < 13){
//     document.querySelector('.note').style.display = 'block'
//     document.querySelector('.note').style.backgroundColor = 'white'
//     document.querySelector('.note').style.padding = '5px'
//     document.querySelector('.note').style.marginTop = '3px'
//     document.querySelector('.note').style.borderRadius = '2px'
//     document.querySelector('.note').style.color = 'green'
//     return false;
//   }else{
//     document.querySelector('.note').style.display = 'none'
//   }
// }
