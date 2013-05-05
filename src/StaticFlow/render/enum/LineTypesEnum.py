# LineTypesEnum.py
# (C)2012-2013
# Scott Ernst

#___________________________________________________________________________________________________ LineTypesEnum
class LineTypesEnum(object):

#===================================================================================================
#                                                                                       C L A S S

    SOLID = ['solid',['solid', '-', 'normal']]

    DOTTED = ['dotted', ['dotted', 'dot', '..']]

    DASHED = ['dashed', ['dashed', 'dash', '--']]

    DOUBLE = ['double', ['double', 'twice', 'doubled', '=']]

    GROOVE = ['groove', ['groove', 'grooved']]

    RIDGE = ['ridge', ['ridge', 'ridged']]

    INSET = ['inset', ['inset']]

    OUTSET = ['outset', ['outset']]

    NONE  = ['none', ['none', 'off', 'no', '0', 'false']]
