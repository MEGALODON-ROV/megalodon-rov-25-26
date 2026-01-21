from inference import get_model
import supervision as sv
from inference.core.utils.image_utils import load_image_bgr
import cv2
from ultralytics import YOLO

def count_label (find_label):
    count = 0
    for label in labels_array:
        if(label == "person"):
            count += 1
    return count

cam = cv2.VideoCapture(0)

frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

decider = int(input("1. Picture Capture\n2. Live Capture\n-"))

# Picture Capture loop, regular camera view and press button to take picture
while decider == 1:
    ret, frame = cam.read()

    out.write(frame)
    cv2.imwrite('capture.jpg', frame)

    # video feed
    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.imwrite('capture.jpg', frame)
        break


# Live Feed Loop (basically caputres the yolo data live, but very laggy rn
while decider == 2:
    ret, frame = cam.read()

    out.write(frame)
    cv2.imwrite('capture.jpg', frame)

    # image rec stuff
    model = get_model(model_id="yolov8n-640")
    results = model.infer(image)[0]
    results = sv.Detections.from_inference(results)
    annotator = sv.BoxAnnotator(thickness=4)
    annotated_image = annotator.annotate(image, results)
    annotator = sv.LabelAnnotator(text_scale=2, text_thickness=2)
    annotated_image = annotator.annotate(annotated_image, results)

    # display image rec
    cv2.imshow('Annotated Vid Feed', annotated_image)


    if cv2.waitKey(1) == ord('q'):
        break

cam.release()
out.release()
cv2.destroyAllWindows()

# image_path = "/home/vihaankabra/Downloads/image_ rec_ test/mygrade2.jpg"
image_path = 'capture.jpg'
image = load_image_bgr(image_path)

model = get_model(model_id="yolov8n-640")
results = model.infer(image)[0]
results = sv.Detections.from_inference(results)
annotator = sv.BoxAnnotator(thickness=4)
annotated_image = annotator.annotate(image, results)
annotator = sv.LabelAnnotator(text_scale=2, text_thickness=2)
annotated_image = annotator.annotate(annotated_image, results)
sv.plot_image(annotated_image)

person_count = 0
labels_array = results.data['class_name']

person_count = count_label("person")

print(f"how many ppl: {person_count}")