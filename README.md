# pcr-battle
根据box和轴的自动排刀软件，基于python，不考虑尾刀的白嫖，欢迎加入一起交流

## 使用方式
- 首先，需要录入所有成员的box情况和所有会战的轴的情况
在`box表.xlsx`中录入box，自己可以调整表格的行数（加人和删人），或者调整表格的列数（加入或者删除角色），**如果box表中这个位置为空，则表示此人无法使用这个角色进行工会战**，如果表示拥有这个角色并且可以出场工会战，保持单元格非空即可，填写具体什么内容可以根据下面的`轴限定`环节调整，此外，对于4.0版本以上的软件，请保证最后**最后3列为 ‘已出刀（不写借人）’**。
在`已出刀`中填写相应内容的话，表示他已经出过一刀，软件会为他排出未出刀的套餐，并且人物不会冲突
对于角色的称呼的填写可以直接填写官方的标准称呼，或者填写常用别称昵称等等均可，想了解有哪些别称可以用，点击[这里](https://github.com/Ice-Cirno/HoshinoBot/blob/master/hoshino/modules/priconne/_pcr_data.py)。
>请注意七七香和nnk的区别

`box表.xlsx`示例如下

| |昵称|狼|狗|充电宝|黑骑|已出刀（不写借人）|已出刀（不写借人）|已出刀（不写借人）|
|-|-|-|-|-|-|-|-|-|
|1|行者孙|120开专|4x|开专|||
|2|好心的佑树|满专|3x|满专|4x|狼 狗 充电宝 |
|3|广告位出租|121满专|5x||满专|


- 对于会战轴表的录入请放在`轴表.xlsx`中，可以自由增加删除轴
    - 第一列表示boss的名称，目前支持3个阶段"a","b","c"
    - 第二列表示所录入的轴使用的角色，每个**角色之间使用空格隔开**，对于角色名称的使用仍然可以使用官方称谓或者别称
    - 第三列表示这个轴的伤害，目前只支持`数字w`的这种格式
    - 第四列表示借人限定，表示这个轴指定可以借那些角色进行出战，如果可以借的角色有很多，那么也请使用空格隔开，名称写法同上。**如果不填写表示所有角色均可以借**，锁借之人请保证公会内有人拥有这个角色，软件未判别公会内是否拥有这个角色。
    - 之后各列可以写这个轴所限定的角色的rank，等级，专武等等。
    具体填写方式如下，需要结合`box表.xlsx`填写。
    示例填写`狼 r9-5 r9-6`
    表示这个轴只能用`r9-5`，`r9-6`出刀，限定不同部分用空格隔开，第一个部分为限定的轴中的*角色*，名称填写方式同上，后面所跟随的为限定*内容部分*，如果一个多种情况均可打，那么不同的内容用空格隔开。这种限定表示只有在`box表.xlsx`中填写`r9-5`或者填写`r9-6`的人可以打，或未拥有这种限定的角色的人需要借这种角色才可以。
    限定的*内容部分*可以任意填写，不止局限于等级，rank等等，只用保证`box表.xlsx`单元格中内容和*限定内容部分*匹配即可。如限定填写`狼 120r11专30 121r11无专`这种填写方式，那在`box表.xlsx`填写`120r11专30`,`121r11无专`才会被认为是符合要求，否则无法匹配。
    如果限定多个人，则在后面紧随的单元格填写即可。
    
    `轴表.xlsx`示例如下
    |boss|阵容|伤害|借人|限定1|限定2|
    |-|-|-|-|-|-|
    |a5|xcw 妹法 水黑 黑猫 yly|120w||xcw 4x| 妹法 1专|
    |a1|黑骑 狼 狗 充电宝 tp弓|100w|狼 狗|||
    |a3|黑骑 狼 511 充电宝 暴击弓|90w|狼 511|黑骑 满专||

- `进度.txt`进行设置此次排刀计划攻击的boss，对于每个boss需要在后面填写计划打掉了目标血量，比如需要打3个a3王，a3的血量是1000万，那么需要填写`...   "a3":3000,   ...`注意逗号的有无和中英文，文件中需要全部为**英文逗号**。对于每一个需要打掉的王都需要填写，自己也可以灵活调整血量，以面对不同的情况。
对于`mode`后面的数字，自己可以根据需求更改，为软件规划的目标，**1表示计算最少的刀数达到目标，2表示最小出刀人数达到目标，3表示达到目标即可无需优化，一般3用于排刀组合数过大，计算时间过长的一个解决策略**



- 关闭所有电子表格和`进度.txt`，之后运行`main.exe`或者代码运行`main.py`即可，最终排刀的结果位于`排刀表.xls`中