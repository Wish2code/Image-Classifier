
# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

# Import the Cloudinary libraries
# ==============================

import pathlib
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)

# Log the configuration
# ==============================
#print("****1. Set up and configure the SDK:****\nCredentials: ", config.cloud_name, config.api_key, "\n")

def upload_image(filename, folder='my_photos'):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(filename,public_id=stem,folder=folder)
    return res

def upload_and_tag_image(filename, folder='my_photos'):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(filename,public_id=stem,
                                    folder=folder, detection='openimages', auto_tagging=0.25)
    return res

#res = upload_and_tag_image('man.jpeg')
#print(res)
def get_all_tags():
    all_tags = []
    tags = cloudinary.api.tags(max_result=100)
    all_tags.extend(tags["tags"])
    next_cursor = tags.get("next_cursor")

    while next_cursor:
        tags = cloudinary.api.tags(max_result=100, next_cursor=next_cursor)
        all_tags.extend(tags["tags"])
        next_cursor = tags.get("next_cursor")
    return all_tags


def search_img():
    result = (
        cloudinary.Search()
        .expression("resource_type:image AND tags=wine")
        .sort_by("public_id", "desc")
        .execute()
    )
    return result


def get_all_images_with_tags():
    all_resources = []
    result = cloudinary.api.resources(
        type="upload",
        resource_type="image",
        prefix="my_photos",
        tags=True,
        max_result=100,
    )
    all_resources.extend(result["resources"])
    next_cursor = result.get("next_cursor")

    while next_cursor:
        result = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            prefix="my_photos",
            tags=True,
            max_result=100,
            next_cursor=next_cursor,
        )
        all_resources.extend(result["resources"])
        next_cursor = result.get("next_cursor")
    return all_resources


def delete_image(public_id):
    """Delete an image from Cloudinary by its public_id"""
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result
    except Exception as e:
        print(f"Error deleting image: {e}")
        return None

# all_resources = get_all_images_with_tags()
# print(all_resources)
# print(len(all_resources))