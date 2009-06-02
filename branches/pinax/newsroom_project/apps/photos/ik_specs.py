""" Default image specifications """

from imagekit.specs import ImageSpec
from imagekit import processors
    
# First we define our "processors". ImageKit ships with four configurable
# processors: Adjustment, Resize, Reflection and Transpose. You can also
# create your own processors. Processors are configured by subclassing and
# overriding specific class variables.

class ResizeThumbnail30x30(processors.Resize):
    width = 30 
    height = 30
    crop = True

class ResizeThumbnail(processors.Resize):
    width = 100
    height = 75
    crop = True
    
class ResizeMedThumbnail(processors.Resize):
    width = 140
    height = 100
    crop = True

class ResizeDisplay(processors.Resize):
    width = 600
    
class EnhanceSmall(processors.Adjustment):
    contrast = 1.2
    sharpness = 1.1
    
# Next we define our specifications or "specs". Image specs are where we define
# the individual "classes" of images we want to have access to. Like processors
# image specs are configured by subclasses the ImageSpec superclass.
    
class AdminThumbnail(ImageSpec):
    access_as = 'admin_thumbnail'
    processors = [ResizeThumbnail, EnhanceSmall]

class MediumThumb(ImageSpec):
    processors = [ResizeMedThumbnail]

class Thumbnail30x30(ImageSpec):
    processors = [ResizeThumbnail30x30, EnhanceSmall]

class Display(ImageSpec):
    increment_count = True
    processors = [ResizeDisplay]
        
class Thumbnail(ImageSpec):
    processors = [ResizeThumbnail, EnhanceSmall]
    pre_cache = True
