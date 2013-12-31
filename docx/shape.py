# encoding: utf-8

"""
Objects related to shapes, visual objects that appear on the drawing layer of
a document.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from docx.enum.shape import WD_INLINE_SHAPE
from docx.oxml.shape import CT_Inline, CT_Picture
from docx.oxml.shared import nsmap


class InlineShape(object):
    """
    Proxy for an ``<wp:inline>`` element, representing the container for an
    inline graphical object.
    """
    def __init__(self, inline):
        super(InlineShape, self).__init__()
        self._inline = inline

    @property
    def height(self):
        """
        Return the display height of this inline shape as an |Emu| instance.
        Length instances such as this behave like an int, but also have
        built-in conversion properties, e.g.::

            \>>> inline_shape.height
            914400
            \>>> inline_shape.height.inches
            1.0
        """
        return self._inline.extent.cy

    @classmethod
    def new_picture(cls, r, image_part, rId, shape_id):
        """
        Return a new |InlineShape| instance containing an inline picture
        placement of *image_part* appended to run *r* and uniquely identified
        by *shape_id*.
        """
        cx, cy, filename = (
            image_part.default_cx, image_part.default_cy, image_part.filename
        )
        pic_id = 0
        pic = CT_Picture.new(pic_id, filename, rId, cx, cy)
        inline = CT_Inline.new(cx, cy, shape_id, pic)
        r.add_drawing(inline)
        return cls(inline)

    @property
    def type(self):
        """
        Return the member of ``docx.enum.shape.WD_INLINE_SHAPE`` denoting the
        inline shape type, e.g. ``LINKED_PICTURE``.
        """
        graphicData = self._inline.graphic.graphicData
        uri = graphicData.uri
        if uri == nsmap['pic']:
            blip = graphicData.pic.blipFill.blip
            if blip.link is not None:
                return WD_INLINE_SHAPE.LINKED_PICTURE
            return WD_INLINE_SHAPE.PICTURE
        if uri == nsmap['c']:
            return WD_INLINE_SHAPE.CHART
        if uri == nsmap['dgm']:
            return WD_INLINE_SHAPE.SMART_ART
        return WD_INLINE_SHAPE.NOT_IMPLEMENTED

    @property
    def width(self):
        """
        Return the display width of this inline shape as an |Emu| instance.
        """
        return self._inline.extent.cx
