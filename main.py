import cv2
import serial
import time

# Initialize camera (0 is usually the default camera; change if needed)
cap = cv2.VideoCapture(0)

# Simulation mode: Set to True if no Arduino is connected, False when Arduino is ready
SIMULATION_MODE = True

if not SIMULATION_MODE:
    # Initialize serial communication (adjust 'COM3' to your Arduino port when available)
    ser = serial.Serial('COM3', 9600, timeout=1)  # Replace COM3 with your port
    time.sleep(2)  # Wait for serial connection to initialize

while True:
    # Read frame from camera
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert frame to HSV color space for red color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red1 = (0, 70, 50)    # Adjusted lower range for red (more lenient)
    upper_red1 = (10, 255, 255)  # Upper range for red
    lower_red2 = (170, 70, 50)   # Adjusted second range for red
    upper_red2 = (180, 255, 255)

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    stop_detected = False

    print(f"Number of contours found: {len(contours)}")  # Debug contour count
    for contour in contours:
        area = cv2.contourArea(contour)
        print(f"Contour area: {area}")  # Debug area
        if area > 500:  # Lowered area threshold from 1000 to 500
            # Approximate the contour to a polygon
            approx = cv2.approxPolyDP(contour, 3, True)
            sides = len(approx)
            print(f"Approximated sides: {sides}")  # Debug sides
            if sides == 8:  # Check for octagon shape
                stop_detected = True
                print("Stop sign detected!")
                break

    # Send signal based on detection
    if stop_detected:
        if SIMULATION_MODE:
            print("Simulated signal: 1 (Stop for 3 seconds)")
            time.sleep(3)  # Simulate 3-second hold
            print("Simulated signal: 0 (Resume moving)")
        else:
            ser.write(b'1')  # Send stop signal
            time.sleep(3)    # Hold for 3 seconds
            ser.write(b'0')  # Resume moving
    else:
        if not SIMULATION_MODE:
            ser.write(b'0')  # Keep moving if no stop sign

    # Display the frame and mask for debugging
    cv2.imshow('Frame', frame)
    cv2.imshow('Mask', mask)  # Show mask to visualize red detection
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
if not SIMULATION_MODE:
    ser.close()
print("Program ended")