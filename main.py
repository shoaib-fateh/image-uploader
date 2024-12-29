import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests

# ImgBB API key (ensure you store it securely, not hardcoded in your code)
IMGBB_API_KEY = "20f6fa9a3febdd99b1a59b3fe028db1f"  # Replace with your actual ImgBB API key
IMGBB_URL = "https://api.imgbb.com/1/upload"

# Function to upload image to ImgBB
def upload_image():
    # Open file dialog to choose an image
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    
    if not image_path:  # If no file is selected
        return

    # Get image name from the path
    image_name = image_path.split("/")[-1]

    try:
        # Open the selected image in binary mode and upload it to ImgBB
        with open(image_path, "rb") as image_file:
            files = {
                'image': image_file,
            }
            payload = {
                'key': IMGBB_API_KEY,
            }
            response = requests.post(IMGBB_URL, data=payload, files=files)

        if response.status_code == 200:
            # Get the URL of the uploaded image
            public_url = response.json()['data']['url']
            messagebox.showinfo("Success", f"Image uploaded successfully!\nPublic URL: {public_url}")
            display_uploaded_image(image_path)  # Display the uploaded image
        else:
            messagebox.showerror("Error", "Failed to upload image.")
    except Exception as e:
        messagebox.showerror("Error", f"Error uploading image: {e}")

# Function to display the uploaded image
def display_uploaded_image(image_path):
    # Open and resize the image
    img = Image.open(image_path)
    img = img.resize((300, 300))  # Resize to fit in the window
    
    # Convert image to Tkinter format
    img_tk = ImageTk.PhotoImage(img)
    
    # Update the label to show the image
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

# Set up the main window using Tkinter
root = tk.Tk()
root.title("ImgBB Image Upload")

# Window size and style
root.geometry("600x600")
root.config(bg="#f4f4f4")  # Light gray background

# Title label
title_label = tk.Label(root, text="Upload Your Product Image", font=("Arial", 18, "bold"), bg="#f4f4f4")
title_label.pack(pady=20)

# Button to trigger image upload
upload_button = tk.Button(root, text="Upload Image", command=upload_image, font=("Arial", 14), bg="green", fg="white", relief="flat")
upload_button.pack(pady=20)

# Label to display the uploaded image
image_label = tk.Label(root, bg="#f4f4f4")
image_label.pack(pady=20)

# Run the Tkinter main loop
root.mainloop()
