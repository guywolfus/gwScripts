# ![Shots Data Manager](https://github.com/guywolfus/gwScripts/blob/main/icons/shots_data_manager.png) Shots Data Manager
A handy tool for Maya that allows splitting a scene into several other scenes. Mainly envisioned to be used by layout artists on a sequence in order to split it into numbered shots, reducing repetitive shot-prep work and allowing a more camera continuity-friendly workflow.  
Created by Guy Wolfus.

![Shots Data Manager](https://static.wixstatic.com/media/eaa8d1_9fd271468eae40f39fc3dbe96bd18775~mv2.png)

## Features:

#### Shots Table
Displays shots by their name and frame range in a clear, editable format, making it easy to review and manage shot splicing.
* `Insert Row`: Adds a new empty row to the table.
* `Remove Row`: Removes the selected row in the table.
* `Get Shots from Selected...`: Samples the keyframes on the selected object in the scene in order to determine the shots' frame ranges.
* `Clear...`: Clears the table entirely.  

#### Rename Shots
Allows a quick and simple way to rename all of the existing shots in the table, based on predetermined parameters. Provides an example text that shows how the shots will be named once you hit `Apply...`.  

#### Settings
Export options for the spliced shots.
* `Export Path`: Sets where the shots will be saved to. The `Export` button will only be enabled once this path is set correctly.
* `Normalize Frames on Export`: This option lets you decide whether to normalize the starting frame of the new shots. e.g. a shot that's defined in the table by the frame range of 25-69, if normalized to start on frame 0, the newly created scene file will have the range of 0-44 (effectively shifting the scene back by 25 frames).
* `Save As`: Define the Maya filetype for the new scene files, either ".ma" or ".mb".

#### Preset
The `Save Preset` and `Load Preset` menu options let you store and apply the tool's state, such as shot data (keeping shot names, start, and end frames), renaming and export options for quick access and reuse.

## How to Use:
In the script editor, use the following Python command:
```markdown
from gwScripts.tools import ShotsDataManager
ShotsDataManager.run()
```

## License
This project is licensed under the Apache 2.0 License. See the [LICENSE](https://github.com/guywolfus/gwScripts/blob/main/LICENSE) file for details.

##### NOTE: Does not support versions of Maya below 2017. If you've encountered any bugs or issues, please feel free to reach out to me at: <guywolfus@gmail.com>
