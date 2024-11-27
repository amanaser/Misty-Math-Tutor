import os, sys
os.environ['RETICO'] = '/home/slimuser/Desktop/HRI/misty project/retico-core'
os.environ['RETICOV'] = '/home/slimuser/Desktop/HRI/misty project/retico-vision'
os.environ['YOLO'] = '/home/slimuser/Desktop/HRI/misty project/retico-yolov8'
os.environ['CLIP'] = '/home/slimuser/Desktop/HRI/misty project/retico-clip'

sys.path.append(os.environ['RETICO'])
sys.path.append(os.environ['RETICOV'])
sys.path.append(os.environ['YOLO'])
sys.path.append(os.environ['CLIP'])

import torch
from transformers import AutoModel
from retico_core import abstract
from retico_core.abstract import AbstractModule
from retico_core.text import TextIU
from retico_vision.vision import DetectedObjectsIU
from PIL import Image
import numpy as np
import retico_core


class ColorDetectionModule(abstract.AbstractModule):
    """
    A ReTiCo module that processes DetectedObjectsIU, uses a color detection model
    to identify colors, and outputs TextIU with detected color names.
    """

    @staticmethod
    def name():
        return "Color Detection Module"

    @staticmethod
    def description():
        return "Identifies colors in detected objects using a Hugging Face color detection model."

    @staticmethod
    def input_ius():
        return [DetectedObjectsIU]

    @staticmethod
    def output_iu():
        return TextIU

    def __init__(self, model_name="/home/slimuser/Desktop/HRI/misty project/colour-checker-detection-models/models/colour-checker-detection-l-seg.pt", **kwargs):
        super().__init__(**kwargs)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.load(model_name, map_location=self.device) 
        print("hey")
        # self.model.eval()

    def preprocess_image(self, pil_image):
        """
        Converts a PIL image to a tensor suitable for the Hugging Face model.
        """
        image_array = np.array(pil_image)
        # Normalize the image and convert to tensor
        tensor = torch.tensor(image_array).permute(2, 0, 1).float() / 255.0
        return tensor.unsqueeze(0).to(self.device)

    def process_color(self, obj_image):
        """
        Processes a single object image using the model to detect its color.

        Args:
            obj_image: A PIL Image of the detected object.

        Returns:
            Detected color name (str).
        """
        obj_tensor = self.preprocess_image(obj_image)
        with torch.no_grad():
            output = self.model(obj_tensor)

        self.model.eval()
        
        # Assuming output is logits, apply softmax to get probabilities
        color_predictions = torch.softmax(output, dim=-1)
        top_color_idx = torch.argmax(color_predictions, dim=-1).item()
        
        # Replace with actual color names if available in model output
        color_names = ["Color 1", "Color 2", "Color 3", "Color 4"]  # Example placeholder
        detected_color = color_names[top_color_idx]  # Get the name of the detected color
        return detected_color

    def process_update(self, update_message):
        """
        Processes an incoming DetectedObjectsIU and outputs a TextIU with detected colors.

        Args:
            input_iu: The DetectedObjectsIU containing detected objects.

        Returns:
            A new TextIU containing detected color names as text.
        """

        for iu, ut in update_message:
            if ut != retico_core.UpdateType.ADD:
                continue
            else:
                print(f"input_iu.image: {iu.payload}")

        detected_colors = []
        for obj in iu.payload:  # Assuming objects is a list of PIL Images
            detected_colors.append(self.process_color(obj))

        # Join detected colors into a single string
        color_text = ", ".join(detected_colors)
        output_iu = self.create_iu(iu)
        output_iu.text = f"Detected colors: {color_text}"
        print(f"output iu: {output_iu}")
        return output_iu

    # def process_update(self, update_message):
    #     """
    #     Processes the update message and generates output IUs.

    #     Args:
    #         update_message: The input update message containing DetectedObjectsIU.

    #     Returns:
    #         An output update message containing TextIU with detected colors.
    #     """
    #     output_ius = []
    #     for iu, update_type in update_message:
    #         if update_type == "add" and isinstance(iu, DetectedObjectsIU):
    #             output_iu = self.process_iu(iu)
    #             output_ius.append((output_iu, "add"))
    #     return self.create_update_message(output_ius)
