"""
Constants for the multimedia app
"""

MEDIA_TYPE_IMAGE = 'photo'
MEDIA_TYPE_VIDEO = 'video'

MEDIA_TYPES = (
    (MEDIA_TYPE_IMAGE,'Photo',),
    (MEDIA_TYPE_VIDEO,'Video',),
)

LICENSE_DEFAULT = 'http://creativecommons.org/licenses/by/2.0/'
LICENSE_CHOICES = (
      ('http://creativecommons.org/licenses/by/2.0/',         'CC Attribution'),
      ('http://creativecommons.org/licenses/by-nd/2.0/',      'CC Attribution-NoDerivs'),
      ('http://creativecommons.org/licenses/by-nc-nd/2.0/',   'CC Attribution-NonCommercial-NoDerivs'),
      ('http://creativecommons.org/licenses/by-nc/2.0/',      'CC Attribution-NonCommercial'),
      ('http://creativecommons.org/licenses/by-nc-sa/2.0/',   'CC Attribution-NonCommercial-ShareAlike'),
      ('http://creativecommons.org/licenses/by-sa/2.0/',      'CC Attribution-ShareAlike'),
)
