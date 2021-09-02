# Image to terminal render engine
A barebone image to ASCII converter which adapts to unix terminal size.

<img src='cyber.png'>

<br>

<img src='cortana.png'>

<br>
<br>

# Usage
Set the terminal to the most optimal size
```bash
render.py think.jpg
```
<img src='think.png'>

Import allows to use the module in full fashion

```python
from render import image
# print with filled ascii (better for high resolution images)
image('cyber.png', printer=True, filled=True)
```