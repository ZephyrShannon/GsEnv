# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: uitypes.proto

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
  name='uitypes.proto',
  package='com.gftchina.common.persistence.uitypes',
  serialized_pb=_b('\n\ruitypes.proto\x12\'com.gftchina.common.persistence.uitypes*\xab\x0c\n\x06UIType\x12\x08\n\x04user\x10\x00\x12\x05\n\x01u\x10\x01\x12\x0b\n\x07small_i\x10\x02\x12\t\n\x05\x42IG_I\x10\x03\x12\x0b\n\x07small_j\x10\x04\x12\t\n\x05\x42IG_J\x10\x05\x12\x0b\n\x07small_t\x10\x06\x12\t\n\x05\x42IG_T\x10\x07\x12\x05\n\x01\x46\x10\x08\x12\x05\n\x01\x62\x10\t\x12\x06\n\x02\x46Q\x10\n\x12\x05\n\x01\x65\x10\x0b\x12\x07\n\x03SYS\x10\x0c\x12\x08\n\x04gbox\x10\r\x12\x08\n\x04\x63\x62ox\x10\x0e\x12\x07\n\x03tbl\x10\x0f\x12\t\n\x05tblUI\x10\x10\x12\n\n\x06search\x10\x11\x12\x0e\n\nnodeSearch\x10\x12\x12\x08\n\x04para\x10\x13\x12\t\n\x05mapUI\x10\x14\x12\x0c\n\x08searchUI\x10\x15\x12\n\n\x06listUI\x10\x16\x12\x0c\n\x08scenario\x10\x17\x12\t\n\x05\x66\x63Par\x10\x18\x12\x0b\n\x07otherUI\x10\x19\x12\x08\n\x04wsUI\x10\x1a\x12\x0f\n\x0breadonlyDoc\x10\x1b\x12\x14\n\x10readonlyDocRange\x10\x1c\x12\x0c\n\x08\x64ocRange\x10\x1d\x12\x0f\n\x0bwritableDoc\x10\x1e\x12\r\n\tuserGroup\x10\x1f\x12\x0f\n\x0bPublication\x10 \x12\x0f\n\x0b\x45xtResource\x10!\x12\x10\n\x0c\x43lientScript\x10\"\x12\x10\n\x0cJavaFunction\x10#\x12\x08\n\x04OSet\x10$\x12\r\n\tHyperlink\x10%\x12\t\n\x05group\x10&\x12\x12\n\rClientUIBegin\x10\x90N\x12\x15\n\x10\x43lientNodeSearch\x10\x91N\x12\x15\n\x10\x43lientPathSearch\x10\x92N\x12\x13\n\x0e\x43lientFQSearch\x10\x93N\x12\x13\n\x0e\x43lientSISearch\x10\x94N\x12\x1a\n\x15\x43lientFunctionCreator\x10\x95N\x12\x16\n\x11\x43lientSkillEditor\x10\x96N\x12\x16\n\x11\x43lientSpreadSheet\x10\x97N\x12\x10\n\x0b\x43lientChart\x10\x98N\x12\x0e\n\tClientDoc\x10\x99N\x12\x0f\n\nClientChat\x10\x9aN\x12\x0f\n\nClientCBox\x10\x9bN\x12\x19\n\x14\x43lientFuncSearchNode\x10\x9cN\x12\x13\n\x0e\x43lientComments\x10\x9dN\x12\x16\n\x11\x43lientWorkflowBox\x10\x9eN\x12\x11\n\x0c\x43lientTaskUI\x10\x9fN\x12\x16\n\x11\x43lientWritableDoc\x10\xa0N\x12\x0f\n\nClientTree\x10\xa1N\x12\x14\n\x0f\x43lientContainer\x10\xa2N\x12\x14\n\x0f\x43lientBlockTemp\x10\xa3N\x12\x1a\n\x15\x43lientActiveTagEditor\x10\xa4N\x12 \n\x1b\x43lientActiveUserGroupEditor\x10\xa5N\x12\x14\n\x0f\x43lientIOWrapper\x10\xa6N\x12\x1e\n\x19\x43lientSingleNodeIOWrapper\x10\xa7N\x12\x17\n\x12\x43lientParameterBar\x10\xa8N\x12\x18\n\x13\x43lientSkillEditorV2\x10\xa9N\x12\x13\n\x0e\x43lientCalendar\x10\xaaN\x12\x16\n\x11\x43lientGraphEditor\x10\xabN\x12\x17\n\x12\x43lientBrowserAgent\x10\xacN\x12\x18\n\x13\x43lientSkillFunction\x10\xadN\x12\x1a\n\x15\x43lientWorkspaceFormUI\x10\xaeN\x12\x1a\n\x15\x43lientGlobalContextUI\x10\xafN\x12\x13\n\x0e\x43lientFqEditor\x10\xb0N\x12\x10\n\x0b\x43lientFQRun\x10\xb1N\x12\x17\n\x12\x43lientFunctionForm\x10\xb2N\x12\x1d\n\x18\x43lientPythonFunctionForm\x10\xb3N\x12\x16\n\x11\x43lientFsDefEditor\x10\xb4N\x12\x18\n\x13\x43lientSessionRunner\x10\xb5N\x12\x11\n\x0b\x43lientUIEnd\x10\xd0\x86\x03\x12\x17\n\x11\x43lientSheetIOTemp\x10\xd1\x86\x03\x12\x17\n\x11\x43lientSkillNoExec\x10\xd2\x86\x03\x12\x16\n\x10\x43lientFormulaRef\x10\xd3\x86\x03\x12\x17\n\x11\x43lientFormulaRect\x10\xd4\x86\x03\x12\x1e\n\x18\x43lientNotificationWindow\x10\xd5\x86\x03\x12\x18\n\x12\x43lientGlobalIOTemp\x10\xd6\x86\x03\x12\x14\n\x0e\x46\x61keTypeWsInst\x10\xd7\x86\x03')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_UITYPE = _descriptor.EnumDescriptor(
  name='UIType',
  full_name='com.gftchina.common.persistence.uitypes.UIType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='user', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='u', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='small_i', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BIG_I', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='small_j', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BIG_J', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='small_t', index=6, number=6,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BIG_T', index=7, number=7,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='F', index=8, number=8,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='b', index=9, number=9,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FQ', index=10, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='e', index=11, number=11,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SYS', index=12, number=12,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='gbox', index=13, number=13,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='cbox', index=14, number=14,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='tbl', index=15, number=15,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='tblUI', index=16, number=16,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='search', index=17, number=17,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='nodeSearch', index=18, number=18,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='para', index=19, number=19,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='mapUI', index=20, number=20,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='searchUI', index=21, number=21,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='listUI', index=22, number=22,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='scenario', index=23, number=23,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='fcPar', index=24, number=24,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='otherUI', index=25, number=25,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='wsUI', index=26, number=26,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='readonlyDoc', index=27, number=27,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='readonlyDocRange', index=28, number=28,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='docRange', index=29, number=29,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='writableDoc', index=30, number=30,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='userGroup', index=31, number=31,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Publication', index=32, number=32,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ExtResource', index=33, number=33,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientScript', index=34, number=34,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='JavaFunction', index=35, number=35,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='OSet', index=36, number=36,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='Hyperlink', index=37, number=37,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='group', index=38, number=38,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientUIBegin', index=39, number=10000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientNodeSearch', index=40, number=10001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientPathSearch', index=41, number=10002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFQSearch', index=42, number=10003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSISearch', index=43, number=10004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFunctionCreator', index=44, number=10005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSkillEditor', index=45, number=10006,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSpreadSheet', index=46, number=10007,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientChart', index=47, number=10008,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientDoc', index=48, number=10009,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientChat', index=49, number=10010,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientCBox', index=50, number=10011,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFuncSearchNode', index=51, number=10012,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientComments', index=52, number=10013,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientWorkflowBox', index=53, number=10014,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientTaskUI', index=54, number=10015,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientWritableDoc', index=55, number=10016,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientTree', index=56, number=10017,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientContainer', index=57, number=10018,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientBlockTemp', index=58, number=10019,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientActiveTagEditor', index=59, number=10020,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientActiveUserGroupEditor', index=60, number=10021,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientIOWrapper', index=61, number=10022,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSingleNodeIOWrapper', index=62, number=10023,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientParameterBar', index=63, number=10024,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSkillEditorV2', index=64, number=10025,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientCalendar', index=65, number=10026,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientGraphEditor', index=66, number=10027,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientBrowserAgent', index=67, number=10028,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSkillFunction', index=68, number=10029,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientWorkspaceFormUI', index=69, number=10030,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientGlobalContextUI', index=70, number=10031,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFqEditor', index=71, number=10032,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFQRun', index=72, number=10033,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFunctionForm', index=73, number=10034,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientPythonFunctionForm', index=74, number=10035,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFsDefEditor', index=75, number=10036,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSessionRunner', index=76, number=10037,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientUIEnd', index=77, number=50000,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSheetIOTemp', index=78, number=50001,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientSkillNoExec', index=79, number=50002,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFormulaRef', index=80, number=50003,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientFormulaRect', index=81, number=50004,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientNotificationWindow', index=82, number=50005,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ClientGlobalIOTemp', index=83, number=50006,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FakeTypeWsInst', index=84, number=50007,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=59,
  serialized_end=1638,
)
_sym_db.RegisterEnumDescriptor(_UITYPE)

UIType = enum_type_wrapper.EnumTypeWrapper(_UITYPE)
user = 0
u = 1
small_i = 2
BIG_I = 3
small_j = 4
BIG_J = 5
small_t = 6
BIG_T = 7
F = 8
b = 9
FQ = 10
e = 11
SYS = 12
gbox = 13
cbox = 14
tbl = 15
tblUI = 16
search = 17
nodeSearch = 18
para = 19
mapUI = 20
searchUI = 21
listUI = 22
scenario = 23
fcPar = 24
otherUI = 25
wsUI = 26
readonlyDoc = 27
readonlyDocRange = 28
docRange = 29
writableDoc = 30
userGroup = 31
Publication = 32
ExtResource = 33
ClientScript = 34
JavaFunction = 35
OSet = 36
Hyperlink = 37
group = 38
ClientUIBegin = 10000
ClientNodeSearch = 10001
ClientPathSearch = 10002
ClientFQSearch = 10003
ClientSISearch = 10004
ClientFunctionCreator = 10005
ClientSkillEditor = 10006
ClientSpreadSheet = 10007
ClientChart = 10008
ClientDoc = 10009
ClientChat = 10010
ClientCBox = 10011
ClientFuncSearchNode = 10012
ClientComments = 10013
ClientWorkflowBox = 10014
ClientTaskUI = 10015
ClientWritableDoc = 10016
ClientTree = 10017
ClientContainer = 10018
ClientBlockTemp = 10019
ClientActiveTagEditor = 10020
ClientActiveUserGroupEditor = 10021
ClientIOWrapper = 10022
ClientSingleNodeIOWrapper = 10023
ClientParameterBar = 10024
ClientSkillEditorV2 = 10025
ClientCalendar = 10026
ClientGraphEditor = 10027
ClientBrowserAgent = 10028
ClientSkillFunction = 10029
ClientWorkspaceFormUI = 10030
ClientGlobalContextUI = 10031
ClientFqEditor = 10032
ClientFQRun = 10033
ClientFunctionForm = 10034
ClientPythonFunctionForm = 10035
ClientFsDefEditor = 10036
ClientSessionRunner = 10037
ClientUIEnd = 50000
ClientSheetIOTemp = 50001
ClientSkillNoExec = 50002
ClientFormulaRef = 50003
ClientFormulaRect = 50004
ClientNotificationWindow = 50005
ClientGlobalIOTemp = 50006
FakeTypeWsInst = 50007


DESCRIPTOR.enum_types_by_name['UIType'] = _UITYPE


# @@protoc_insertion_point(module_scope)
