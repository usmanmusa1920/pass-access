from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages as flash_msg
from django.contrib.auth.decorators import login_required
from .models import SecureItemInfo
from .forms import PassCodeForm, AccountPassCodeForm
from toolkit import (
    check_user_passcode_set, passcode_required, PasscodeSecurity, SliceDetector
)


User = get_user_model()
THIS_YEARE = datetime.today().year


def landing(request):
    """landing page view"""
    if request.user.is_authenticated:
        return redirect('secureapp:dashboard')
    context = {
        'the_year': THIS_YEARE,
    }
    return render(request, 'account/landing.html', context)


@passcode_required
def dashboard(request):
    """dashboard page view"""
    user_items = SecureItemInfo.objects.filter(
        i_owner=request.user.passcode).order_by('-date_created')[:10]
    context = {
        'user_items': user_items,
        'the_year': THIS_YEARE,
        'monitor_session_age': True,
    }
    return render(request, 'secureapp/dashboard.html', context)


@login_required
def set_passcode(request):
    """set user passcode view"""
    
    user_email = request.user.email
    
    # block user from setting passcode if already setted id
    if request.user.passcode.passcode_ingredient != '' and request.user.passcode.passcode_ingredient != None and request.user.passcode_hash != '' and request.user.passcode_hash != None:
        flash_msg.warning(request, f'You already setup passcode, you can change it here!')
        return redirect('secureapp:update_passcode')
    
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
            verify_new_passcode_again = pass_form.cleaned_data.get('passcode_ingredient')
            
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
            flash_msg.success(request, f'Your master passcode is set just now!')
            return redirect('secureapp:landing')
    else:
        pass_form = PassCodeForm(instance=request.user.passcode)
    context = {
        'pass_form': pass_form,
        'monitor_session_age': True,
    }
    return render(request, 'secureapp/set_passcode.html', context)


@check_user_passcode_set(flash_for='update')
@passcode_required
def update_passcode(request):
    """function for updating user passcode"""
    
    user_email = request.user.email
    
    # getting passcode
    slc = SliceDetector(request)
    slice_hash = slc._hash
    slice_ingre = slc._ingre
    slice_salt = slc._salt
    slice_iter = slc._iter
    
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
                return redirect('secureapp:landing')
    else:
        pass_form = PassCodeForm(instance=request.user.passcode)
    context = {
        'pass_form': pass_form,
        'monitor_session_age': True,
    }
    return render(request, 'secureapp/update_passcode.html', context)
