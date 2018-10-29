# Label_BoundingBox
A tool for labeling image level label.

# Requirement
- tkinter
- PIL
- NotoSansCJK-Black.ttc (if need Chinese characters)

# Usage
## for basic bbox-label-tool:
- Write down the classes in, for example, "cls231names.chs.txt". which joined with "_" (two levels label, one label per pline, eg: animal_cat animal_dog vehicle_car), and configure the txt path in src scripyt.
- Run python qxin_class.py -d image_dirs -i start_index
- To create a new label, press 0000 and "return"
- "backspace: to re type
- "left" or "right" to browser.
- label files are stored in "image_dirs" with suffix ".txt"
