## Blender Addon: Exclusive Groups

属するオブジェクトが互いに重複することのないグループ(`Exclusive Group`)を作成します。








===========

> ###### Usage

グループ名に`exc-`プレフィクスがついていれば、それがExclusive Groupとして認識されます。

<br>

* **_New_**
  * Exclusive Groupを新たに作成し、選択オブジェクトをアサインします。既にExclusive Groupがアサインされている場合は
自動的に消去された後、新たな方にアサインし直されます。

  ![image](https://raw.githubusercontent.com/wiki/a-nakanosora/blender-scripts/images/bl-exclusive-groups/explain1_new.gif)

<br>

* **_Join_**
  * 選択オブジェクトをアクティブオブジェクトの属するExclusive Groupにアサインします。  
グループ名がアクティブオブジェクトのものになる以外は**`New`**と同様です。

  ![image](https://raw.githubusercontent.com/wiki/a-nakanosora/blender-scripts/images/bl-exclusive-groups/explain2_join_.gif)

<br>

--

以下は補助的な機能になります

* **_Clean_**
  * 1つのオブジェクトが複数のExclusive Groupに属している場合、どれか1つのExclusive Groupのみに残します。  
  基本的にグループの生成やアサインを上の **`New`** や **`Join`** で行っていれば使うことはないはずですが、
  何らかの事故で1つのオブジェクトが複数のExclusive Groupに属することになった場合に使用してください。

* **_Remove from non-Exclusive Groups_**
  * 属しているグループのうちExclusive Groupでないグループ全てから外れます。主にExclusive Groupのみに属させたい場合に使います。
  
  ![image](https://raw.githubusercontent.com/wiki/a-nakanosora/blender-scripts/images/bl-exclusive-groups/explain3_clean.gif)

===========

> ###### Install

* Blender User Preferences > Install from File にて `excgroup.py` を選択

===========

> See Also:

* [Blender Addon - Group Amigo](https://github.com/a-nakanosora/Group-Amigo)
