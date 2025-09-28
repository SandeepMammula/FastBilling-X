import cv2
from ultralytics import YOLO
from cart_utils import update_cart, cart

MODEL_PATH = "computer_vision/models/yolov8s.pt"
CONF_THRESHOLD = 0.7   

FRAME_WIDTH = 640  
FRAME_HEIGHT = 480
COUNT_ZONE_WIDTH = 250
ROI = (FRAME_WIDTH - COUNT_ZONE_WIDTH, 0, FRAME_WIDTH - 1, FRAME_HEIGHT - 1)


def is_inside_roi(x1, y1, x2, y2):
    rx1, ry1, rx2, ry2 = ROI
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return rx1 <= cx <= rx2 and ry1 <= cy <= ry2


def draw_cart_overlay(frame):
    """Draw cart items on right side of screen (no pricing)."""
    overlay = frame.copy() 
    x_start = frame.shape[1] - 250
    cv2.rectangle(overlay, (x_start, 0), (frame.shape[1], frame.shape[0]), (0, 0, 0), -1)
    alpha = 0.6
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)

    y0 = 30
    cv2.putText(frame, "CART", (x_start+10, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    for i, (item, count) in enumerate(cart.items()):
        text = f"{item}: {count}"
        y = y0 + (i+1)*30
        cv2.putText(frame, text, (x_start+10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    return frame


def main():
    model = YOLO(MODEL_PATH)
    cap = cv2.VideoCapture(0)  

    if not cap.isOpened():
        print("Error: Cannot open camera.")
        return

    print("Starting real-time detection. Press 'q' to quit, 'c' to clear cart.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        results = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                name = model.names[cls_id]

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if is_inside_roi(x1, y1, x2, y2):
                    update_cart(name)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{name}", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Draw cart overlay
        frame = draw_cart_overlay(frame)

        rx1, ry1, rx2, ry2 = ROI
        cv2.rectangle(frame, (rx1, ry1), (rx2, ry2), (0, 0, 255), 2)  # Red box
        cv2.putText(frame, "COUNT ZONE", (rx1+10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
        cv2.imshow("YOLOv8 Grocery Checkout", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            cart.clear()
            print("[CART] Cleared.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
