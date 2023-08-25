# PassAccess

Password and sensitive information manager, that encrypt and save them for a user, which can be decrypt by the user when ever need to be. Security application that secure sensitive informations.

![snippet_theme](screen/landing.png)

## Hints

The __'monitor_session_age': True__ within some view's context dictionary (mostly in view that are decorated with `@passcode_required` and have page to render), enable the (security_secs, and security_user_sess_age) span tags to display in the html page. Note these two tags are only place at the top of `base_1.html, and base_2.html` where as other pages are in herited from one of these two. The javascript function for them is below each file, within the script (<script></script>) tag. All what am trying to say is, by the use of such, if a user take <!-- half of the `session age` he/she set or --> 30 seconds without doing nothing `(onload, onmousemove, onmousedown, ontouchstart, onclick, or onkeypress)` the screen page will be dim (dark navy in color).

User can disable it by unchecking the checkbox in the update page.

