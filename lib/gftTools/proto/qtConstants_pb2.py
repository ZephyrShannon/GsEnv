# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: qtConstants.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='qtConstants.proto',
  package='com.gftchina.common.persistence.qtConstants',
  serialized_pb=_b('\n\x11qtConstants.proto\x12+com.gftchina.common.persistence.qtConstants*\xde\x01\n\rAlignmentFlag\x12\r\n\tAlignLeft\x10\x01\x12\x0e\n\nAlignRight\x10\x02\x12\x10\n\x0c\x41lignHCenter\x10\x04\x12\x10\n\x0c\x41lignJustify\x10\x08\x12\x11\n\rAlignAbsolute\x10\x10\x12\x18\n\x14\x41lignHorizontal_Mask\x10\x1f\x12\x0c\n\x08\x41lignTop\x10 \x12\x0f\n\x0b\x41lignBottom\x10@\x12\x11\n\x0c\x41lignVCenter\x10\x80\x01\x12\x12\n\rAlignBaseline\x10\x80\x02\x12\x17\n\x12\x41lignVertical_Mask\x10\xe0\x03*x\n\x08PenStyle\x12\t\n\x05NoPen\x10\x00\x12\r\n\tSolidLine\x10\x01\x12\x0c\n\x08\x44\x61shLine\x10\x02\x12\x0b\n\x07\x44otLine\x10\x03\x12\x0f\n\x0b\x44\x61shDotLine\x10\x04\x12\x12\n\x0e\x44\x61shDotDotLine\x10\x05\x12\x12\n\x0e\x43ustomDashLine\x10\x06*\x8a\x08\n\x0e\x43ontrolElement\x12\x11\n\rCE_PushButton\x10\x00\x12\x16\n\x12\x43\x45_PushButtonBevel\x10\x01\x12\x16\n\x12\x43\x45_PushButtonLabel\x10\x02\x12\x0f\n\x0b\x43\x45_CheckBox\x10\x03\x12\x14\n\x10\x43\x45_CheckBoxLabel\x10\x04\x12\x12\n\x0e\x43\x45_RadioButton\x10\x05\x12\x17\n\x13\x43\x45_RadioButtonLabel\x10\x06\x12\x10\n\x0c\x43\x45_TabBarTab\x10\x07\x12\x15\n\x11\x43\x45_TabBarTabShape\x10\x08\x12\x15\n\x11\x43\x45_TabBarTabLabel\x10\t\x12\x12\n\x0e\x43\x45_ProgressBar\x10\n\x12\x18\n\x14\x43\x45_ProgressBarGroove\x10\x0b\x12\x1a\n\x16\x43\x45_ProgressBarContents\x10\x0c\x12\x17\n\x13\x43\x45_ProgressBarLabel\x10\r\x12\x0f\n\x0b\x43\x45_MenuItem\x10\x0e\x12\x13\n\x0f\x43\x45_MenuScroller\x10\x0f\x12\x12\n\x0e\x43\x45_MenuVMargin\x10\x10\x12\x12\n\x0e\x43\x45_MenuHMargin\x10\x11\x12\x12\n\x0e\x43\x45_MenuTearoff\x10\x12\x12\x14\n\x10\x43\x45_MenuEmptyArea\x10\x13\x12\x12\n\x0e\x43\x45_MenuBarItem\x10\x14\x12\x17\n\x13\x43\x45_MenuBarEmptyArea\x10\x15\x12\x16\n\x12\x43\x45_ToolButtonLabel\x10\x16\x12\r\n\tCE_Header\x10\x17\x12\x14\n\x10\x43\x45_HeaderSection\x10\x18\x12\x12\n\x0e\x43\x45_HeaderLabel\x10\x19\x12\x11\n\rCE_ToolBoxTab\x10\x1a\x12\x0f\n\x0b\x43\x45_SizeGrip\x10\x1b\x12\x0f\n\x0b\x43\x45_Splitter\x10\x1c\x12\x11\n\rCE_RubberBand\x10\x1d\x12\x16\n\x12\x43\x45_DockWidgetTitle\x10\x1e\x12\x17\n\x13\x43\x45_ScrollBarAddLine\x10\x1f\x12\x17\n\x13\x43\x45_ScrollBarSubLine\x10 \x12\x17\n\x13\x43\x45_ScrollBarAddPage\x10!\x12\x17\n\x13\x43\x45_ScrollBarSubPage\x10\"\x12\x16\n\x12\x43\x45_ScrollBarSlider\x10#\x12\x15\n\x11\x43\x45_ScrollBarFirst\x10$\x12\x14\n\x10\x43\x45_ScrollBarLast\x10%\x12\x11\n\rCE_FocusFrame\x10&\x12\x14\n\x10\x43\x45_ComboBoxLabel\x10\'\x12\x0e\n\nCE_ToolBar\x10(\x12\x16\n\x12\x43\x45_ToolBoxTabShape\x10)\x12\x16\n\x12\x43\x45_ToolBoxTabLabel\x10*\x12\x16\n\x12\x43\x45_HeaderEmptyArea\x10+\x12\x15\n\x11\x43\x45_ColumnViewGrip\x10,\x12\x13\n\x0f\x43\x45_ItemViewItem\x10-\x12\x12\n\x0e\x43\x45_ShapedFrame\x10.*\xce\x01\n\x08ItemFlag\x12\x0f\n\x0bNoItemFlags\x10\x00\x12\x14\n\x10ItemIsSelectable\x10\x01\x12\x12\n\x0eItemIsEditable\x10\x02\x12\x15\n\x11ItemIsDragEnabled\x10\x04\x12\x15\n\x11ItemIsDropEnabled\x10\x08\x12\x17\n\x13ItemIsUserCheckable\x10\x10\x12\x11\n\rItemIsEnabled\x10 \x12\x12\n\x0eItemIsTristate\x10@\x12\x19\n\x14ItemNeverHasChildren\x10\x80\x01*3\n\rSortIndicator\x12\x08\n\x04None\x10\x00\x12\n\n\x06SortUp\x10\x01\x12\x0c\n\x08SortDown\x10\x02*+\n\x0bOrientation\x12\x0e\n\nHorizontal\x10\x01\x12\x0c\n\x08Vertical\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_ALIGNMENTFLAG = _descriptor.EnumDescriptor(
  name='AlignmentFlag',
  full_name='com.gftchina.common.persistence.qtConstants.AlignmentFlag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AlignLeft', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignRight', index=1, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignHCenter', index=2, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignJustify', index=3, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignAbsolute', index=4, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignHorizontal_Mask', index=5, number=31,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignTop', index=6, number=32,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignBottom', index=7, number=64,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignVCenter', index=8, number=128,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignBaseline', index=9, number=256,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='AlignVertical_Mask', index=10, number=480,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=67,
  serialized_end=289,
)
_sym_db.RegisterEnumDescriptor(_ALIGNMENTFLAG)

AlignmentFlag = enum_type_wrapper.EnumTypeWrapper(_ALIGNMENTFLAG)
_PENSTYLE = _descriptor.EnumDescriptor(
  name='PenStyle',
  full_name='com.gftchina.common.persistence.qtConstants.PenStyle',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NoPen', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SolidLine', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DashLine', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DotLine', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DashDotLine', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DashDotDotLine', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CustomDashLine', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=291,
  serialized_end=411,
)
_sym_db.RegisterEnumDescriptor(_PENSTYLE)

PenStyle = enum_type_wrapper.EnumTypeWrapper(_PENSTYLE)
_CONTROLELEMENT = _descriptor.EnumDescriptor(
  name='ControlElement',
  full_name='com.gftchina.common.persistence.qtConstants.ControlElement',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='CE_PushButton', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_PushButtonBevel', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_PushButtonLabel', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_CheckBox', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_CheckBoxLabel', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_RadioButton', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_RadioButtonLabel', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_TabBarTab', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_TabBarTabShape', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_TabBarTabLabel', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ProgressBar', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ProgressBarGroove', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ProgressBarContents', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ProgressBarLabel', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuItem', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuScroller', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuVMargin', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuHMargin', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuTearoff', index=18, number=18,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuEmptyArea', index=19, number=19,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuBarItem', index=20, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_MenuBarEmptyArea', index=21, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ToolButtonLabel', index=22, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_Header', index=23, number=23,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_HeaderSection', index=24, number=24,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_HeaderLabel', index=25, number=25,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ToolBoxTab', index=26, number=26,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_SizeGrip', index=27, number=27,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_Splitter', index=28, number=28,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_RubberBand', index=29, number=29,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_DockWidgetTitle', index=30, number=30,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarAddLine', index=31, number=31,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarSubLine', index=32, number=32,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarAddPage', index=33, number=33,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarSubPage', index=34, number=34,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarSlider', index=35, number=35,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarFirst', index=36, number=36,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ScrollBarLast', index=37, number=37,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_FocusFrame', index=38, number=38,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ComboBoxLabel', index=39, number=39,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ToolBar', index=40, number=40,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ToolBoxTabShape', index=41, number=41,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ToolBoxTabLabel', index=42, number=42,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_HeaderEmptyArea', index=43, number=43,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ColumnViewGrip', index=44, number=44,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ItemViewItem', index=45, number=45,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CE_ShapedFrame', index=46, number=46,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=414,
  serialized_end=1448,
)
_sym_db.RegisterEnumDescriptor(_CONTROLELEMENT)

ControlElement = enum_type_wrapper.EnumTypeWrapper(_CONTROLELEMENT)
_ITEMFLAG = _descriptor.EnumDescriptor(
  name='ItemFlag',
  full_name='com.gftchina.common.persistence.qtConstants.ItemFlag',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NoItemFlags', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsSelectable', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsEditable', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsDragEnabled', index=3, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsDropEnabled', index=4, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsUserCheckable', index=5, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsEnabled', index=6, number=32,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemIsTristate', index=7, number=64,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ItemNeverHasChildren', index=8, number=128,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1451,
  serialized_end=1657,
)
_sym_db.RegisterEnumDescriptor(_ITEMFLAG)

ItemFlag = enum_type_wrapper.EnumTypeWrapper(_ITEMFLAG)
_SORTINDICATOR = _descriptor.EnumDescriptor(
  name='SortIndicator',
  full_name='com.gftchina.common.persistence.qtConstants.SortIndicator',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='None', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SortUp', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SortDown', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1659,
  serialized_end=1710,
)
_sym_db.RegisterEnumDescriptor(_SORTINDICATOR)

SortIndicator = enum_type_wrapper.EnumTypeWrapper(_SORTINDICATOR)
_ORIENTATION = _descriptor.EnumDescriptor(
  name='Orientation',
  full_name='com.gftchina.common.persistence.qtConstants.Orientation',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Horizontal', index=0, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Vertical', index=1, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1712,
  serialized_end=1755,
)
_sym_db.RegisterEnumDescriptor(_ORIENTATION)

Orientation = enum_type_wrapper.EnumTypeWrapper(_ORIENTATION)
AlignLeft = 1
AlignRight = 2
AlignHCenter = 4
AlignJustify = 8
AlignAbsolute = 16
AlignHorizontal_Mask = 31
AlignTop = 32
AlignBottom = 64
AlignVCenter = 128
AlignBaseline = 256
AlignVertical_Mask = 480
NoPen = 0
SolidLine = 1
DashLine = 2
DotLine = 3
DashDotLine = 4
DashDotDotLine = 5
CustomDashLine = 6
CE_PushButton = 0
CE_PushButtonBevel = 1
CE_PushButtonLabel = 2
CE_CheckBox = 3
CE_CheckBoxLabel = 4
CE_RadioButton = 5
CE_RadioButtonLabel = 6
CE_TabBarTab = 7
CE_TabBarTabShape = 8
CE_TabBarTabLabel = 9
CE_ProgressBar = 10
CE_ProgressBarGroove = 11
CE_ProgressBarContents = 12
CE_ProgressBarLabel = 13
CE_MenuItem = 14
CE_MenuScroller = 15
CE_MenuVMargin = 16
CE_MenuHMargin = 17
CE_MenuTearoff = 18
CE_MenuEmptyArea = 19
CE_MenuBarItem = 20
CE_MenuBarEmptyArea = 21
CE_ToolButtonLabel = 22
CE_Header = 23
CE_HeaderSection = 24
CE_HeaderLabel = 25
CE_ToolBoxTab = 26
CE_SizeGrip = 27
CE_Splitter = 28
CE_RubberBand = 29
CE_DockWidgetTitle = 30
CE_ScrollBarAddLine = 31
CE_ScrollBarSubLine = 32
CE_ScrollBarAddPage = 33
CE_ScrollBarSubPage = 34
CE_ScrollBarSlider = 35
CE_ScrollBarFirst = 36
CE_ScrollBarLast = 37
CE_FocusFrame = 38
CE_ComboBoxLabel = 39
CE_ToolBar = 40
CE_ToolBoxTabShape = 41
CE_ToolBoxTabLabel = 42
CE_HeaderEmptyArea = 43
CE_ColumnViewGrip = 44
CE_ItemViewItem = 45
CE_ShapedFrame = 46
NoItemFlags = 0
ItemIsSelectable = 1
ItemIsEditable = 2
ItemIsDragEnabled = 4
ItemIsDropEnabled = 8
ItemIsUserCheckable = 16
ItemIsEnabled = 32
ItemIsTristate = 64
ItemNeverHasChildren = 128
None = 0
SortUp = 1
SortDown = 2
Horizontal = 1
Vertical = 2


DESCRIPTOR.enum_types_by_name['AlignmentFlag'] = _ALIGNMENTFLAG
DESCRIPTOR.enum_types_by_name['PenStyle'] = _PENSTYLE
DESCRIPTOR.enum_types_by_name['ControlElement'] = _CONTROLELEMENT
DESCRIPTOR.enum_types_by_name['ItemFlag'] = _ITEMFLAG
DESCRIPTOR.enum_types_by_name['SortIndicator'] = _SORTINDICATOR
DESCRIPTOR.enum_types_by_name['Orientation'] = _ORIENTATION


# @@protoc_insertion_point(module_scope)
