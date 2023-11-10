代码：

https://github.com/PDE26jjk/MayaADVrename

尝试在Maya中将其他绑定好的模型添加ADV插件的控制器。

作品集里需要有能动的角色，所以学了下怎么蒙皮绑骨，刚开始学K帧。找到的教程用了AdvancedSkeleton5，我绑了几次骨骼之后感觉好麻烦，决定用已有的模型来学着做动画先。可是其他模型没有那些方方圆圆的控制器，手动创建太麻烦了，所以学了下Maya的脚本。

先找了个重命名的脚本（见参考），就在这个基础上改。

我所用的Maya版本是2019，培训班提供的。AdvancedSkeleton5版本是5.712，网上找的。插件4万行代码看得我脑壳疼。而且构建一出错场景就坏了，Maya的ctrl-z好像是一步步指令撤回来的，和执行一样的速度，很令人恼火。

关于对称关节，一开始的做法是将左边关节删掉，让ADV自动创建回来，构建好控制器再对回原来的位置。这样需要保存位置，名称，是否存在对应右边关节等，bug修不完，遂放弃。最后使用ADV的noMirror属性实现，在创建控制器之后把ADV改的后缀改回来。

关于蒙皮权重，ADV构建控制器必须要没绑定的骨骼，所以需要保存权重，解除绑定，构建好再绑回来，恢复权重。网上搜到了一些修改权重的资料（见参考），稍作修改就能应用于我的场景。直接解除绑定的话，如果骨骼姿势和模型的原来姿势不一样，会出现错位，这时需要解除绑定时烘焙历史。

<img src="https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110223158820.png" alt="image-20231110223158820" style="zoom: 50%;" />

代码是

```python
mel.eval('doDetachSkin "2" { "3","1" }')
```

以下是操作步骤：

## 一、摆绑定pose

把模型摆成Tpose或Apose，因为当前模型的姿势是控制器的位移旋转为0的姿势，这样便于让姿势归零。然后把根骨骼冻结变换，不然ADV构建时会把旋转归0，会自动生成一个组，然后这个关节的父对象就是组而不是上级关节了，就会出现找不到上级关节的错误（但凡保存下中间状态都不会出这么离谱的错误，可能新版本已经修复了bug）。

## 二、关节改名

把模型的关节改成ADV的格式，可以导入默认的biped.ma来对，可以用脚本来完成，批量修改

<img src="https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110225712139.png" alt="image-20231110225712139" style="zoom:50%;" />

示例脚本

```Python
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
```

## 三、保存权重、解除绑定、烘焙历史

保存权重我用脚本实现的（见参考），思路是将获取的权重值和骨骼顺序对应的名称保存下来。

解除绑定需要烘焙历史，不然骨骼绑定对不上模型，上面已经讲过了。

## 四、关节赋予ADV标签和属性

使用这个面板即可，选中关节，添加属性，可以点击问号看图示说明

![image-20231110232228712](https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110232228712.png)

当然我也写了脚本

```Python
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
```

这里没做手指那个曲线的，因为我找的模型关节数量对不上，各位可以按需修改。

## 五、ADV构建

<img src="https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110231809867.png" alt="image-20231110231809867" style="zoom:50%;" />

构建结果，这里用米家模型做示例。还需手动调整控制器曲线的大小，可能还要打组控制下位置，不过比从头来创建快多了。

![image-20231110233003780](https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110233003780.png)

## 六、关节名称修复

现在关节和FK、IK等会添加一个\_R或\_M的后缀，但是原来的关节已经有了一个后缀，所以会有`_*_*`这样的后缀，用正则把后面一个删掉即可

## 七、权重恢复

重新绑定后把保存的权重恢复即可。也是用的脚本，代码见仓库。

## 八、其他修复

ADV创建的Leg或Arm的IK名字是Leg1_R、Leg2_R之类的，应该是Leg_L，Leg_R，用ADV那个biped小公具选不上对应的关节。把名字替换即可。





最后在改名脚本的基础上放了几个按钮，对同一种模型可以一键加控制器。

<img src="https://raw.githubusercontent.com/PDE26jjk/misc/main/img/image-20231110234849130.png" alt="image-20231110234849130" style="zoom:67%;" />



### Python文件中文乱码：

加`\# -*- coding: utf-8 -*-`到文件头，VSCode文件格式改成GB 2312即可。

搞这个用了2天，有点本末倒置了。不说了，去看视频学K帧了。

### 参考：

重命名脚本：https://zhuanlan.zhihu.com/p/641096769

权重：https://www.artstation.com/blogs/benmorgan/72rD/maya-python-api-gettingsetting-skin-weights
