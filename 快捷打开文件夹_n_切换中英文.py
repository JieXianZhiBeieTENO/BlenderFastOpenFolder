bl_info = {
    "name" : "UPBGE快捷方式",
    "author" : "尐贤之辈のTENO",
    "description" : "快捷打开文件夹，切换中英文",
    "blender" : (3, 6, 0),
    "version" : (1, 0, 0),
    "location" : "View 3D > faster",
    "category" : "快捷方式",
    "doc_url": "",
    "tracker_url": "https://space.bilibili.com/1729654169"
}
import bpy,os,sys
from bpy.props import (
        IntProperty,
        BoolProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
        FloatProperty,
        IntVectorProperty,
        EnumProperty,
        CollectionProperty
    )
Ty=bpy.types
often_files=[]
Path=bpy.utils.resource_path('USER') + r'\scripts\presets\File_save'

class logic_nodes_place(Ty.Operator):
    bl_label = "打开Logic Nodes+位置"
    bl_idname = "faster.logic_nodes_place"
    def execute(self,context):
        try:
            os.startfile(os.path.dirname(sys.prefix)+r"\scripts\addons\bge_netlogic")
        except:
            rl("无法打开")
        return {"FINISHED"}
class uplogic_place(Ty.Operator):
    bl_label = "打开uplogic位置"
    bl_idname = "faster.uplogic_place"
    def execute(self,context):
        try:
            os.startfile(os.path.dirname(sys.prefix)+r"\python\lib\site-packages\uplogic")
        except:
            rl("无法打开")
        return {"FINISHED"}
class open_addon_place(Ty.Operator):
    bl_label = "打开插件位置"
    bl_idname = "faster.open_addon_place"
    def execute(self,context):
        try:
            os.startfile(os.path.dirname(__file__))
        except:
            rl("无法打开")
        return {"FINISHED"}
class exe_place(Ty.Operator):
    bl_label = "打开启动软件位置"
    bl_idname = "faster.exe_place"
    def execute(self,context):
        try:
            os.startfile(os.path.dirname(sys.prefix))
        except:
            rl("无法打开")
        return {"FINISHED"}

class ins_in_pref(Ty.AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout=self.layout
        col = layout.column()
        col.operator(open_addon_place.bl_idname)
        col.operator(exe_place.bl_idname)
        col.operator(logic_nodes_place.bl_idname)
        col.operator(uplogic_place.bl_idname)

class MOTIONCATCH_MT_Error_menu(Ty.Menu):
    bl_label = "错误"
    bl_idname = "MOTIONCATCH_MT_Error_menu"

    def draw(self, context):
        tools=context.scene.faster
        layout = self.layout
        layout.label(text=tools.error_thing,icon="ERROR")

    def draw_item(self, context):
        layout = self.layout
        layout.menu(MOTIONCATCH_MT_Error_menu.bl_idname)
def rl(errorthing,naming=MOTIONCATCH_MT_Error_menu):
    bpy.context.scene.faster.error_thing=errorthing
    bpy.ops.wm.call_menu(name=naming.bl_idname)

def Open(self,context):
    if self.open:
        try:
            os.startfile(self.path)
        except:
            rl("无法打开")
        self.open=False
def Open1(self,context):
    tools=context.scene.faster
    if tools.file1_open:
        try:
            os.startfile(tools.file1_path)
        except:
            rl("无法打开")
        tools.file1_open=False
def Open2(self,context):
    tools=context.scene.faster
    if tools.file2_open:
        try:
            os.startfile(tools.file2_path)
        except:
            rl("无法打开")
        tools.file2_open=False
def Remove(self,context):
    tools=context.scene.faster
    if not self.remove:
        return
    for c,i in enumerate(tools.file_vars):
        if i.remove:
            tools.file_vars.remove(c)
            i.remove=False
            return
def File(self,context):
    tools=context.scene.faster
    if tools.file_vars[-1].path!="":
        tools.file_vars.add()
def often_File(self,context):
    tools=context.scene.faster
    if not os.path.exists(Path):
        os.makedirs(Path)
    with open(Path+"\\often_files.py","w") as f:
        f.write(f"often_files={[tools.file1_path,tools.file2_path]}")
class File_Vars(Ty.PropertyGroup):
    path : StringProperty(subtype = "FILE_PATH" , update=File)
    open : BoolProperty(update = Open,name="打开文件夹",description="若为空，则呼出启动路径所对文件夹")
    remove : BoolProperty(update = Remove)

def Language(self,context):
    bpy.context.preferences.view.language=self.language
class Vars(Ty.PropertyGroup):
    Is_show_presets : BoolProperty(name="显示预设",default=True)
    file_vars : CollectionProperty(type = File_Vars)
    error_thing : StringProperty()
    
    if not os.access(Path+"\\often_files.py",os.F_OK):
        if not os.path.exists(Path):
            os.makedirs(Path)
        with open(Path+"\\often_files.py","w") as f:
            f.write("often_files=['','']")
    with open(Path+"\\often_files.py","r") as f:
        exec(f"global often_files\n{f.read()}")
        path1=often_files[0]
        path2=often_files[1]
    file1_path : StringProperty(subtype = "FILE_PATH" , update=often_File , default=path1)
    file1_open : BoolProperty(update = Open1,name="打开文件夹",description="若为空，则呼出启动路径所对文件夹")
    file2_path : StringProperty(subtype = "FILE_PATH" , update=often_File , default=path2)
    file2_open : BoolProperty(update = Open2,name="打开文件夹",description="若为空，则呼出启动路径所对文件夹")

    language: EnumProperty(
        name="语言",
        items=(
            ("zh_CN","中文",""),
            ("en_US", "英文", ""),
        ),
        default="zh_CN",
        update=Language
    )

class Open_File_1(Ty.Operator):
    bl_label = "file1"
    bl_idname = "faster.file1"
    def execute(self,context):
        tools=context.scene.faster
        try:
            os.startfile(tools.file1_path)
        except:
            rl("无法打开")
        return {"FINISHED"}

class Open_File_2(Ty.Operator):
    bl_label = "file2"
    bl_idname = "faster.file2"
    def execute(self,context):
        tools=context.scene.faster
        try:
            os.startfile(tools.file2_path)
        except:
            rl("无法打开")
        return {"FINISHED"}

class Add_new_one(Ty.Operator):
    bl_label = "增加值"
    bl_idname = "faster.addnewone"
    def execute(self,context):
        tools = bpy.context.scene.faster
        tools.file_vars.add()
        return {"FINISHED"}

class FASTER_PT_files_ui_panel(Ty.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "文件夹"
    bl_idname = "FASTER_PT_files_ui_panel"
    bl_label = "打开文件夹"

    def draw(self,context):
        tools = context.scene.faster

        col0=self.layout.column(align=True)
        col0.prop(tools,"Is_show_presets",text="隐藏预设" if tools.Is_show_presets else "显示预设",icon="TRIA_DOWN" if tools.Is_show_presets else "TRIA_RIGHT")
        if tools.Is_show_presets:
            bocol0=col0.box().column(align=True)
            bocol0.operator(open_addon_place.bl_idname)
            bocol0.operator(exe_place.bl_idname)
            bocol0.operator(logic_nodes_place.bl_idname)
            bocol0.operator(uplogic_place.bl_idname)
        layout=self.layout.column(align=True)
        layout.label(text="含快捷键")
        box0=layout.box().column(align=True)
        box0.label(text="Ctrl+Alt+Shift+C")
        row1=box0.row(align=True)
        row1.prop(tools,"file1_path",text="")
        row1.prop(tools,"file1_open",text="",icon="FILE")
        box01=box0.column(align=True)
        box01.label(text="Ctrl+Alt+Shift+D")
        row2=box0.row(align=True)
        row2.prop(tools,"file2_path",text="")
        row2.prop(tools,"file2_open",text="",icon="FILE")
        layout=self.layout.column(align=True)
        layout.label(text="其他")
        box1=layout.box()
        col1=box1.column(align=True)
        for c,i in enumerate(tools.file_vars):
            exec(f"""
row{c}=col1.row(align=True)
row{c}.prop(i,"path",text="")
row{c}.prop(i,"open",text="",icon="FILE")
row{c}.prop(i,"remove",text="",icon="REMOVE")
            """)
        if len(tools.file_vars)==0:
            col1.row().operator(Add_new_one.bl_idname)
        else:
            box1.operator(Add_new_one.bl_idname)
        self.layout.prop(tools,"language")

addon_keymaps = []
cls=(
open_addon_place,
exe_place,
logic_nodes_place,
uplogic_place,
ins_in_pref,
MOTIONCATCH_MT_Error_menu,
File_Vars,
Vars,
Open_File_1,
Open_File_2,
FASTER_PT_files_ui_panel,
Add_new_one,
)
def register():
    for i in cls:
        bpy.utils.register_class(i)
    bpy.types.Scene.faster = PointerProperty(type=Vars)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(Open_File_1.bl_idname, ctrl=1, alt=1, shift=1, type='C', value='PRESS')
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(Open_File_2.bl_idname, ctrl=1, alt=1, shift=1, type='D', value='PRESS')
        addon_keymaps.append((km, kmi))
def unregister():
    for i in cls:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.faster
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__=="__main__":
    register()