#!/usr/bin/env python3
"""
OAK-D Camera Test - Using ColorCamera
Based on official DepthAI example
"""

import cv2
import depthai as dai

print("=" * 60)
print("OAK-D Camera Test")
print(f"DepthAI Version: {dai.__version__}")
print("=" * 60)

# Check devices
devices = dai.Device.getAllAvailableDevices()
print(f"\n✅ Found {len(devices)} OAK-D device(s)")

# Create pipeline
pipeline = dai.Pipeline()

# Define source - ColorCamera
camRgb = pipeline.create(dai.node.ColorCamera)
camRgb.setPreviewSize(640, 480)
camRgb.setInterleaved(False)

# Try to create XLinkOut
try:
    xoutRgb = pipeline.create(dai.node.XLinkOut)
    xoutRgb.setStreamName("rgb")
    camRgb.preview.link(xoutRgb.input)
    print("✅ Using dai.node.XLinkOut")
except AttributeError:
    print("⚠️  dai.node.XLinkOut not found, trying alternatives...")
    # Try without .node
    try:
        xoutRgb = pipeline.create(dai.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.preview.link(xoutRgb.input)
        print("✅ Using dai.XLinkOut")
    except:
        print("❌ Cannot create XLinkOut node")
        exit(1)

print("\n🎥 Starting camera...")

# Connect to device
with dai.Device(pipeline) as device:
    print(f"✅ Camera started!")
    print(f"   USB Speed: {device.getUsbSpeed().name}")
    print(f"   Device: {device.getDeviceName()}")
    print("\nPress 'q' to quit")
    print("=" * 60 + "\n")
    
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    
    frame_count = 0
    
    while True:
        inRgb = qRgb.get()
        frame = inRgb.getCvFrame()
        
        frame_count += 1
        
        # Add overlay
        cv2.putText(frame, f"OAK-D Camera - Frame: {frame_count}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to quit", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("OAK-D Camera", frame)
        
        if cv2.waitKey(1) == ord('q'):
            print("\nStopping camera...")
            break

cv2.destroyAllWindows()
print("\n" + "=" * 60)
print("✅ SUCCESS! Your OAK-D camera is working!")
print("=" * 60)
