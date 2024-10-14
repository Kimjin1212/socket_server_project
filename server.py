import socket
import os
import datetime
import re

# Create 'request' directory to store requests
if not os.path.exists('request'):
    os.makedirs('request')

# Create 'images' directory to store images
if not os.path.exists('images'):
    os.makedirs('images')

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))  # Bind IP and port
server_socket.listen(5)  # Listen for up to 5 client connections

print("Server is running...")

# Save client request as a .bin file
def save_request_data(data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'request/{timestamp}.bin'
    
    with open(filename, 'wb') as f:
        f.write(data)
    
    print(f"Request data saved as {filename}")

# Save image data
def save_image_data(data):
    match = re.search(r'filename="(.+)"', data.decode('utf-8', errors='ignore'))
    if match:
        filename = match.group(1)
    else:
        filename = f'image_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
    
    filepath = f'images/{filename}'
    image_data = data.split(b'\r\n\r\n')[1].split(b'\r\n------')[0]
    
    with open(filepath, 'wb') as img_file:
        img_file.write(image_data)
    
    print(f"Image data saved as {filepath}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection accepted from {client_address}")
    
    data = client_socket.recv(8192)
    if data:
        if b'Content-Disposition: form-data' in data:
            save_image_data(data)
        else:
            save_request_data(data)
    
    client_socket.close()

