import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, UnidentifiedImageError  # Handle image errors
import cv2

# Ensure input/output folders exist
os.makedirs("input", exist_ok=True)
os.makedirs("output", exist_ok=True)

class ImageEnhancerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Enhancer & Upscaler - Developed by JR The Electronic Guy")
        self.root.geometry("700x500")

        # Tab Control for Input/Output tabs
        tab_control = ttk.Notebook(self.root)
        self.input_tab = ttk.Frame(tab_control)
        self.output_tab = ttk.Frame(tab_control)

        tab_control.add(self.input_tab, text="Input Image")
        tab_control.add(self.output_tab, text="Output Image")
        tab_control.pack(expand=1, fill="both")

        # Input Tab UI Elements
        self.upload_btn = ttk.Button(
            self.input_tab, text="Upload Image", command=self.upload_image
        )
        self.upload_btn.pack(pady=20)

        self.input_image_display = tk.Label(self.input_tab)
        self.input_image_display.pack(pady=10)

        self.enhance_btn = ttk.Button(
            self.input_tab, text="Enhance & Upscale", command=self.enhance_image, state=tk.DISABLED
        )
        self.enhance_btn.pack(pady=10)

        # Output Tab UI Elements
        self.output_image_display = tk.Label(self.output_tab)
        self.output_image_display.pack(pady=10)

        self.input_path = ""

    def upload_image(self):
        """Handles image upload."""
        file_path = filedialog.askopenfilename(
            initialdir="input",
            title="Select an Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            try:
                # Attempt to load the image to confirm it's valid
                img = Image.open(file_path)
                img.verify()  # Check for corrupt images

                self.input_path = file_path  # Store the valid file path
                self.display_image(file_path, self.input_image_display)
                self.enhance_btn.config(state=tk.NORMAL)  # Enable the button

            except UnidentifiedImageError:
                messagebox.showerror("Error", "Invalid or corrupt image file.")
                self.enhance_btn.config(state=tk.DISABLED)

            except Exception as e:
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
                self.enhance_btn.config(state=tk.DISABLED)

    def display_image(self, image_path, display_widget):
        """Displays an image in the provided widget."""
        img = Image.open(image_path).resize((300, 300), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        display_widget.config(image=img_tk)
        display_widget.image = img_tk

    def enhance_image(self):
        """Enhances and upscales the image."""
        if not self.input_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        # Read the image using OpenCV
        img = cv2.imread(self.input_path)

        # Apply a sharpening filter
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        enhanced_img = cv2.filter2D(img, -1, kernel)

        # Upscale the image (doubling the size)
        upscaled_img = cv2.resize(enhanced_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # Save the enhanced image to the output folder
        output_path = os.path.join("output", "enhanced_upscaled.jpg")
        cv2.imwrite(output_path, upscaled_img)

        # Display the enhanced image
        self.display_image(output_path, self.output_image_display)
        messagebox.showinfo("Success", f"Image saved to: {output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEnhancerApp(root)
    root.mainloop()
