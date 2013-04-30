3D-gesture-authentication
=========================

DESCRIPTION
Use Wii nunchuck and Arduino board to take in 3D vectors for gestures and dynamic time warping algorithm to recognize user for motion-based passwords. Final project during Hackbright.

INSTRUCTIONS

1. Run read_arduino.py to get data off Wii nunchuck through Arduino
- hold z-button (the bigger button on front of nunchuck) down while taking reading
- hit c-button (the smaller button) to close serial connection and exit read_arduino.py gracefully

2. Run server.py to get Open Sesame login app running locally.