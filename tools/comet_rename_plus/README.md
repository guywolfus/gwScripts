# gwCometRenamePlus+

## Author:
Created by Guy Wolfus.
<br>A Python adaptation of the original MEL script:
<br>Comet Rename by Michael B. Comet
<br>https://www.comet-cartoons.com/maya.html

## Description:
A simple renaming GUI utility that allows basic Prefix, Suffix, Search &amp; Replace, and Rename+Number methods.
Works properly on any hierarchy, even if renaming nodes in the hierarchy out of order.
This new Python adaptation includes several quality-of-life improvements:
* Consistent window instance keeps the user's text input
  the same every time you open the tool.
* "Clear Text" built-in button to easily clear each line edit.
* Capped padding at double-digit value to prevent accidental
  crashes when renaming with a name that is too long.
* Support for dockable window behavior.

## How to Use:
In Maya, use the following Python code to run the tool:
```markdown
from gwScripts.tools import gwCometRenamePlus
gwCometRenamePlus.run()
```

##### NOTE: Does not support versions of Maya below 2017. <br>If you've encountered any bugs or issues, please feel free to reach out to me at: guywolfus@gmail.com

<br>"Comet Rename" originally created by:
<br>Michael B. Comet - comet@comet-cartoons.com
<br>Copyright 2003 Michael B. Comet - All Rights Reserved.
