## FastBillingX – Smart Grocery Checkout

FastBillingX is a real-time grocery checkout system that uses computer vision to detect items and maintain a shopping cart automatically. The system integrates YOLOv8 for object detection, OpenCV for video processing, FastAPI for backend APIs, and MongoDB for storing cart items.

## Features

-Real-time detection of grocery items via webcam.

-Supports multiple grocery items. 

-Right-side cart overlay showing item names and counts.

-Debounce mechanism to prevent double counting.

-Backend storage using FastAPI + MongoDB.

## NOTE :
-I have used YOLOv8 model, which is pretrained on COCO dataset. So at present the system may only detect classes which are present in COCO dataset.
