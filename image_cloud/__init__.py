import numpy as np
from random import Random

from PIL import Image

from wordcloud.wordcloud import IntegralOccupancyMap


class CloudBuilder:
    def __init__(self, height, width, margin=2, bg_color=255):       
        self.height = height
        self.width = width
        self.margin = margin
        self.bg_color = bg_color
        self.random_state = Random()
        
    def generate(self, images, scales=None, retries=1, retry_scale=0.6):
        """
        Numpy returns height, width
        PIL returns width, height
        """

        canvas = np.ones((self.height, self.width, 3)).astype(np.uint8) * self.bg_color
        occupancy = IntegralOccupancyMap(self.height, self.width, mask=None)

        if scales is None:
            scales = [1] * len(images)

        for img, scl in zip(images, scales):
            
            # Resize the image
            for r in range(retries):
                if r != 0:
                    scl *= retry_scale
                img_scaled = np.array(Image.fromarray(img).resize((int(img.shape[1] * scl), int(img.shape[0] * scl))))
                img_h, img_w = img_scaled.shape[:2]

                # Check to see if there's a place for the image
                result = occupancy.sample_position(img_h + self.margin, img_w + self.margin, self.random_state)
                if result is not None:
                    break
            else:
                break
            
            # Get the top left coord of the image location
            h, w = np.array(result) + self.margin // 2

            # Paste the image into the canvas
            canvas[h:h+img_h, w:w+img_w, :][img_scaled != self.bg_color] = img_scaled[img_scaled != self.bg_color]
            
            # Update the occupancy canvas
            occupancy_mask = (canvas != self.bg_color).any(axis=2)
            occupancy.update(occupancy_mask, h, w)

        return canvas
