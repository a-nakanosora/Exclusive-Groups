bl_info = {
    "name": "Exclusive Groups",
    "description": "Quick assign to groups exclusive",
    "author": "A Nakanosora",
    "version": (1, 2),
    "blender": (2, 76, 0),
    "location": "View 3D > Toolbar (T) > Relations",
    "warning": "",
    "category": "3D View"
    }

import bpy

class ExclusiveGroupsPanel(bpy.types.Panel):
    bl_label = "Exclusive Groups"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Relations"
    bl_idname = 'view3d.excgroup_mainpanel'

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.operator(ExcGroupOperator_New.bl_idname, text='New')
        row.operator(ExcGroupOperator_Join.bl_idname, text='Join')
        row.menu('ExcGroupMenu')

class ExcGroupMenu(bpy.types.Menu):
    bl_label = "..."

    @classmethod
    def poll(cls, context):
        return context.object

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.operator(ExcGroupOperator_Cleanup.bl_idname, text='Clean')
        col.operator(ExcGroupOperator_ToOnlyExclusive.bl_idname, text='Remove from non-Exclusive Groups')

class ExcGroupOperator_New(bpy.types.Operator):
    bl_idname = 'view3d.excgroup_new'
    bl_label = 'Exclusive Group New'
    bl_options = {'REGISTER', 'UNDO'}

    groupname = bpy.props.StringProperty(default = "")

    def invoke(self, context, event):
        self.groupname = ''
        return self.execute(context)

    def execute(self, context):
        selobjs = bpy.context.selected_objects

        if not self.groupname:
            self.groupname = make_excgroup_name()

        join_to_excgroup(selobjs, self.groupname)
        clean_useless_groups()
        return {'FINISHED'}

class ExcGroupOperator_Join(bpy.types.Operator):
    bl_idname = 'view3d.excgroup_join'
    bl_label = 'Exclusive Group Join'
    bl_options = {'REGISTER', 'UNDO'}

    groupname = bpy.props.StringProperty(default = "")

    def invoke(self, context, event):
        self.groupname = ''
        return self.execute(context)

    def execute(self, context):
        selobjs = bpy.context.selected_objects
        actobj = bpy.context.active_object

        if not self.groupname:
            groupname = excgroupname_of(actobj) if actobj is not None else ''
            if groupname is None:
                return {'FINISHED'}
            self.groupname = groupname

        join_to_excgroup(selobjs, self.groupname)
        clean_useless_groups()
        return {'FINISHED'}

class ExcGroupOperator_Cleanup(bpy.types.Operator):
    bl_idname = 'view3d.excgroup_cleanup'
    bl_label = 'Exclusive Group Clean'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selobjs = bpy.context.selected_objects
        count = cleanup(selobjs)
        clean_useless_groups()

        self.report({'INFO'}, '{} object(s) cleaned.'.format(count))
        return {'FINISHED'}

class ExcGroupOperator_ToOnlyExclusive(bpy.types.Operator):
    bl_idname = 'view3d.excgroup_to_only_exclusive'
    bl_label = 'Remove from non-Exclusive Groups'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        def groupnum_of(obj): return len(obj.users_group)
        def groupnums(objs): return [groupnum_of(obj) for obj in objs]

        selobjs = bpy.context.selected_objects
        nums0 = groupnums(selobjs)
        to_only_exclusive(selobjs)
        clean_useless_groups()
        nums1 = groupnums(selobjs)

        changecount = len( [True for a,b in zip(nums0, nums1) if a-b!=0] )
        self.report({'INFO'}, '{} object(s) change group state.'.format(changecount))
        return {'FINISHED'}

EXCLUSIVE_GROUP_PREFIX = 'exc-'

def to_only_exclusive(objs):
    for obj in objs:
        for group in list(obj.users_group):
            if not group.name.startswith( EXCLUSIVE_GROUP_PREFIX ):
                group.objects.unlink(obj)

def cleanup(objs):
    def quated(s): return '"{}"'.format(s)

    if not objs:
        objs = bpy.data.objects

    cleanedcount = 0
    for obj in objs:
        groupnames = excgroupnames_of(obj)
        if len(groupnames) >= 2:
            remained_group = groupnames[0]
            print('Exclusive Group Cleanup: Object {} exc-group cleaned: ({}) -> {}'
                      .format( quated(obj.name)
                             , ', '.join([quated(n) for n in groupnames])
                             , quated(remained_group)
                             ))
            leave_from_all_excgroups(obj)
            join_to_excgroup([obj], remained_group)
            cleanedcount += 1
    return cleanedcount

def clean_useless_groups():
    for group in bpy.data.groups:
        if group.name.startswith( EXCLUSIVE_GROUP_PREFIX )  and  not group.objects:
            bpy.data.groups.remove(group)

def leave_from_all_excgroups(obj):
    for group in list(obj.users_group):
        if group.name.startswith( EXCLUSIVE_GROUP_PREFIX ):
            group.objects.unlink(obj)

def join_to_excgroup(objs, groupname=None):
    if groupname is None  or  not groupname.startswith( EXCLUSIVE_GROUP_PREFIX ):
        groupname = make_excgroup_name()

    for obj in objs:
        leave_from_all_excgroups(obj)
        add_to_group(obj, groupname)

def add_to_group(obj, groupname):
    if groupname not in bpy.data.groups:
        bpy.data.groups.new(groupname)
    bpy.data.groups[groupname].objects.link(obj)

def make_excgroup_name():
    basename = EXCLUSIVE_GROUP_PREFIX+'Group'
    if basename not in bpy.data.groups:
        return basename
    for index in range(1,10000):
        name = '{0}.{1:0>3}'.format(basename, index)
        if name not in bpy.data.groups:
            return name

def excgroupname_of(obj): # type Optional[String]
    for group in list(obj.users_group):
        if group.name.startswith( EXCLUSIVE_GROUP_PREFIX ):
            return group.name

def excgroupnames_of(obj): # type List[String]
    names = []
    for group in list(obj.users_group):
        if group.name.startswith( EXCLUSIVE_GROUP_PREFIX ):
            names.append(group.name)
    return names

def register():
    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    try:
        bpy._unr()
    except:
        pass
    bpy._unr = unregister

    register()