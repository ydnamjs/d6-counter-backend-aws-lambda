from torchvision.transforms import v2
from torchvision import transforms
import torchvision.models as models
import bbox_visualizer as bbv
from io import BytesIO
import base64
import torch
import numpy
import PIL
import cv2
from fastapi import FastAPI, HTTPException, Response, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from io import BytesIO
from PIL import Image
from mangum import Mangum
import base64

seed = 0
torch.manual_seed(seed)

LABEL_KEY = {
    0: "Unknown",
    1: "D%-0",
    2: "D%-10",
    3: "D%-20",
    4: "D%-30",
    5: "D%-40",
    6: "D%-50",
    7: "D%-60",
    8: "D%-70",
    9: "D%-80",
    10: "D%-90",
    11: "D4-1",
    12: "D4-2",
    13: "D4-3",
    14: "D4-4",
    15: "D6-1",
    16: "D6-2",
    17: "D6-3",
    18: "D6-4",
    19: "D6-5",
    20: "D6-6",
    21: "D8-1",
    22: "D8-2",
    23: "D8-3",
    24: "D8-4",
    25: "D8-5",
    26: "D8-6",
    27: "D8-7",
    28: "D8-8",
    29: "D10-1",
    30: "D10-2",
    31: "D10-3",
    32: "D10-4",
    33: "D10-5",
    34: "D10-6",
    35: "D10-7",
    36: "D10-8",
    37: "D10-9",
    38: "D10-10",
    39: "D12-1",
    40: "D12-2",
    41: "D12-3",
    42: "D12-4",
    43: "D12-5",
    44: "D12-6",
    45: "D12-7",
    46: "D12-8",
    47: "D12-9",
    48: "D12-10",
    49: "D12-11",
    50: "D12-12",
    51: "D20-1",
    52: "D20-2",
    53: "D20-3",
    54: "D20-4",
    55: "D20-5",
    56: "D20-6",
    57: "D20-7",
    58: "D20-8",
    59: "D20-9",
    60: "D20-10",
    61: "D20-11",
    62: "D20-12",
    63: "D20-13",
    64: "D20-14",
    65: "D20-15",
    66: "D20-16",
    67: "D20-17",
    68: "D20-18",
    69: "D20-19",
    70: "D20-20",
    71: "Unknown"
}

def reduce_contrast(image_array: numpy.ndarray, factor: float) -> numpy.ndarray:

    mean_intensity = numpy.mean(image_array, axis=(0, 1))

    reduced_contrast_image = mean_intensity + factor * (image_array - mean_intensity)

    reduced_contrast_image = numpy.clip(reduced_contrast_image, 0, 255)

    return reduced_contrast_image.astype(numpy.uint8)

NUM_CLASSES = 71
DETECTION_STATE_PATH = "./detector.pt"
CLASSIFIER_STATE_PATH = "./classifier.pt"
BBOX_COLOR = (255, 255, 255)
LABEL_BG_COLOR = (0, 0, 0)
LABEL_TEXT_COLOR = (255, 255, 255)
PAD_COLOR = (0, 0, 0)
PAD_AMT = 25

detection_model = models.detection.fasterrcnn_mobilenet_v3_large_320_fpn(weights=None, num_classes=2)
detection_model.load_state_dict(torch.load(DETECTION_STATE_PATH, weights_only=True))
detection_model.eval()

classification_model = models.mobilenet_v3_small(weights=None)
num_features = classification_model.classifier[3].in_features
classification_model.classifier[3] = torch.nn.Linear(num_features, NUM_CLASSES)
classification_model.load_state_dict(torch.load(CLASSIFIER_STATE_PATH, weights_only=True))
classification_model.eval()

transform = v2.Compose([
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

tensorify = transforms.Compose([
    transforms.ToTensor(),
])

def preprocess_image(image, threshold1, threshold2):
    imageArray = numpy.array(image)

    processed_image_array = cv2.resize(imageArray, (512, 512), interpolation=cv2.INTER_LANCZOS4)
    processed_image_array = cv2.GaussianBlur(processed_image_array, (5, 5), 0)
    processed_image_array = cv2.Canny(processed_image_array, threshold1=threshold1, threshold2=threshold2)

    return processed_image_array

def predict_image(preprocessed_image):

    imageTensor = tensorify(preprocessed_image)
    imageTensor = transform(imageTensor)

    with torch.no_grad():
        prediction = detection_model([imageTensor])

    scores = numpy.array(prediction[0]['scores'])
    boxes = numpy.array(prediction[0]['boxes']).astype(numpy.int32)

    predictions = []
    for box in boxes:

        x1, y1, x2, y2 = box

        subImageArray = preprocessed_image[int(y1):int(y2), int(x1):int(x2)]
        subImageArray = cv2.resize(subImageArray, (125, 125), interpolation=cv2.INTER_LANCZOS4)
        subImageArray = reduce_contrast(subImageArray, .5)
        subImageTensor = tensorify(subImageArray)
        subImageTensor = transform(subImageTensor)
        subImageTensor = torch.unsqueeze(subImageTensor, 0)
        output = classification_model(subImageTensor)

        predicted_class = torch.argmax(output, dim=1)
        predictions.append(predicted_class.item())

    return boxes, scores, predictions

def process_predictions(image, boxes, scores, predictions, scoreThreshold):

    imageArray = numpy.array(image)
    imageArray = cv2.resize(imageArray, (512, 512), interpolation=cv2.INTER_LANCZOS4)
    result = imageArray
    predicted_total = 0
    for i in range(0, len(boxes)):

        if scores[i] < scoreThreshold:
            continue

        label = LABEL_KEY[predictions[i]]
        predicted_total = predicted_total + predictions[i] + 1

        result = bbv.draw_rectangle(result, boxes[i], BBOX_COLOR, thickness=1)
        result = bbv.add_label(result, label, boxes[i], text_bg_color=LABEL_BG_COLOR, text_color=LABEL_TEXT_COLOR)

    return PIL.Image.fromarray(result), predicted_total

def image_to_base64(image: PIL.Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

class OutputModel(BaseModel):
    preprocessed_image: str
    output_image: str
    total: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"hello": "world"}

@app.post("/post-image")
async def process_frame(
    image64: Annotated[str, Form()], 
    canny_threshold_1: Annotated[int, Form()], 
    canny_threshold_2: Annotated[int, Form()], 
    confidence_threshold: Annotated[float, Form()]
):

    imageDecoded = base64.b64decode(image64)
    image = Image.open(BytesIO(imageDecoded))
    preprocessed_image_array = preprocess_image(image, canny_threshold_1, canny_threshold_2)
    boxes, scores, predictions = predict_image(preprocessed_image_array)
    outputImage, predicted_total = process_predictions(image, boxes, scores, predictions, confidence_threshold)

    img_byte_arr = BytesIO()
    outputImage.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    return OutputModel(
        preprocessed_image=image_to_base64(Image.fromarray(preprocessed_image_array)),
        output_image=image_to_base64(outputImage),
        total=predicted_total
    )

handler = Mangum(app)