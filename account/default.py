# -*- coding: utf-8 -*-
from datetime import datetime
from secureapp.models import SecureItemInfo


def default(request):
    """
    It is mainly created so that it can be use (access) in any page,
    for example the year that will show in the footer
    it is not only for one page it is for all pages in the site
    
    so by using this class method we can access it in any page
    instead of creating `the_year` variable in each view
    
    like so the category list in the menu bar also it is not for one page
    and possibly for other variables ==> [the_year, user_items]
    """

    the_year = datetime.utcnow().year
    t_users = 0
     
    if request.user.is_authenticated:
        user_items = SecureItemInfo.objects.filter(
            i_owner=request.user.passcode).order_by('-date_created')[:10]
        
        # incrementing trusted users number
        for ii in SecureItemInfo.objects.filter(i_owner=request.user.passcode).all():
            t_users += ii.trusted_user.count()
    else:
        user_items = None
    
    data = {
        't_users': t_users,
        'the_year': the_year,
        'user_items': user_items,
        'monitor_session_age': True,
    }
    return data
