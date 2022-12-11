image_cloud
==========

A little function based on the [word_cloud](https://github.com/amueller/word_cloud) generator to create a cloud, but with images.

![Image Cloud](assets/image_cloud.png)

## Installation

Install wordcloud via pip
```
pip install wordcloud
```

Then import the CloudBuilder and get started!
```python
from PIL import Image
from image_cloud import CloudBuilder

cloud = CloudBuilder(height=2000, width=2000)
canvas = cloud.generate(imgs, retries=10)
Image.fromarray(canvas).save("image_cloud.png")
```
