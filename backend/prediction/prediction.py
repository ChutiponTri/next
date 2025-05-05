import torch
import torchvision 
import torchvision.transforms as T
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.faster_rcnn import GeneralizedRCNNTransform
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from fastapi.responses import JSONResponse
from datetime import datetime, date
from PIL import Image
import io
from ..dependencies import get_token_header
from ..db_connection import get_db_connection

router = APIRouter(
    prefix="/predict",
    tags=["predict"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

# Number of classes: 1 background + 4 bed sore grades
NUM_CLASSES = 5  # Including the background class

# Pre-trained Faster R-CNN with ResNet50 backbone
def get_faster_rcnn_model():
    # Load pre-trained Faster R-CNN model with a ResNet50 backbone
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrain=True)
    
    # Get the input features from the pre-trained model's classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    
    # Replace the classifier with a new one that outputs NUM_CLASSES (4 classes + 1 background)
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, NUM_CLASSES)
    
    # Modify the image transform for your custom dataset (e.g., using 640x640 images)
    model.transform = GeneralizedRCNNTransform(min_size=640, max_size=640, image_mean=[0.485, 0.456, 0.406], image_std=[0.229, 0.224, 0.225])
    
    return model

# Create the model
model = get_faster_rcnn_model()

# Move model to the appropriate device (GPU or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load("model/latest_model.pth", map_location=device))
model.eval()

def get_transform(image):
    transform = T.Compose([
        T.ToTensor(),
        T.Resize((640, 640)),  # Stretch to 640x640
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),  # Standard normalization
    ])
    return transform(image)

def get_prediction(model, image, device=None):
    with torch.no_grad():
        # Move image to the device
        image = [image.to(device)]
        
        # Get predictions from the model
        outputs = model(image)
        
        # Process outputs
        for output in outputs:
            # Get the bounding boxes, labels, and scores
            pred_boxes = output['boxes'].cpu().numpy().tolist()
            pred_labels = output['labels'].cpu().numpy().tolist()
            pred_scores = output['scores'].cpu().numpy().tolist()

            # Find the index of the highest score
            max_score_idx = pred_scores.index(max(pred_scores))
            
            # Store predictions and ground truth
            predictions = {
                "pred_boxes": pred_boxes[max_score_idx],
                "pred_labels": pred_labels[max_score_idx],
                "pred_scores": pred_scores[max_score_idx],
            }

    return predictions

def allowed_file(filename: str):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/")
async def predict(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No File Uploaded")
    
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Format Not Supported")
    
    try:
        # Read the uploaded file
        img_bytes = await file.read()
        img = Image.open(io.BytesIO(img_bytes))
        
        # Preprocess the image and get predictions
        tensor = get_transform(img)
        prediction = get_prediction(model, tensor, device)
        
        # Create a response with the prediction
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error During Prediction: {str(e)}")




