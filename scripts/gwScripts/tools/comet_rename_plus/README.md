# ![Comet Rename Plus+](https://github.com/guywolfus/gwScripts/blob/main/icons/comet_rename_plus.png) Comet Rename Plus+
A simple renaming GUI that allows renaming operations such as Prefix, Suffix, Search and Replace, and Rename and Number.  
Created by Guy Wolfus.

![Comet Rename Plus+](https://static.wixstatic.com/media/eaa8d1_46bff5eea1204a4783611f2f6c5d48e0~mv2.png)

A Python adaptation of the original MEL script:  
Comet Rename by Michael B. Comet  
<https://www.comet-cartoons.com/maya.html>

## Description:
Works properly on any hierarchy, even if renaming nodes in the hierarchy out of order.
Adapted into Python, this version includes several quality-of-life improvements:
* Consistent window instance: keeps the user's text input the same every time you open the tool.
* "Clear Text" built-in button to easily clear each line edit.
* Capped padding at double-digit values to prevent accidental crashes when renaming with a name that is too long.
* Support for dockable window behavior.

## Features:

#### Prefix
Easily add a specified prefix to the names of selected nodes. This is useful for organizing and categorizing nodes based on their roles or types.

#### Suffix
Add a suffix to the names of selected nodes. This can help in distinguishing nodes that share similar names or belong to the same group.

#### Search and Replace
Search for specific substrings within node names and replace them with a new substring. This feature allows for quick and efficient renaming of multiple nodes based on a common pattern.

#### Rename and Number
Rename nodes with a base name followed by a sequential number. Options include setting the padding for the numbers (e.g. 001, 002) and specifying the starting number. This is particularly useful for creating ordered lists of nodes.

## How to Use:
In the script editor, use the following Python command:
```markdown
from gwScripts.tools import CometRenamePlus
CometRenamePlus.run()
```

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/guywolfus/gwScripts/blob/main/LICENSE) file for details.

##### NOTE: Does not support versions of Maya below 2017. If you've encountered any bugs or issues, please feel free to reach out to me at: <guywolfus@gmail.com>

##### "Comet Rename" originally created by:<br>Michael B. Comet - <comet@comet-cartoons.com><br>Copyright 2003 Michael B. Comet - All Rights Reserved.
