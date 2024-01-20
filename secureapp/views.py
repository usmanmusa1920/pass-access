# -*- coding: utf-8 -*-
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from .models import (
    Platform,
    Category,
    SecureItemInfo,
    ItemSecretIngredient,
    ItemSecret
)
from .forms import (
    SecureItemInfoForm_1,
    SecureItemInfoForm_2
)
from account.models import PassCode
from account.default import general_context
from toolkit import (
    check_user_passcode_set,
    passcode_required,
    InformationSecurity,
    MixinTrick
)


User = get_user_model()


@check_user_passcode_set(flash_for='item')
@passcode_required
def new_item(request):
    """First page for saving new item"""

    site_platform = Platform.objects.all()
    site_categories = Category.objects.all()
    
    # making list of platform, by using list comprehension. By default it will
    # return a tuples of (id, timestamp, platform_key, platform_value, category_id),
    # so we slice the fourth index `i[4]` which is the platform_value
    # l_platform = [i[4] for i in Platform.objects.values_list()]
    l_platform = [i['platform_value'] for i in Platform.objects.values_list().all().values()]
    
    # appending `custom`` in the `l_platform` list, because we did not added it directly into our database, to avoid being categorize into a category. Which will make us do alot if we add it there
    l_platform.append('custom')
    
    # making list of category, by using list comprehension. By default it will
    # return a tuples of (id, timestamp, category_key, category_value),
    # so we slice the third index `i[3]` which is the category_value
    # l_category = [i[3] for i in Category.objects.values_list()]
    l_category = [i['category_value'] for i in Category.objects.values_list().all().values()]
    
    # our default visibility list
    l_visibility = ['private', 'team', 'organisation']
    
    if request.method == 'POST':
        form = SecureItemInfoForm_1(request.POST)
        item_label = request.POST['i_label']

        # validating item label
        validate_label = SecureItemInfo.objects.filter(
            i_label=item_label, i_owner=request.user.passcode).first()
        if validate_label:
            flash_msg.warning(
                request, f'You already save an item with this label `{item_label}`')
            
        if form.is_valid():
            # Items values from html template
            item_category = form.cleaned_data.get("selected_category")
            item_platform = form.cleaned_data.get("selected_platform")
            item_custom_platform = form.cleaned_data.get("custom_platform")
            item_visibility = form.cleaned_data.get("visibility")
            
            context = {
                'item_category': item_category,
                'item_visibility': item_visibility,
                'item_platform': item_platform,
                'item_custom_platform': item_custom_platform,
                'item_label': item_label,
                
                'site_categories': site_categories,
                'site_platform': site_platform,
                'general_context': general_context(request),
            }
            
            # Checking for whether if a user edited the hidden fields by inspecting the page
            if item_visibility not in l_visibility:
                context = {
                    'form': form,
                    'site_categories': site_categories,
                    'site_platform': site_platform,
                    'l_platform': l_platform,
                    'l_category': l_category,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your visibility field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            
            if item_category not in l_category:
                context = {
                    'form': form,
                    'site_categories': site_categories,
                    'site_platform': site_platform,
                    'l_platform': l_platform,
                    'l_category': l_category,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your category field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            
            if item_platform not in l_platform:
                context = {
                    'form': form,
                    'site_categories': site_categories,
                    'site_platform': site_platform,
                    'l_platform': l_platform,
                    'l_category': l_category,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your platform field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            return render(request, 'secureapp/new_item_2.html', context)
    else:
        form = SecureItemInfoForm_1()

    context = {
        'form': form,
        'site_categories': site_categories,
        'site_platform': site_platform,
        'l_platform': l_platform,
        'l_category': l_category,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/new_item_1.html', context)


@check_user_passcode_set(flash_for='item')
@passcode_required
def new_item_fields(request):
    """Second page for saving new item"""

    the_i_owner = PassCode.objects.get(id=request.user.passcode.id)
    
    # making list of platform, by using list comprehension. By default it will
    # return a tuples of (id, timestamp, platform_key, platform_value, category_id),
    # so we slice the fourth index `i[4]` which is the platform_value
    # l_platform = [i[4] for i in Platform.objects.values_list()]
    l_platform = [i['platform_value'] for i in Platform.objects.values_list().all().values()]
    
    # appending `custom`` in the `l_platform` list, because we did not added it directly into our database, to avoid being categorize into a category. Which will make us do alot if we add it there
    l_platform.append('custom')
    
    # making list of category, by using list comprehension. By default it will
    # return a tuples of (id, timestamp, category_key, category_value),
    # so we slice the third index `i[3]` which is the category_value
    # l_category = [i[3] for i in Category.objects.values_list()]
    l_category = [i['category_value'] for i in Category.objects.values_list().all().values()]
    
    # our default visibility list
    l_visibility = ['private', 'team', 'organisation']
    
    if request.method == 'POST':
        form = SecureItemInfoForm_2(request.POST)

        if form.is_valid():
            # Items values from html template
            i_label = form.cleaned_data.get('i_label')
            i_category = form.cleaned_data.get("category")
            i_platform = form.cleaned_data.get("platform")
            i_custom_platform = form.cleaned_data.get("custom_platform")
            visibility = form.cleaned_data.get("visibility")
            
            # Checking for whether if a user edited the hidden fields by inspecting the page
            if visibility not in l_visibility:
                context = {
                    'form': form,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your visibility field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            
            if i_category not in l_category:
                context = {
                    'form': form,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your category field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            
            if i_platform not in l_platform:
                context = {
                    'form': form,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'May be you edited your platform field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            
            # fields for social
            i_username = form.cleaned_data.get('i_username')
            i_phone = form.cleaned_data['i_phone']
            i_email = form.cleaned_data['i_email']
            i_password = form.cleaned_data['i_password']
            
            # fields for cloud
            i_passphrase = form.cleaned_data['i_passphrase']
            i_api = form.cleaned_data['i_api']
            i_ssh_key_pub = form.cleaned_data['i_ssh_key_pub']
            i_ssh_key_prt = form.cleaned_data['i_ssh_key_prt']
            
            # fields for card
            i_card_no = form.cleaned_data['i_card_no']
            i_card_valid_range = form.cleaned_data['i_card_valid_range']
            i_card_ccv = form.cleaned_data['i_card_ccv']
            i_card_pin = form.cleaned_data['i_card_pin']
            
            # checking if all the fields are empty
            if i_username == '' and i_phone == None and i_email == None and i_password == None and i_passphrase == None and i_api == None and i_ssh_key_pub == None and i_ssh_key_prt == None and i_card_no == None and i_card_valid_range == None and i_card_ccv == None and i_card_pin == None:
                form = SecureItemInfoForm_2()
                context = {
                    'form': form,
                    'general_context': general_context(request),
                }
                flash_msg.warning(
                    request, f'All fields can\'t be empty, try again')
                return redirect('secureapp:new_item')
            
            # calling our encryption class and it's ancesstors
            _BASE_ = InformationSecurity()
            _private_ = _BASE_.crypt_key_32  # private key
            fernet_cls = _BASE_.f_cls  # the fernet class
            # randomly generated salt for pbkdf2_hmac hashing
            _salt_generation_ = _BASE_.the_key()
            
            # These are items public keys, and we are by passing them,
            # if an item is an empty space `''` or is `None`, else we will encrypt it
            if i_username != '' and i_username != None:
                i_username_encrypt_info = _BASE_.encrypt_info(i_username, fernet_cls)
            if i_phone != '' and i_phone != None:
                i_phone_encrypt_info = _BASE_.encrypt_info(i_phone, fernet_cls)
            if i_email != '' and i_email != None:
                i_email_encrypt_info = _BASE_.encrypt_info(i_email, fernet_cls)
            if i_password != '' and i_password != None:
                i_password_encrypt_info = _BASE_.encrypt_info(i_password, fernet_cls)
            if i_passphrase != '' and i_passphrase != None:
                i_passphrase_encrypt_info = _BASE_.encrypt_info(i_passphrase, fernet_cls)
            if i_api != '' and i_api != None:
                i_api_encrypt_info = _BASE_.encrypt_info(i_api, fernet_cls)
            if i_ssh_key_pub != '' and i_ssh_key_pub != None:
                i_ssh_key_pub_encrypt_info = _BASE_.encrypt_info(i_ssh_key_pub, fernet_cls)
            if i_ssh_key_prt != '' and i_ssh_key_prt != None:
                i_ssh_key_prt_encrypt_info = _BASE_.encrypt_info(i_ssh_key_prt, fernet_cls)
            if i_card_no != '' and i_card_no != None:
                i_card_no_encrypt_info = _BASE_.encrypt_info(i_card_no, fernet_cls)
            if i_card_valid_range != '' and i_card_valid_range != None:
                i_card_valid_range_encrypt_info = _BASE_.encrypt_info(i_card_valid_range, fernet_cls)
            if i_card_ccv != '' and i_card_ccv != None:
                i_card_ccv_encrypt_info = _BASE_.encrypt_info(i_card_ccv, fernet_cls)
            if i_card_pin != '' and i_card_pin != None:
                i_card_pin_encrypt_info = _BASE_.encrypt_info(i_card_pin, fernet_cls)
                
            # generating iteration for our item, i.e iteration number (3 digit e.g, 212)
            _fast_itter_ = _BASE_.fast_iteration
            # get hash method, return a list of [hash_result, secure_ingredient]
            _get_hash_ = _BASE_.get_hash(
                _salt_generation_, _fast_itter_, _private_)
            sign_hash = _get_hash_[0]  # second hash
            # (salt, itter, hash_result)
            _ingredient_ = _get_hash_[1]
            _salt_itter_ = _ingredient_[:-len(sign_hash)]
            sign_salt = _salt_itter_[:-3]
            sign_iteration = _salt_itter_[len(sign_salt):]
            sign_return = MixinTrick.sign_mix(
                sign_iteration, sign_hash, sign_salt, _private_)
            # OUTPUT:
            #   the_key = sign_return[0],
            #   the_hash = sign_return[1],
            #   the_private = sign_return[2],
            #   ingredient = sign_return[3]
            
            # assigning the required item fields to their instances
            instance = form.save(commit=False)
            instance.i_owner = the_i_owner
            instance.i_label = i_label
            instance.category = i_category
            instance.platform = i_platform
            # also lower casing the custom platform
            if i_custom_platform != None or i_custom_platform == '':
                instance.custom_platform = i_custom_platform.lower()
            else:
                instance.custom_platform = i_platform.lower()
            instance.visibility = visibility
            
            # checking to see if whether an item is not an empty space `''` or is `None`,
            # before we decode it and assign it to the instance of the field of which we
            # will save in a database
            if i_username != '' and i_username != None:
                instance.i_username = i_username_encrypt_info.decode()
            if i_phone != '' and i_phone != None:
                instance.i_phone = i_phone_encrypt_info.decode()
            if i_email != '' and i_email != None:
                instance.i_email = i_email_encrypt_info.decode()
            if i_password != '' and i_password != None:
                instance.i_password = i_password_encrypt_info.decode()
            if i_passphrase != '' and i_passphrase != None:
                instance.i_passphrase = i_passphrase_encrypt_info.decode()
            if i_api != '' and i_api != None:
                instance.i_api = i_api_encrypt_info.decode()
            if i_ssh_key_pub != '' and i_ssh_key_pub != None:
                instance.i_ssh_key_pub = i_ssh_key_pub_encrypt_info.decode()
            if i_ssh_key_prt != '' and i_ssh_key_prt != None:
                instance.i_ssh_key_prt = i_ssh_key_prt_encrypt_info.decode()
            if i_card_no != '' and i_card_no != None:
                instance.i_card_no = i_card_no_encrypt_info.decode()
            if i_card_valid_range != '' and i_card_valid_range != None:
                instance.i_card_valid_range = i_card_valid_range_encrypt_info.decode()
            if i_card_ccv != '' and i_card_ccv != None:
                instance.i_card_ccv = i_card_ccv_encrypt_info.decode()
            if i_card_pin != '' and i_card_pin != None:
                instance.i_card_pin = i_card_pin_encrypt_info.decode()
            instance.the_key = sign_return[0]
            instance.save()
            
            # for secret
            instance_secret = ItemSecret(
                rely_on=instance, the_hash=sign_return[1], the_private=sign_return[2])
            instance_secret.save()
            
            # for ingredient
            instance_ingedient = ItemSecretIngredient(
                rely_on=instance, ingredient=sign_return[3])
            instance_ingedient.save()
            return redirect(reverse('secureapp:item_info', kwargs={'item_id': instance.id}))
    else:
        form = SecureItemInfoForm_2()

    context = {
        'form': form,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/new_item_2.html', context)


@passcode_required
def item_info(request, item_id):
    """Item infomation view"""

    item_unveil_info = SecureItemInfo.objects.get(id=item_id)  # the item info

    # stored previous last review in other to render in template
    last_review = item_unveil_info.last_review

    # saving current time as last review
    item_unveil_info.last_review = timezone.now
    item_unveil_info.save()

    if request.user != item_unveil_info.i_owner.owner:
        return False
    item_unveil_secret = ItemSecret.objects.get(
        rely_on_id=item_unveil_info.id)  # secret
    item_unveil_ingre = ItemSecretIngredient.objects.get(
        rely_on_id=item_unveil_info.id)  # ingredient
    
    # [(itter * 2) - random.randint(1, 10, 2)] + gen_salt + key + hash
    item_key = item_unveil_info.the_key
    i_username_pub = item_unveil_info.i_username  # username public key
    i_phone_pub = item_unveil_info.i_phone  # phone public key
    i_email_pub = item_unveil_info.i_email  # email public key
    i_password_pub = item_unveil_info.i_password  # password public key
    i_passphrase_pub = item_unveil_info.i_passphrase  # passphrase public key
    i_api_pub = item_unveil_info.i_api  # api public key
    i_ssh_key_pub_pub = item_unveil_info.i_ssh_key_pub  # ssh_key_pub public key
    i_ssh_key_prt_pub = item_unveil_info.i_ssh_key_prt  # ssh_key_prt public key
    i_card_no_pub = item_unveil_info.i_card_no  # card_no public key
    # card_valid_range public key
    i_card_valid_range_pub = item_unveil_info.i_card_valid_range
    i_card_ccv_pub = item_unveil_info.i_card_ccv  # card_ccv public key
    i_card_pin_pub = item_unveil_info.i_card_pin  # card_pin public key
    
    # [(itter * 2) + random.randint(1, 9)] + hash + (itter * 2) + "".join(random.sample(select_from_me, 1))
    item_the_hash = item_unveil_secret.the_hash
    # [(itter - random.randint(1, 10)) * 2] + private + hash + gen_salt
    item_the_private = item_unveil_secret.the_private
    # [(itter - 13) * 2] + key + hash + [(itter * 2) - random.randint(3, 8)]
    item_ingredient = item_unveil_ingre.ingredient
    unsign_return = MixinTrick.unsign_mix(item_key, item_the_hash, item_the_private, item_ingredient)
    # OUTPUT:
    #   real salt = unsign_return[0],
    #   real iteration = unsign_return[1],
    #   real hash = unsign_return[2],
    #   real private key = unsign_return[3]
    
    # calling our encryption class
    _BASE_ = InformationSecurity()
    
    # in the following `i_<item_field>_pub` fields we check for the field
    # of each to see if it is not empty or it is not None, and if it is not
    # None and it is not empty we decrypt it by using the item field (for each field)
    # public key and the item private key (which is for all fields)
    # for username
    if i_username_pub != '' and i_username_pub != None:
        decrypt_i_username = _BASE_.decrypt_info(
            i_username_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_username = ''
    # for phone
    if i_phone_pub != '' and i_phone_pub != None:
        decrypt_i_phone = _BASE_.decrypt_info(
            i_phone_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_phone = ''
    # for email
    if i_email_pub != '' and i_email_pub != None:
        decrypt_i_email = _BASE_.decrypt_info(
            i_email_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_email = ''
    # for password
    if i_password_pub != '' and i_password_pub != None:
        decrypt_i_password = _BASE_.decrypt_info(
            i_password_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_password = ''
    # for passphrase
    if i_passphrase_pub != '' and i_passphrase_pub != None:
        decrypt_i_passphrase = _BASE_.decrypt_info(
            i_passphrase_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_passphrase = ''
    # for api
    if i_api_pub != '' and i_api_pub != None:
        decrypt_i_api = _BASE_.decrypt_info(
            i_api_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_api = ''
    # for ssh_key_pub
    if i_ssh_key_pub_pub != '' and i_ssh_key_pub_pub != None:
        decrypt_i_ssh_key_pub = _BASE_.decrypt_info(
            i_ssh_key_pub_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_ssh_key_pub = ''
    # for ssh_key_prt
    if i_ssh_key_prt_pub != '' and i_ssh_key_prt_pub != None:
        decrypt_i_ssh_key_prt = _BASE_.decrypt_info(
            i_ssh_key_prt_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_ssh_key_prt = ''
    # for card_no
    if i_card_no_pub != '' and i_card_no_pub != None:
        decrypt_i_card_no = _BASE_.decrypt_info(
            i_card_no_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_card_no = ''
    # for card_valid_range
    if i_card_valid_range_pub != '' and i_card_valid_range_pub != None:
        decrypt_i_card_valid_range = _BASE_.decrypt_info(
            i_card_valid_range_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_card_valid_range = ''
    # for card_ccv
    if i_card_ccv_pub != '' and i_card_ccv_pub != None:
        decrypt_i_card_ccv = _BASE_.decrypt_info(
            i_card_ccv_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_card_ccv = ''
    # for card_pin
    if i_card_pin_pub != '' and i_card_pin_pub != None:
        decrypt_i_card_pin = _BASE_.decrypt_info(
            i_card_pin_pub.encode('utf-8'), unsign_return[3])
    else:
        decrypt_i_card_pin = ''
        
    context = {
        'item_unveil_info': item_unveil_info,
        'last_review': last_review,
        'decrypt_i_username': decrypt_i_username,
        'decrypt_i_phone': decrypt_i_phone,
        'decrypt_i_email': decrypt_i_email,
        'decrypt_i_password': decrypt_i_password,
        'decrypt_i_passphrase': decrypt_i_passphrase,
        'decrypt_i_api': decrypt_i_api,
        'decrypt_i_ssh_key_pub': decrypt_i_ssh_key_pub,
        'decrypt_i_ssh_key_prt': decrypt_i_ssh_key_prt,
        'decrypt_i_card_no': decrypt_i_card_no,
        'decrypt_i_card_valid_range': decrypt_i_card_valid_range,
        'decrypt_i_card_ccv': decrypt_i_card_ccv,
        'decrypt_i_card_pin': decrypt_i_card_pin,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/item_info.html', context)


@passcode_required
def search_trusted_user(request, item_id):
    """Search trusted user"""

    # This search_panel variable is the name attribute of search input field of this view template, and also it is a variable name included when paginating
    search_panel = request.GET.get('search_trusted_user')
    item = SecureItemInfo.objects.get(id=item_id)
    try:
        # This is a filter that filter user matching a giving query.
        search_result = User.objects.filter(
            Q(first_name__exact=search_panel) | Q(first_name__iexact=search_panel) | Q(first_name__startswith=search_panel) | Q(first_name__istartswith=search_panel) | Q(first_name__contains=search_panel) | Q(first_name__icontains=search_panel) | Q(first_name__endswith=search_panel) | Q(first_name__iendswith=search_panel) |

            Q(last_name__exact=search_panel) | Q(last_name__iexact=search_panel) | Q(last_name__startswith=search_panel) | Q(last_name__istartswith=search_panel) | Q(last_name__contains=search_panel) | Q(last_name__icontains=search_panel) | Q(last_name__endswith=search_panel) | Q(last_name__iendswith=search_panel) |

            Q(username__exact=search_panel) | Q(username__iexact=search_panel) | Q(username__startswith=search_panel) | Q(username__istartswith=search_panel) | Q(username__contains=search_panel) | Q(
                username__icontains=search_panel) | Q(username__endswith=search_panel) | Q(username__iendswith=search_panel) | Q(phone_number=search_panel) | Q(email=search_panel)
        ).order_by('-date_joined')
    except:
        # This is a filter that filter user matching a giving query.
        search_result = User.objects.filter(Q(first_name=search_panel) | Q(last_name=search_panel) | Q(
            username=search_panel) | Q(phone_number=search_panel) | Q(email=search_panel)).order_by('-date_joined')
    paginator = Paginator(search_result, 30)
    page = request.GET.get('page')
    searches = paginator.get_page(page)

    context = {
        'item': item,
        'searches': searches,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/add_trusted_user.html', context)


@passcode_required
def add_trusted_user(request, item_id, user_id):
    """Add trusted user view"""

    trusted_user = User.objects.get(id=user_id)
    item = SecureItemInfo.objects.get(id=item_id)
    item.trusted_user.add(trusted_user)
    
    flash_msg.success(
        request, f'You added {trusted_user.first_name} as trusted user in your item ({item.custom_platform})')
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))


@passcode_required
def remove_trusted_user(request, item_id, user_id):
    """Remove trusted user view"""

    trusted_user = User.objects.get(id=user_id)
    item = SecureItemInfo.objects.get(id=item_id)
    item.trusted_user.remove(trusted_user)
    
    flash_msg.warning(
        request, f'You remove {trusted_user.first_name} as trusted user in your item ({item.custom_platform})')
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))


@passcode_required
def remove_all_trusted_user(request, item_id):
    """Remove all trusted user view"""

    item = SecureItemInfo.objects.get(id=item_id)

    if request.method == 'POST':
        for trust_user in item.trusted_user.all():
            item.trusted_user.remove(trust_user)
        flash_msg.warning(
            request, f'You remove all trusted user in your item ({item.custom_platform})')
        return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))
    
    context = {
        'item': item,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/remove_all_trusted_user.html', context)


@passcode_required
def delete_item(request, item_id):
    """Delete item view"""
    
    item = SecureItemInfo.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        flash_msg.success(request, f'You successfully deleted `{item.i_label}` item')
        return redirect('auth:landing')
    
    context = {
        'item': item,
        'general_context': general_context(request),
    }
    return render(request, 'secureapp/delete_item.html', context)
