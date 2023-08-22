# -*- coding: utf-8 -*-
from .crypt import PasscodeSecurity, InformationSecurity, MixinTrick, SliceDetector


class NextUrl:
    """url constructor"""
    @staticmethod
    def foward(request):
        """
        replacing `/` with `-`, so as to pass it in the `password_validation` and `set_pass_code` view
        """
        next_url_str = request.path_info.replace('/', '-')
        return next_url_str
    
    @staticmethod
    def reverse(next_url):
        """
        replacing `-` with `/`, so as to render in the next route and in the passcode validation page
        """
        next_url_convert = next_url.replace('-', '/')
        return next_url_convert


__all__ = [
    'PasscodeSecurity',
    'InformationSecurity',
    'MixinTrick',
    'SliceDetector',
    'NextUrl',
]
