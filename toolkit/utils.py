# -*- coding: utf-8 -*-

class NextUrl:
    """Url constructor"""

    @staticmethod
    def foward(request):
        """
        Replacing route `/` with `-`, so as to pass it in the `password_validation` and `set_passcode` view
        """

        next_url = request.path_info.replace('/', '-')
        # next_url = next_url.replace('//', '/')
        # next_url = next_url.replace('--', '-')
        # next_url = next_url.replace('?', '%3F')
        return next_url
    
    @staticmethod
    def reverse(next_url):
        """
        Replacing our converted route `-` with `/`, so as to render in the next route and in the passcode validation page
        """
        
        next_url = next_url.replace('-', '/')
        # next_url = next_url.replace('//', '/')
        # next_url = next_url.replace('--', '-')
        # next_url = next_url.replace('?', '%3F')
        return next_url
