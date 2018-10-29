# Label_ClassificationLabel
- A tool for labeling image level label.

- To simplify the labeling process, e.g. 1000 labels, we can organise the lebel into two level
- for example:

    animal_cat
    
    animal_dog
    
    ...
    
    vehicle_car
    

# Requirement
- tkinter
- PIL
- NotoSansCJK-Black.ttc (if need Chinese characters)

# Usage
- Write down the classes in, for example, "cls231names.chs.txt". which joined with "_" (two levels label, one label per pline, e.g.: animal_cat animal_dog vehicle_car), and configure the txt path in src scripyt.
- Run 
    > python qxin_class.py -d image_dirs -i startIndex
    
    (eg.  python qxin_class.py -d ~/qxin/xx/images/ -i 350)
- To create a new label, press 0010 and "return". The first two number "00" means the top level of class, and 10 the second level.
- `backspace`: to re type
- "left" or "right" to browser.
- label files are stored in "image_dirs" with suffix ".txt"
