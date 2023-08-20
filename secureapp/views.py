from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from .models import (
    Platform, Category, SecureItemInfo, ItemSecretIngredient, ItemSecret
)
from .forms import (
    PassCodeForm, AccountPassCodeForm, SecureItemInfoForm_1, SecureItemInfoForm_2
)
from account.models import PassCode
from toolkit.decorators import check_user_pascode_set
from toolkit import PasscodeSecurity, InformationSecurity, MixinTrick


User = get_user_model()


def home(request):
    the_year = datetime.today().year
    if request.user.is_authenticated:
        user_items = SecureItemInfo.objects.filter(
            i_owner=request.user.passcode).order_by('-date_created')[:10]
        context = {
            'user_items': user_items,
            'the_year': the_year,
        }
        return render(request, 'secureapp/home.html', context)
    context = {
        'the_year': the_year,
    }
    return render(request, 'account/landing.html', context)


@login_required
def searchTrustedUser(request, item_id):
    # This search_panel variable is the name attribute of search input field of this view template, and also it is a variable name included when paginating
    p = '1999'
    print(p)
    search_panel = request.GET.get('search_trusted')
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
    # form = searchTrustedForm(request.POST)
    paginator = Paginator(search_result, 30)
    page = request.GET.get('page')
    searches = paginator.get_page(page)
    context = {
        'searches': searches,
        'p': p,
    }
    # data = form.cleaned_data.get('search_value')
    # s_user = User.objects.get(id=user_id)
    # flash_msg.warning(request, f'You added {u_t.first_name} as trusted user in your item ({i_id.custom_platform})')
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))
    # return render(request, 'secureapp/se.html', context)


@login_required
def addTrustedUser(request, item_id, user_id):
    u_t = User.objects.get(id=user_id)
    i_id = SecureItemInfo.objects.get(id=item_id)
    i_id.trusted_user.add(u_t)

    flash_msg.success(
        request, f'You added {u_t.first_name} as trusted user in your item ({i_id.custom_platform})')
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))


@login_required
def removeTrustedUser(request, item_id, user_id):
    u_t = User.objects.get(id=user_id)
    i_id = SecureItemInfo.objects.get(id=item_id)
    i_id.trusted_user.remove(u_t)

    flash_msg.warning(
        request, f'You remove {u_t.first_name} as trusted user in your item ({i_id.custom_platform})')
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))


@login_required
def searchTrustedUser(request, item_id):
    return redirect(reverse('secureapp:item_info', kwargs={'item_id': item_id}))


@login_required
def itemInfo(request, item_id):
    item_unveil_info = SecureItemInfo.objects.get(id=item_id)  # the item info
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
    my_result = MixinTrick._3_to_3(item_key, item_the_hash,
                             item_the_private, item_ingredient)
    # OUTPUT:
    #   real salt = my_result[0],
    #   real iteration = my_result[1],
    #   real hash = my_result[2],
    #   real private key = my_result[3]

    # calling our encryption class
    _BASE_ = InformationSecurity()

    """
    in the following `i_<item_field>_pub` fields we check for the field
    of each to see if it is not empty or it is not None, and if it is not
    None and it is not empty we decrypt it by using the item field (for each field)
    public key and the item private key (which is for all fields)
    """
    # for username
    if i_username_pub != '' and i_username_pub != None:
        decrypt_i_username = _BASE_.decrypt_info(
            i_username_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_username = ''
    # for phone
    if i_phone_pub != '' and i_phone_pub != None:
        decrypt_i_phone = _BASE_.decrypt_info(
            i_phone_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_phone = ''
    # for email
    if i_email_pub != '' and i_email_pub != None:
        decrypt_i_email = _BASE_.decrypt_info(
            i_email_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_email = ''
    # for password
    if i_password_pub != '' and i_password_pub != None:
        decrypt_i_password = _BASE_.decrypt_info(
            i_password_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_password = ''
    # for passphrase
    if i_passphrase_pub != '' and i_passphrase_pub != None:
        decrypt_i_passphrase = _BASE_.decrypt_info(
            i_passphrase_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_passphrase = ''
    # for api
    if i_api_pub != '' and i_api_pub != None:
        decrypt_i_api = _BASE_.decrypt_info(
            i_api_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_api = ''
    # for ssh_key_pub
    if i_ssh_key_pub_pub != '' and i_ssh_key_pub_pub != None:
        decrypt_i_ssh_key_pub = _BASE_.decrypt_info(
            i_ssh_key_pub_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_ssh_key_pub = ''
    # for ssh_key_prt
    if i_ssh_key_prt_pub != '' and i_ssh_key_prt_pub != None:
        decrypt_i_ssh_key_prt = _BASE_.decrypt_info(
            i_ssh_key_prt_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_ssh_key_prt = ''
    # for card_no
    if i_card_no_pub != '' and i_card_no_pub != None:
        decrypt_i_card_no = _BASE_.decrypt_info(
            i_card_no_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_card_no = ''
    # for card_valid_range
    if i_card_valid_range_pub != '' and i_card_valid_range_pub != None:
        decrypt_i_card_valid_range = _BASE_.decrypt_info(
            i_card_valid_range_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_card_valid_range = ''
    # for card_ccv
    if i_card_ccv_pub != '' and i_card_ccv_pub != None:
        decrypt_i_card_ccv = _BASE_.decrypt_info(
            i_card_ccv_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_card_ccv = ''
    # for card_pin
    if i_card_pin_pub != '' and i_card_pin_pub != None:
        decrypt_i_card_pin = _BASE_.decrypt_info(
            i_card_pin_pub.encode('utf-8'), my_result[3])
    else:
        decrypt_i_card_pin = ''

    context = {
        'item_unveil_info': item_unveil_info,
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
    }
    return render(request, 'secureapp/item_info.html', context)


@login_required
def setPassCode(request):
    user_email = request.user.email

    if request.method == 'POST':
        """
        The acc_form is not going to be use in HTML template,
        it will be use only within this function, so that to save it (second hash i.e passcode_hash)
        to the custome user model (UserAccount)
        """
        acc_form = AccountPassCodeForm(request.POST, instance=request.user)
        pass_form = PassCodeForm(request.POST, instance=request.user.passcode)

        if pass_form.is_valid() and acc_form.is_valid():
            """getting data from HTML template, only for pass_form"""
            verify_user_email = pass_form.cleaned_data.get('verify_email')
            verify_new_passcode = pass_form.cleaned_data.get('verify_passcode')
            verify_new_passcode_again = pass_form.cleaned_data.get(
                'passcode_ingredient')

            """authenticating email address"""
            if verify_user_email != user_email:
                flash_msg.warning(
                    request, f'Email address you enter didn`t match with your account email address')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/set_passcode.html', {'pass_form': pass_form})

            """length Validation of the two fields"""
            if len(verify_new_passcode) < 8 or len(verify_new_passcode_again) < 8:
                flash_msg.warning(request, f'Your passcode length must be at least 8 character')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/set_passcode.html', {'pass_form': pass_form})

            """Validating the two fields"""
            if verify_new_passcode != verify_new_passcode_again:
                flash_msg.warning(request, f'The two passcode field mis-match, try again')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/set_passcode.html', {'pass_form': pass_form})

            """committing the two forms save method to false"""
            instance_1 = pass_form.save(commit=False)
            instance_2 = acc_form.save(commit=False)

            """invoking the PasscodeSecurity class"""
            auth_pass = PasscodeSecurity()
            salt_q = auth_pass.passcode_salt  # salt of the passcode
            iter_q = auth_pass.passcode_iteration  # iteration of the passcode

            # the key of the passcode
            auth_result = auth_pass.get_hash(salt_q, iter_q, verify_new_passcode_again)
            # second hash after been encoded using base64
            hashed_passcode = auth_result[0]
            # the ingredient of the hash (salt + iteration + second_hash) respectively
            pass_ingredient = auth_result[1]

            """assigning instances value"""
            instance_1.passcode_ingredient = pass_ingredient
            instance_2.passcode_hash = hashed_passcode

            """saving the instances"""
            instance_1.save()
            instance_2.save()
            flash_msg.success(request, f'Your passcode is set just now!')
            return redirect('secureapp:home')
    else:
        pass_form = PassCodeForm(instance=request.user.passcode)
    context = {
        'pass_form': pass_form,
    }
    return render(request, 'secureapp/set_passcode.html', context)


@check_user_pascode_set(flash_for='update')
def UpdatePassCode(request):
    """function for updating user passcode"""

    user_email = request.user.email
    
    """ingredient (salt + iteration + second hash) respectively"""
    old_ingredient = request.user.passcode.passcode_ingredient

    """(second hash) from custome user model"""
    real_hash = request.user.passcode_hash
    """(second hash) slicing it from old_ingredient"""
    slice_hash = old_ingredient[-len(real_hash):]

    """
    slicing ingredient from old_ingredient, starting from index zero to the actual length of the (real_hash) above
    """
    slice_ingre = old_ingredient[: -len(slice_hash)]

    """slicing iteration from the (slice_ingre) above from index -6 to the end"""
    slice_iter = slice_ingre[-6:]

    """slicing salt from the first index of the (slice_ingre) to index -6"""
    slice_salt = slice_ingre[: -6]

    if request.method == 'POST':
        """
        The acc_form is not going to be use in HTML template,
        it will be use only within this function, so that to renew (second hash i.e passcode_hash) in the custome user model (UserAccount)
        """
        acc_form = AccountPassCodeForm(request.POST, instance=request.user)
        pass_form = PassCodeForm(request.POST, instance=request.user.passcode)

        if pass_form.is_valid() and acc_form.is_valid():
            """Grabbing data from html template"""
            verify_user_email = pass_form.cleaned_data.get('verify_email')
            old_raw_passcode = pass_form.cleaned_data.get('old_passcode')
            # old_raw_passcode = request.POST['old_passcode']
            new_raw_passcode = pass_form.cleaned_data.get('passcode_ingredient')
            verify_new_passcode = pass_form.cleaned_data.get('verify_passcode')

            """authenticating email address"""
            if verify_user_email != user_email:
                flash_msg.warning(
                    request, f'Email address you enter didn`t match with your account email address')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/update_passcode.html', {'pass_form': pass_form})

            """length Validation of the three fields"""
            if len(old_raw_passcode) < 8 or len(new_raw_passcode) < 8 or len(verify_new_passcode) < 8:
                flash_msg.warning(request, f'Your passcode length must be at least 8 character')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/update_passcode.html', {'pass_form': pass_form})

            """
            The below confirm_* is use to authenticate the old passcode that a user claim (old_raw_passcode),
            and compare it with the one he/she want to change it (the one he/she is using, i.e `slice_ingre`).
            """
            confirm_auth = PasscodeSecurity()
            confirm_result = confirm_auth.get_hash(slice_salt, int(slice_iter), old_raw_passcode)
            confirm_passcode = confirm_result[0]
            confirm_ingredient = confirm_result[1][: -len(confirm_passcode)]

            """
            comparing the second hash (old), with the new second hash (compare one), like wise also;
            comparing the ingredient (old), with the new ingredient (compare one),
            both must match to what we assign to them, in other to pass to the next step
            """
            if slice_hash != confirm_passcode or slice_ingre != confirm_ingredient:
                flash_msg.warning(request, f'Your old passcode is incorrect')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/update_passcode.html', {'pass_form': pass_form})

            """authenticating two fields for new passcode"""
            if verify_new_passcode != new_raw_passcode:
                flash_msg.warning(request, f'The two passcode field mis-match, try again')
                pass_form = PassCodeForm(instance=request.user.passcode)
                return render(request, 'secureapp/update_passcode.html', {'pass_form': pass_form})

            """
            comparing the two html fields with each other, and comparing the old ingredient with the confirm one, for the renewal
            """
            if verify_new_passcode == new_raw_passcode and slice_ingre == confirm_ingredient:
                """invoking the PasscodeSecurity class"""
                renew_pass = PasscodeSecurity()
                new_salt = renew_pass.passcode_salt  # salt of the renew passcode
                new_iter = renew_pass.passcode_iteration  # iteration of  the renew passcode

                # the key of the passcode
                pass_result = renew_pass.get_hash(new_salt, new_iter, new_raw_passcode)
                # second hash after been encode using base64
                new_passcode = pass_result[0]
                # the ingredient of the hash (salt + iteration + second_hash) respectively
                new_ingredient = pass_result[1]

                """committing the two forms save method to false"""
                instance_1 = pass_form.save(commit=False)
                instance_2 = acc_form.save(commit=False)

                """assigning instances value"""
                instance_1.passcode_ingredient = new_ingredient
                instance_2.passcode_hash = new_passcode

                """saving instances"""
                instance_1.save()
                instance_2.save()

                flash_msg.success(request, f'Your passcode is updated')
                return redirect('secureapp:home')
    else:
        pass_form = PassCodeForm(instance=request.user.passcode)
    context = {
        'pass_form': pass_form,
    }
    return render(request, 'secureapp/update_passcode.html', context)


@check_user_pascode_set(flash_for='item')
def newItem(request):
    """First page for saving new item"""
    site_platform = Platform.objects.all()
    site_categories = Category.objects.all()

    """
    making list of platform, by using list comprehension. By default it will
    return a tuples of (id, timestamp, platform_key, platform_value, category_id),
    so we slice the fourth index `i[4]` which is the platform_value
    """
    # l_platform = [i[4] for i in Platform.objects.values_list()]
    l_platform = [i['platform_value'] for i in Platform.objects.values_list().all().values()]

    # appending `custom`` in the `l_platform` list, because we did not added it directly into our database, to avoid being categorize into a category. Which will make us do alot if we add it there
    l_platform.append('custom')

    """
    making list of category, by using list comprehension. By default it will
    return a tuples of (id, timestamp, category_key, category_value),
    so we slice the third index `i[3]` which is the category_value
    """
    # l_category = [i[3] for i in Category.objects.values_list()]
    l_category = [i['category_value'] for i in Category.objects.values_list().all().values()]

    # our default visibility list
    l_visibility = ['private', 'team', 'organisation']

    if request.method == 'POST':
        form = SecureItemInfoForm_1(request.POST)
        if form.is_valid():
            """Items values from html template"""
            item_label = form.cleaned_data.get("i_label")
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
            }

            """Checking for whether if a user edited the hidden fields by inspecting the page"""
            if item_visibility not in l_visibility:
                context = {
                    'form': form,
                    'site_categories': site_categories,
                    'site_platform': site_platform,
                    'l_platform': l_platform,
                    'l_category': l_category,
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
    }
    return render(request, 'secureapp/new_item_1.html', context)


@check_user_pascode_set(flash_for='item')
def newItemFields(request):
    """Second page for saving new item"""
    the_i_owner = PassCode.objects.get(id=request.user.passcode.id)

    """
    making list of platform, by using list comprehension. By default it will
    return a tuples of (id, timestamp, platform_key, platform_value, category_id),
    so we slice the fourth index `i[4]` which is the platform_value
    """
    # l_platform = [i[4] for i in Platform.objects.values_list()]
    l_platform = [i['platform_value'] for i in Platform.objects.values_list().all().values()]

    # appending `custom`` in the `l_platform` list, because we did not added it directly into our database, to avoid being categorize into a category. Which will make us do alot if we add it there
    l_platform.append('custom')

    """
    making list of category, by using list comprehension. By default it will
    return a tuples of (id, timestamp, category_key, category_value),
    so we slice the third index `i[3]` which is the category_value
    """
    # l_category = [i[3] for i in Category.objects.values_list()]
    l_category = [i['category_value'] for i in Category.objects.values_list().all().values()]

    # our default visibility list
    l_visibility = ['private', 'team', 'organisation']
    
    if request.method == 'POST':
        form = SecureItemInfoForm_2(request.POST)
        if form.is_valid():
            """Items values from html template"""
            i_label = form.cleaned_data.get('i_label')
            i_category = form.cleaned_data.get("category")
            i_platform = form.cleaned_data.get("platform")
            i_custom_platform = form.cleaned_data.get("custom_platform")
            visibility = form.cleaned_data.get("visibility")

            """Checking for whether if a user edited the hidden fields by inspecting the page"""
            if visibility not in l_visibility:
                context = {
                    'form': form,
                }
                flash_msg.warning(
                    request, f'May be you edited your visibility field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            if i_category not in l_category:
                context = {
                    'form': form,
                }
                flash_msg.warning(
                    request, f'May be you edited your category field(s), thats why we redirect you back')
                return render(request, 'secureapp/new_item_1.html', context)
            if i_platform not in l_platform:
                context = {
                    'form': form,
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
                }
                flash_msg.warning(
                    request, f'All fields can\'t be empty, try again')
                return redirect('secureapp:new_item')

            # calling our encryption class and it's ancesstors
            _BASE_ = InformationSecurity()
            ITEM_private = _BASE_.crypt_key_32  # private key
            fernet_base_class = _BASE_.f_cls  # the fernet class
            # randomly generated salt for pbkdf2_hmac hashing
            ITEM_salt_generation = _BASE_.the_key()

            """
            These are items public keys, and we are by passing them,
            if an item is an empty space `''` or is `None`, else we will encrypt it
            """
            if i_username != '' and i_username != None:
                i_username_encrypt_info = _BASE_.encrypt_info(i_username, fernet_base_class)
            if i_phone != '' and i_phone != None:
                i_phone_encrypt_info = _BASE_.encrypt_info(i_phone, fernet_base_class)
            if i_email != '' and i_email != None:
                i_email_encrypt_info = _BASE_.encrypt_info(i_email, fernet_base_class)
            if i_password != '' and i_password != None:
                i_password_encrypt_info = _BASE_.encrypt_info(i_password, fernet_base_class)
            if i_passphrase != '' and i_passphrase != None:
                i_passphrase_encrypt_info = _BASE_.encrypt_info(i_passphrase, fernet_base_class)
            if i_api != '' and i_api != None:
                i_api_encrypt_info = _BASE_.encrypt_info(i_api, fernet_base_class)
            if i_ssh_key_pub != '' and i_ssh_key_pub != None:
                i_ssh_key_pub_encrypt_info = _BASE_.encrypt_info(i_ssh_key_pub, fernet_base_class)
            if i_ssh_key_prt != '' and i_ssh_key_prt != None:
                i_ssh_key_prt_encrypt_info = _BASE_.encrypt_info(i_ssh_key_prt, fernet_base_class)
            if i_card_no != '' and i_card_no != None:
                i_card_no_encrypt_info = _BASE_.encrypt_info(i_card_no, fernet_base_class)
            if i_card_valid_range != '' and i_card_valid_range != None:
                i_card_valid_range_encrypt_info = _BASE_.encrypt_info(i_card_valid_range, fernet_base_class)
            if i_card_ccv != '' and i_card_ccv != None:
                i_card_ccv_encrypt_info = _BASE_.encrypt_info(i_card_ccv, fernet_base_class)
            if i_card_pin != '' and i_card_pin != None:
                i_card_pin_encrypt_info = _BASE_.encrypt_info(i_card_pin, fernet_base_class)

            # generating iteration for our item, i.e iteration number (3 digit e.g, 212)
            ITEM_get_iteration = _BASE_.fast_iteration
            # get hash method, return a list of [hash_result, secure_ingredient]
            ITEM_get_hash_info = _BASE_.get_hash(
                ITEM_salt_generation, ITEM_get_iteration, ITEM_private)
            ITEM_hash = ITEM_get_hash_info[0]  # second hash
            # (salt, itter, hash_result)
            ITEM_ingredient = ITEM_get_hash_info[1]
            ITEM_salt__itter = ITEM_ingredient[:-len(ITEM_hash)]
            ITEM_salt = ITEM_salt__itter[:-3]
            ITEM_iteration = ITEM_salt__itter[len(ITEM_salt):]
            INS_result = MixinTrick._instance_item_data(
                ITEM_iteration, ITEM_hash, ITEM_salt, ITEM_private)
            # OUTPUT:
            #   the_key = INS_result[0],
            #   the_hash = INS_result[1],
            #   the_private = INS_result[2],
            #   ingredient = INS_result[3]

            # assigning the required item fields to their instances
            instance = form.save(commit=False)
            instance.i_owner = the_i_owner
            instance.i_label = i_label
            instance.category = i_category
            instance.platform = i_platform
            # also lower casing the custom platform
            if i_custom_platform != None or i_custom_platform == '':
                instance.custom_platform = i_custom_platform.lower()
            instance.visibility = visibility

            """
            checking to see if whether an item is not an empty space `''` or is `None`,
            before we decode it and assign it to the instance of the field of which we
            will save in a database
            """
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
            instance.the_key = INS_result[0]
            instance.save()
            
            # for secret
            instance_secret = ItemSecret(
                rely_on=instance, the_hash=INS_result[1], the_private=INS_result[2])
            instance_secret.save()

            # for ingredient
            instance_ingedient = ItemSecretIngredient(
                rely_on=instance, ingredient=INS_result[3])
            instance_ingedient.save()
            return redirect(reverse('secureapp:item_info', kwargs={'item_id': instance.id}))
    else:
        form = SecureItemInfoForm_2()
    context = {
        'form': form,
    }
    return render(request, 'secureapp/new_item_2.html', context)
