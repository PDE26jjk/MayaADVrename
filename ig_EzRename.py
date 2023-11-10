# -*- coding: utf-8 -*-
# PDE：这些是原来命名脚本的版权声明
#--------------------------------------------------------------------------------#
# QIONGTWO汉化 <脚本基于Python3，支持Maya2020以上版本>
# 先看看作者的版权信息，然后有使用说明。
#
#             ig_EzRename.py 
#             version 1.3, last modified 04/10/2022
#             版权所有Copyright (C) 2022 Igor Silva
#             Email: igorsilva.design@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# 本程序是免费软件：您可以重新分发它和/或修改
# 基于 GNU 通用公共许可证的条款发布，
# FSF自由软件基金会许可证的第 3 版或任何更高版本（根据您的选择）。
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# 分发该程序是希望它能提供帮助，
# 但对于适销性、特定用途的适用性不做任何保证;包括任何默示的保证
# 请参阅的GNU 通用公共许可证了解更多详情。
# 

# See http://www.gnu.org/licenses/gpl.html for a copy of the GNU General 
# Public License.
# GNU通用公共许可证网址：http://www.gnu.org/licenses/gpl.html
# 
 

#--------------------------------------------------------------------------------#

# 使用说明：
# 拷贝全部代码粘贴至maya脚本编辑器的python框中。
# 保存脚本为ig_EzRename.py到 MyDocuments\Maya\scripts\ 目录下。
# 在maya脚本编辑器的python框中输入以下内容：
'''

from importlib import reload # 新版本用，2019把这行删掉
import ig_EzRename
reload(ig_EzRename)
ig_EzRename.UI()

'''
# 然后把这段代码中键拖到工具架，点击运行即可。




import maya.cmds as cmds
import maya.mel as mel
import re
def UI():

    global SelectName
    global RenameText

    global StartValue
    global PaddingValue
    global NumberCheck

    global RemoveFirst
    global RemoveEnd

    global PrefixText
    global SuffixText

    global SearchText
    global ReplaceText
    global SRCheck

    #UI Width
    sizeX = 260
    version = "v1.0"
    if cmds.window("igEzRenameWin", exists=True):
        cmds.deleteUI("igEzRenameWin", window=True)

    #Creating UI
    igEzRenamWin = cmds.window("igEzRenameWin", title="ig重命名工具 "+version, width=sizeX+6,  mnb = True, mxb = False, sizeable = True)

    #Creating interface elements
    mainLayout = cmds.columnLayout("mainColumnLayout", width = sizeX, adjustableColumn=False, co = ["both",2])

    #Remove First/Last
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 25), (2, 60)], cs = [(5,5)])
    cmds.text(label="  删除所选的:", font = "boldLabelFont", w = sizeX/3-12, align="left")
    cmds.button(label = "开头字母->", w=sizeX/3, h=25, c="ig_EzRename.Remove(True)", align = "Center")
    cmds.button(label = "<-结尾字母", w=sizeX/3, h=25, c="ig_EzRename.Remove(False)", align = "Center")
    cmds.separator(h=5, style = "none", parent = mainLayout)
    cmds.separator(w = sizeX, h=15, style = "in", parent = mainLayout)

    #Suffix
    #Control Suffix
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    cmds.text(label="  添加前缀:", font = "boldLabelFont", w = sizeX/4-5, align="left")
    PrefixText = cmds.textField(w = sizeX/2.5+33, tx="SM_", ann="输入前缀")
    cmds.button(label = "添加", w=sizeX/4-10, h=25, c="ig_EzRename.PrefixSuffix(False)", align = "Center")
    cmds.separator(h=5, style = "none", parent = mainLayout)

    #Group Suffix
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    cmds.text(label="  添加后缀:", font = "boldLabelFont", w = sizeX/4-5, align="left")
    SuffixText = cmds.textField(w = sizeX/2.5+33, tx="_001", ann="输入后缀")
    cmds.button(label = "添加", w=sizeX/4-10, h=25, c="ig_EzRename.PrefixSuffix(True)", align = "Center")
    cmds.separator(w = sizeX, h=15, style = "in", parent = mainLayout)

    #Prefix
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    cmds.text(label="  后缀预设:", font = "boldLabelFont", w = sizeX/3-15, align="left", ann="后缀预设")
    cmds.button(label = "_high", w=sizeX/3, h=25, c="ig_EzRename.Suffix('_high')", align = "Center", ann = "高模后缀") 
    cmds.button(label = "_low", w=sizeX/3, h=25, c="ig_EzRename.Suffix('_low')", align = "Center", ann = "低模后缀")
    cmds.separator(w = sizeX, h=15, style = "in", parent = mainLayout)

    #Search and Replace
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    cmds.text(label="  搜索:", font = "boldLabelFont", w = sizeX/4-10, align="left", ann="搜索需要替换的文字")
    SearchText = cmds.textField(w = sizeX/2+100, ann="Write the text to search")
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    cmds.text(label="  替换:", font = "boldLabelFont", w = sizeX/4-10, align="left", ann="替换所搜文字")
    ReplaceText = cmds.textField(w = sizeX/2+100, ann="Write the text to replace")
    cmds.rowColumnLayout( numberOfRows=1, w=sizeX, parent=mainLayout, rowHeight=[(1, 20), (2, 60)], cs = [(5,5)])
    SRCheck = cmds.radioButtonGrp(labelArray3=[ '已选的目标', '已选的组内', '全部'], numberOfRadioButtons=3, w=sizeX, h=20, sl=1, cw = ([1,95],[2,95],[3,95]))
    cmds.separator(h=10, style = "none", parent = mainLayout)
    cmds.button(label = "确认替换", w=sizeX, h=25, c=SearchReplace, align = "Center", parent = mainLayout)
    cmds.separator(h=5, style = "none", parent = mainLayout)
    cmds.separator(w = sizeX, h=15, style = "in", parent = mainLayout)

    sizeX -= 40
    #ADV 
    # 创建折叠区域
    Adv_layout = cmds.frameLayout(label='ADV骨骼适配工具',mw=10, collapsable=True, collapse=False, parent = mainLayout)
    col_layout = cmds.columnLayout(adj=True, parent = Adv_layout)
    
    # 快速
    Adv_onekey_layout = cmds.frameLayout(label='快速',mw=10, collapsable=True, collapse=False, parent = col_layout)
    cmds.text(l="快速创建控制器",align = "left")
    cmds.button(label = "标记已蒙皮物体", w=sizeX, h=25, c=ADVSelectSkinObjects, align = "Center")
    cmds.button(label = "标记根骨骼", w=sizeX, h=25, c=ADVSelectRootJoint, align = "Center")
    cmds.button(label = "ADV创建控制器", w=sizeX, h=25, c=ADVBuild, align = "Center")
    cmds.separator(w = sizeX, h=15, style = "in")

    # 单步 
    Adv_step_layout = cmds.frameLayout(label='单步',mw=10, collapsable=True, collapse=True, parent = col_layout)
    cmds.text(l="选择根关节，然后",align = "left")
    cmds.button(label = "更改关节名称", w=sizeX, h=25, c=ChangeNameToMatchADV, align = "Center")
    cmds.text(l="选择已经蒙皮的mesh，然后",align = "left")
    cmds.button(label = "暂存权重", w=sizeX, h=25, c="ig_EzRename.saveLoadWeights(False)", align = "Center", )
    cmds.text(l="接着解除绑定",align = "left")
    cmds.text(l="选择根关节，冻结变换，然后",align = "left")
    cmds.button(label = "加ADV标签和属性", w=sizeX, h=25, c=LabelJointsToMatchADV, align = "Center")
    # cmds.button(label = "RestoreAndDeleteRedundantJoints", w=sizeX, h=25, c=RestoreAndDeleteRedundantJoints, align = "Center")
    # cmds.separator(h=5, style = "none")
    cmds.text(l="在ADV里面构建好控制器，然后",align = "left")
    cmds.button(label = "修复关节名称", w=sizeX, h=25, c=RenameAfterBuild, align = "Center")
    cmds.text(l="选择之前蒙皮的mesh，绑定回骨骼，然后",align = "left")
    cmds.button(label = "加载权重", w=sizeX, h=25, c="ig_EzRename.saveLoadWeights(True)", align = "Center")
    cmds.separator(w = sizeX, h=15, style = "in")


    Adv_fix_layout = cmds.frameLayout(label='修复',mw=10, collapsable=True, collapse=True, parent = col_layout)
    cmds.text(l="如果没有Arm_*，而有Arm1_*",align = "left")
    cmds.button(label = "修复关节名称", w=sizeX, h=25, c=RenameAfterBuild, align = "Center")
    cmds.text(l="修复Leg或Arm左右翻转",align = "left")
    cmds.button(label = "翻转左右Leg名", w=sizeX, h=25, c=FlipLegName, align = "Center")
    cmds.button(label = "翻转左右Arm名", w=sizeX, h=25, c=FlipArmName, align = "Center")
    cmds.separator(w = sizeX, h=15, style = "in")

    #Show UI:
    cmds.showWindow(igEzRenamWin)

def SelectName(*args):
    cmds.select(cl=True)
    name = cmds.textField(SelectName, text = 1, q=True)
    try:
        selection = cmds.ls(name, l = True)
    except:
        cmds.warning("Object Don't Exist")

    for objs in selection:
        cmds.select(objs, add=True)
  
def Remove(Type):
    
    selection = cmds.ls(selection = True, sn = True)

    for objs in selection:
        #Teste if has duplicate mesh with the same name on the scene
        trueName = testDuplicateName(objs)

        #Save the original name
        oldName = trueName

        if Type:
            name = trueName[1:]
        else:
            name = trueName[:-1]

        try:
            cmds.rename(objs, name)
        except:
            pass

        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, name)
            selection[x] = newParentName

def PrefixSuffix(Suffix):
    prefix = cmds.textField(PrefixText, text = 1, q=True)
    suffix = cmds.textField(SuffixText, text = 1, q=True)

    selection = cmds.ls(selection = True, sn = True)

    for objs in selection:

        #Teste if has duplicate mesh with the same name on the scene
        trueName = testDuplicateName(objs)
        #Save the original name
        oldName = trueName
        
        if Suffix:
            name = str(trueName)+suffix
        else:
            name = prefix+str(trueName)

        try:
            cmds.rename(objs, name)
        except:
            pass
        
        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, name)
            selection[x] = newParentName

JointNameMapSplit = {
    "Chest":("Spine2",),
    "Hip":("Thigh",),
    "Knee":("Calf",),
    "Ankle":("Foot",),
    "Scapula":("Clavicle",),
    "Toes":("Toe0",),
    "Shoulder":("UpperArm",),
    "Elbow":("Forearm",),
    "Wrist":("Hand",),
    'ThumbFinger1': ('Finger0',),'ThumbFinger2': ('Finger01',),'ThumbFinger3': ('Finger02',),
    'IndexFinger1': ('Finger1',),'IndexFinger2': ('Finger11',),'IndexFinger3': ('Finger12',),
    'MiddleFinger1': ('Finger2',),'MiddleFinger2': ('Finger21',),'MiddleFinger3': ('Finger22',),
    'RingFinger1': ('Finger3',),'RingFinger2': ('Finger31',),'RingFinger3': ('Finger32',),
    'PinkyFinger1': ('Finger4',),'PinkyFinger2': ('Finger41',),'PinkyFinger3': ('Finger42',),
}

JointNameMapTotal = {
    'Bip001': '',
    "EyeBone_A01" : "Eye",
    "EyeBone_A02" : "EyeEnd",
    "Spine1_M":"Spine1", # 这个在ADV里是硬编码的(大概在45122行), 有hip标记则一定要有Spine1存在
}

SkinObjects = None
RootJoint = None
def ADVSelectSkinObjects(_):
    global SkinObjects
    # selection = cmds.listRelatives(allDescendents=True)
    selection = cmds.ls(selection=True)
    # if p not in selection:
    #     selection.append(p)
    SkinObjects = selection[:]
    print("Skin Objects: ")
    print(SkinObjects)

def ADVSelectRootJoint(_):
    global RootJoint
    RootJoint = cmds.ls(selection=True)[0]
    print("Root Joint:" + RootJoint)

def ADVBuild(_):
    global SkinObjects
    global RootJoint
    try:
        cmds.optionMenu("asAttributeType", edit=True, value="noMirror")
    except Exception as e:
        om.MGlobal.displayError("Please open AdvancedSkeleton5 windows.")
        return
    # 关节改名
    rootName = 'Root'
    if RootJoint!= rootName:
        try:
            if cmds.objExists(rootName):
                cmds.rename(rootName, rootName+'_')
            cmds.rename(RootJoint, rootName)
        except:
            om.MGlobal.displayError(rootName+" exist! Rename it.")
            return
    
    cmds.select(rootName)
    # X轴归零，不然会创建一个RootSide_*的骨骼
    # try:
    #     cmds.parent(world=True)
    # except:
    #     pass
    # translation = cmds.xform(query=True, translation=True)
    # cmds.xform(translation=[0,translation[1],translation[2]])
    # 算了，还是删了，还有其他bug
    ChangeNameToMatchADV(None)

    # 保存权重
    cmds.select(SkinObjects)
    saveLoadWeights(False)
    # 解除绑定、烘焙历史，不然可能一解除绑定模型就变了，绑定回来对不上。否则可以用cmds.skinCluster( unbindKeepHistory=True )来保存权重的
    mel.eval('doDetachSkin "2" { "3","1" }')

    # 关节打标记，ADV用的
    cmds.select(rootName)
    LabelJointsToMatchADV(None)

    # ADV构建控制器
    mel.eval('asBuildAdvancedSkeleton')

    # 恢复ADV构建控制器的时候改的关节名
    RenameAfterBuild(None)
    RenameAfterBuild(None)

    # 恢复绑定
    rootName = rootName+'_M'
    # cmds.select(rootName,SkinObjects)
    for obj in SkinObjects:
        cmds.skinCluster(rootName,obj)

    # 恢复权重
    cmds.select(SkinObjects)
    saveLoadWeights(True)


def ChangeNameToMatchADV(_):  
    selection = cmds.listRelatives(allDescendents=True, type='joint')    
    for obj in selection:
        # 把|分离的名称取最后一个。
        trueName = testDuplicateName(obj)

        toReplaceSide = {"R_":"_R","L_":"_L","M_":"_M","CF_":"_M"}

        #Save the original name
        oldName = trueName
        # +号会被自动转成_,不过这里手动转了
        newName = re.sub(r'FBXASC\d{3}', '_', trueName)
        newName = newName.strip("_")
        for k,v in toReplaceSide.items():
            if k in newName:
                newName = newName.replace(k,'')
                newName += v
        if not newName.endswith(('_L','_R','_M')):
            newName = newName+'_M'
               
        for k,v in JointNameMapTotal.items():
            newName = re.sub(k, v, newName)
        newName = newName.strip("_")
        namePart = newName.split('_')

        for k,v in JointNameMapSplit.items():
            for joint_name in v:
                for i in range(len(namePart)):
                    if namePart[i] == joint_name:
                        namePart[i] = k
                    break

        newName = '_'.join(namePart)

        try:
            cmds.rename(obj, newName)
        except:
            pass
        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, newName)
            selection[x] = newParentName

JointsSave = {}
# 已废弃，使用noMirror代替
def SaveAndDeleteJointsToMatchADV(_):
    selection = cmds.listRelatives(allDescendents=True, type='joint')
    root = cmds.ls(selection=True)[0]
    selection.append(root)
    cmds.makeIdentity(root, apply=True, translate=True, rotate=True, scale=True)
    # 保存骨骼偏移和旋转
    for obj in selection:
        parent = cmds.listRelatives(obj, parent=True, type='joint')
        if parent :
            parent = parent[0]
        
        translation = cmds.xform(obj, query=True, translation=True)
        rotation = cmds.xform(obj, query=True, rotation=True)
        joint_orient = cmds.getAttr(obj+".jointOrient")
        jointStruct = {
            "translation":translation,
            "rotation":rotation,
            "parent": parent,
            #"Loaded": False
        }
        JointsSave[obj] = jointStruct
        #TODO 存preferredAngle?
        print(obj,translation,joint_orient)
        trueName = testDuplicateName(obj)
        # if trueName.endswith('_L'):
        #     if cmds.objExists(trueName[:-2]+'_R'):
        #         cmds.delete(obj)
        #         continue
        #     else:
        #         newX = abs(translation[0])
        # elif trueName.endswith('_R'):
        #         newX = -abs(translation[0])
        # elif trueName.endswith('_M'):
        #         newX = 0
        # newTranslation = [newX,translation[1],translation[2]]
        # cmds.xform(obj,r=True, translation=newTranslation,rotation=rotation)
        #cmds.parent(obj,parent,a=True, )
    for obj in selection:
        if not cmds.objExists(obj): continue
        trueName = testDuplicateName(obj)
    
        if obj.endswith('_L'):
            if cmds.objExists(trueName[:-2]+'_R'):
                cmds.delete(obj)
                continue
        jointStruct = JointsSave.get(obj)
        parent = jointStruct["parent"]
        # cmds.parent(obj, world=True)
        # cmds.xform(obj, translation=translation,rotation=rotation)
        # cmds.parent(obj,parent,r=True)
        
        if parent == 'Root':
            jointStruct['parent'] = 'Root_M'

        if trueName.endswith(('_L','_R','_M')):
            newName = trueName[:-2]
            try:
                cmds.rename(obj, newName)
            except:
                pass
    cmds.select('Root')
    
def RenameAfterBuild(_):
    selection = cmds.listRelatives('Main',allDescendents=True)
    for objs in selection:
        oldName = objs
        newName = re.sub(r"Spine1_[RLM]", r"Spine1_M", objs)
        newName = re.sub(r"(_[RLM])_[RLM]", r"\1", newName)
        newName = re.sub(r"Arm1_R", r"Arm_R", newName)
        newName = re.sub(r"Arm2_R", r"Arm_L", newName)
        newName = re.sub(r"Leg1_R", r"Leg_R", newName)
        newName = re.sub(r"Leg2_R", r"Leg_L", newName)
        if newName == oldName:
            continue
        try:
            cmds.rename(oldName, newName)
        except:
            pass

        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, newName)
            selection[x] = newParentName

def replaceADVName(ori,dst):
    selection = cmds.listRelatives('Main',allDescendents=True)
    for objs in selection:
        oldName = objs
        
        newName = re.sub(ori, dst, objs)
        if newName == oldName:
            continue
        try:
            cmds.rename(oldName, newName)
            print(oldName+"-->"+newName)
        except:
            pass

def FlipLegName(_):
    replaceADVName("Leg_R","Leg_Temp")
    replaceADVName("Leg_L","Leg_R")
    replaceADVName("Leg_Temp","Leg_L")

def FlipArmName(_):
    replaceADVName("Arm_R","Arm_Temp")
    replaceADVName("Arm_L","Arm_R")
    replaceADVName("Arm_Temp","Arm_L")
# 已废弃，配合RestoreAndDeleteRedundantJoints的
def RestoreAndDeleteRedundantJoints(_):
    joints = cmds.listRelatives('Main',allDescendents=True, type='joint')
    # root = cmds.ls(selection=True)[0]
    # selection.append(root)
    # 获取保存的骨骼偏移和旋转
    print(JointsSave.keys())
    for obj in joints:
        fkName = "FKOffset"+obj
        jointStruct = JointsSave.get(obj)
        if not jointStruct:
            print(obj + " not in JointSave")
            # children = cmds.listRelatives(obj,allDescendents=True)
            # if children:
            #     cmds.parent(children,world=True,a=True)
            cmds.delete(obj)
            if cmds.objExists(fkName):
                cmds.delete(fkName)
            continue
        translation = jointStruct["translation"]
        rotation = jointStruct["rotation"]
        # parent = jointStruct["parent"]

        if cmds.objExists(fkName):
            obj = fkName
        parent = cmds.listRelatives(obj, parent=True)
        cmds.parent(obj, world=True)
        cmds.xform(obj, translation=translation, rotation=rotation)
        cmds.parent(obj, parent,a=True)

labelOfJoint = {
    "Root":("Pelvis",),
    "Chest":("Chest",),
    "Hip":("Hip",),
    "Foot":("Foot","Ankle"),
    "Toes":("Toes",),
    "Hand":("Wrist",),
    "Shoulder":("Shoulder",),
}
attrOfJoint = {
    "aim":("Eye",),
}

def LabelJointsToMatchADV(_):
    root = cmds.ls(selection=True)[0]
    cmds.makeIdentity(root, apply=True, translate=True, rotate=True, scale=True)
    original_sel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(original_sel)
    selection = cmds.listRelatives(allDescendents=True, type='joint')
    selection.append(root)
    try:
        cmds.optionMenu("asAttributeType", edit=True, value="noMirror")
    except Exception as e:
        om.MGlobal.displayError("Open ADV windows please.")
        return
    for obj in selection:
        cmds.select(obj)
        cmds.optionMenu("asAttributeType", edit=True, value="noMirror")
        mel.eval("asAddFitJointAttribute")
        trueName = obj
        for k,v in labelOfJoint.items():
            for joint_name in v:
                if joint_name in trueName.split('_'):
                    cmds.optionMenu("asLabelType", edit=True, value=k)
                    mel.eval("asAddFitJointLabel")
                    break
        for k,v in attrOfJoint.items():
            for joint_name in v:
                if joint_name in trueName.split('_'):
                    cmds.optionMenu("asAttributeType", edit=True, value=k)
                    mel.eval("asAddFitJointAttribute")
                    break
    om.MGlobal.setActiveSelectionList(original_sel)

def select_selected_mesh_and_children():
    selection = cmds.ls(selection=True)
    if not selection:
        print("No objects are currently selected!")
        return None

    # 获取所选物体及其子物体
    children = []
    for obj_name in selection:
        child_objects = cmds.listRelatives(obj_name, allDescendents=True, type='transform')
        if child_objects:
            children.extend(child_objects)
        children.append(obj_name)
    return children

def Suffix(Text):
    
    selection = cmds.ls(selection = True, sn = True)
    
    for objs in selection:
        #Test if has duplicate mesh with the same name on the scene
        trueName = testDuplicateName(objs)

        #Save the original name
        oldName = trueName

        newName = trueName+Text
        try:
            cmds.rename(objs, newName)
        except:
            pass

        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, newName)
            selection[x] = newParentName

def SearchReplace(*args):
    
    search = cmds.textField(SearchText, text = 1, q=True)
    replace = cmds.textField(ReplaceText, text = 1, q=True)

    SRMethod = cmds.radioButtonGrp(SRCheck, q=True, select=True)
    
    #Selected search and Replace method
    if SRMethod == 1:
        selection = cmds.ls(selection = True, sn = True)

    #Hierarchy search and Replace method
    if SRMethod == 2:
        cmds.select(hi = True)
        selection = cmds.ls(selection = True, sn = False)
        
    #All search and Replace method
    if SRMethod == 3:
        #Select All DagObjects in scene
        selection = []
        cmds.select(ado = True, hi = True)
        selection = cmds.ls(selection = True, sn=False)

    #for to rename the objects 
    for obj in selection:
        #Teste if has duplicate mesh with the same name on the scene and return the name without parents
        trueName = testDuplicateName(obj)
        #Save the original name
        oldName = trueName
        #Search and replace to create the new name
        newName = trueName.replace(search, replace)
        
        #Rename the object
        try:
            cmds.rename(obj, newName)
        except:
            pass
    
        #For to rename all the oldNames on list to newNames
        for x in range(len(selection)):
            newParentName = selection[x].replace(oldName, newName)
            selection[x] = newParentName

        print("Slecao: ", selection)
     
    
def testDuplicateName(Obj):

    try:
        trueName =  Obj.split("|")
        return trueName[len(trueName)-1]
    except:
        return Obj


# https://www.artstation.com/blogs/benmorgan/72rD/maya-python-api-gettingsetting-skin-weights
import maya.OpenMaya as om
import maya.OpenMayaAnim as omAnim

def getSkinCluster(dag):
    """A convenience function for finding the skinCluster deforming a mesh.

    params:
      dag (MDagPath): A MDagPath for the mesh we want to investigate. 
    """

    # useful one-liner for finding a skinCluster on a mesh
    skin_cluster = cmds.ls(cmds.listHistory(dag.fullPathName()), type="skinCluster")

    if len(skin_cluster) > 0:
      # get the MObject for that skinCluster node if there is one
      sel = om.MSelectionList()
      sel.add(skin_cluster[0])
      skin_cluster_obj = om.MObject()
      sel.getDependNode(0, skin_cluster_obj)

      return skin_cluster[0], skin_cluster_obj

    else:
        print(dag.partialPathName()+ " has not skin_cluster, skipped.")
        return None,None

meshWeights = {}
def saveLoadWeightsOneObj(path,isLoad):
    global meshWeights
    # get the selected mesh and components
    cmds.select(path)
    cmds.select(cmds.polyListComponentConversion(toVertex=True))
    sel = om.MSelectionList()
    sel.add(path)
    selected_components = om.MObject()
    dag = om.MDagPath()
    
    sel.getDagPath(0, dag, selected_components)
    dag.extendToShape()

    if dag.apiType() != 296:
      om.MGlobal.displayError("Selection must be a polygon mesh.")
      return
    
    skin_cluster,skin_cluster_obj = getSkinCluster(dag)
    if not skin_cluster_obj:
        return

    # cmds.skinPercent(skin_cluster, pruneWeights=0.005)
    mFnSkinCluster = omAnim.MFnSkinCluster(skin_cluster_obj)
    
    inf_objects = om.MDagPathArray()
    # returns a list of the DagPaths of the joints affecting the mesh
    mFnSkinCluster.influenceObjects(inf_objects)
    
    inf_count_util = om.MScriptUtil(inf_objects.length())

    # c++ utility needed for the get/set weights functions
    inf_count_ptr = inf_count_util.asUintPtr()
    inf_count = inf_count_util.asInt()
    influence_indices = om.MIntArray()

    # create an MIntArray that just counts from 0 to inf_count
    for i in range(0, inf_count):
      influence_indices.append(i)

    old_weights = om.MDoubleArray()
    # don't use the selected_components MObject we made since we want to get the weights for each vertex 
    # on this mesh, not just the selected one
    empty_object = om.MObject()
    mFnSkinCluster.getWeights(dag, empty_object, old_weights, inf_count_ptr)

    # new_weights just starts as a copy of old_weights
    new_weights = om.MDoubleArray(old_weights)

    # iterate over the selected verts
    itVerts = om.MItMeshVertex(dag, selected_components)
    if isLoad:
        meshWeight = meshWeights.get(dag.partialPathName())
        if not meshWeight:
            om.MGlobal.displayError("Not save yet")
            return
        # 将关节顺序和名称对上，做个映射表
        ori_weights = meshWeight["weights"]
        ori_inf_objects = meshWeight["inf_objects"]
        ori_inf_count = meshWeight["inf_count"]
        l1 = [testDuplicateName(inf_objects[i].partialPathName()) for i in range(inf_objects.length())]
        l2 = [testDuplicateName(ori_inf_objects[i].partialPathName()) for i in range(ori_inf_objects.length())]
        # ADV可能会将Root改成RootSide_R，这里修正
        if 'RootSide_R' in l1 and 'Root_M' in l1:
            l1[l1.index('Root_M')] = '___'
            l1[l1.index('RootSide_R')] = 'Root_M'

        # Spine1的修复
        for i in range(len(l2)):
            if not l2[i].endswith(('_L','_R','_M')):
                l2[i] += '_M'

        try:
            joint_map = [l2.index(l1[i]) if l1[i] in l2 else ori_inf_count for i in range(inf_count)]
            # tem = []
            # for j in l1:
            #     if j not in l2:
            #         tem.append(j)
            # print(l1)
            # print(l2)
            # print(tem)
            # print(len(l1),len(l2),len(tem))
        except Exception as e:
            om.MGlobal.displayError("ERROR: "+str(e))
            return

        while not itVerts.isDone():
            this_vert_weight_index = itVerts.index() * inf_count
            
            # print(vert_weights)
            # 恢复保存的权重，注意骨骼顺序
            ori_this_vert_weight_index = itVerts.index() * ori_inf_count
            ori_vert_weights = list(ori_weights[ori_this_vert_weight_index: ori_this_vert_weight_index + ori_inf_count])
            ori_vert_weights += [0]
            weights = [ori_vert_weights[joint_map[i]] for i in range(inf_count)]
            new_weights[this_vert_weight_index: this_vert_weight_index + inf_count] = weights[:]

            itVerts.next()
        # set weights all at once
        mFnSkinCluster.setWeights(dag, empty_object, influence_indices, new_weights, True, old_weights)
        print("load "+dag.partialPathName())
    else: # if isLoad
        meshWeight = {"inf_count":inf_count,"weights":new_weights, "inf_objects":inf_objects}
        meshWeights[dag.partialPathName()] = meshWeight
        print("save "+dag.partialPathName())
        
def saveLoadWeights(isLoad=True):
    global meshWeights
    original_sel = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(original_sel)
    selected = select_selected_mesh_and_children()
    if not selected:
        print("no selected")
        return
    
    for obj in selected:
        saveLoadWeightsOneObj(obj,isLoad)
        
    om.MGlobal.setActiveSelectionList(original_sel)

    