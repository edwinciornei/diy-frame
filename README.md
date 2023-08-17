# Handcrafted Picture Frames

A simple web application built with Flask and MongoDB designed to showcase and sell handcrafted picture frames made with love and creativity by my mother-in-law. Users can view items, admins can upload new items, and interested buyers can contact the seller.

## Features:

- **Home Page**: Displays all items available in database with thumbnails, descriptions, and prices.
- **Contact Page**: Allows interested buyers to send contact messages. 
- **Admin Authentication**: Secure admin panel for managing and uploading new items.
- **Image Hashing**: Prevents the uploading of duplicate items by hashing image data.
- **Dynamic Image Loading**: Images are stored in MongoDB and served dynamically based on their SHA256 hash.
- **Security**: Unauthorized users trying to access admin features are redirected.

  
## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/edwinciornei/diy-frame.git
   ```

2. **Install Dependencies**:  
   Navigate to the project directory and install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up MongoDB**:  
   Make sure you have MongoDB running on your system. Update the connection string if needed in the application code.

4. **Run the Application**:
   ```bash
   python main.py
   ```
   Access the app on [http://localhost:80/](http://localhost:80/).

5. **Contribution**:  
   If you have suggestions or want to improve the app, feel free to fork the repo, make your changes, and submit a pull request. Contributions are welcome!

---

Crafted by **edwinciornei**
