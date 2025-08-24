# Image Classifier & Gallery

A Streamlit web application that allows users to upload, automatically tag, and browse images using Cloudinary's AI-powered image recognition.

## Features

### Image Gallery
- **Upload Images**: Upload photos in various formats (PNG, JPG, JPEG, GIF, BMP)
- **Auto-Tagging**: Automatically generate tags using Cloudinary's AI detection
- **Browse by Tags**: Filter and view images by tags or tag combinations
- **Delete Images**: Remove images from your collection
- **Tag Display**: View all tags associated with each image

### Image Statistics
- **Tag Distribution**: Pie chart showing all tags and their frequencies
- **Top Tags**: Bar chart of the 10 most common tags
- **Tag Combinations**: Analysis of most common tag pairs

## Tech Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly Express
- **Image Storage**: Cloudinary
- **AI Tagging**: Cloudinary's OpenImages detection
- **Data Processing**: Pandas

## Setup & Installation

### Prerequisites
- Python 3.8+
- Cloudinary account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Wish2code/Image-Classifier.git
   cd Image-Classifier
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # source venv/bin/activate    # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Deployment on Streamlit Cloud

1. **Push to GitHub**: Ensure your code is pushed to a GitHub repository

2. **Connect to Streamlit Cloud**: 
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository

3. **Configure Secrets**:
   In your Streamlit Cloud app settings, add your Cloudinary credentials to the Secrets section:
   ```toml
   CLOUDINARY_URL = "cloudinary://api_key:api_secret@cloud_name"
   ```

## Usage

### Uploading Images
1. Navigate to the "Image Gallery" page
2. Use the file uploader to select an image
3. Click "Upload and Tag Image" to process and store the image
4. View the generated tags and image URL

### Browsing Images
1. Select a tag from the dropdown menu
2. View all images associated with that tag
3. Use the delete button to remove unwanted images

### Viewing Statistics
1. Navigate to the "Image Stats" page
2. Explore tag distributions and combinations
3. Analyze your image collection patterns

## File Structure

```
├── app.py                 # Main Streamlit application
├── cloudinary_service.py  # Cloudinary API integration
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (local only)
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## API Reference

### Cloudinary Service Functions

- `upload_and_tag_image(filename, folder)`: Upload image with auto-tagging
- `get_all_images_with_tags()`: Retrieve all images with their tags
- `delete_image(public_id)`: Delete an image from Cloudinary

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [Cloudinary](https://cloudinary.com/) for image storage and AI tagging
- [Plotly](https://plotly.com/) for data visualization