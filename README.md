# Garage Sale Web Application 🏷️💲

A simple web application built with Flask and MongoDB for displaying and managing items in a garage sale. Users can view items, admins can upload new items, and interested buyers can contact the seller.

## Features:

- **Home Page**: Displays all items with thumbnails, descriptions, and prices.
- **Contact Page**: Allows interested buyers to send contact messages. 
- **Admin Authentication**: Secure admin login page to manage the items.
- **Image Hashing**: Prevents the uploading of duplicate items by hashing image data.
- **Dynamic Image Loading**: Images are stored in MongoDB and served dynamically based on their SHA256 hash.
