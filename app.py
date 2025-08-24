import streamlit as st
import plotly.express as px
import pandas as pd
import tempfile
import os

from collections import Counter
from itertools import combinations

import cloudinary_service


@st.cache_data
def get_images_with_tags():
    return cloudinary_service.get_all_images_with_tags()


all_images = get_images_with_tags()

all_tags = []
all_tags_lists = []
for image in all_images:
    tags = image["tags"]
    if not tags or "person" in tags:
        continue
    all_tags.extend(tags)
    all_tags_lists.append(tags)

tag_counter = Counter(all_tags)

sorted_tags = [item for item in sorted(tag_counter.items(), key=lambda x: -x[1])]
sorted_tag_strings = [f"{item[0]} ({item[1]})" for item in sorted_tags]

combs = []
for tags_per_image in all_tags_lists:
    for comb in combinations(tags_per_image, 2):
        combs.append(comb)

most_common_combs = Counter(combs).most_common(20)


def show_images(images):
    columns = st.columns(3)
    for idx, img in enumerate(images):
        col = columns[idx % 3]
        url = img["url"]
        if url.endswith(".heic"):
            url = url[:-5] + ".jpg"
        with col:
            st.image(url)
            st.markdown(f"[Link]({url})")
            
            # Add delete button
            public_id = img.get("public_id", "")
            if public_id and st.button(f"🗑️ Delete", key=f"delete_{public_id}_{idx}"):
                with st.spinner("Deleting image..."):
                    try:
                        result = cloudinary_service.delete_image(public_id)
                        if result and result.get('result') == 'ok':
                            st.success("Image deleted successfully!")
                            # Clear cache and refresh
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error("Failed to delete image")
                    except Exception as e:
                        st.error(f"Error deleting image: {str(e)}")
            
            # Show tags for the image
            if img.get("tags"):
                st.caption(f"Tags: {', '.join(img['tags'])}")
            
            st.divider()


def image_page():
    # Upload section
    st.subheader("Upload New Image")
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg', 'gif', 'bmp'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
        
        # Upload and tag button
        if st.button("Upload and Tag Image"):
            with st.spinner("Uploading and analyzing image..."):
                try:
                    # Save uploaded file temporarily
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    # Upload to Cloudinary with auto-tagging
                    result = cloudinary_service.upload_and_tag_image(tmp_file_path)
                    
                    # Clean up temporary file
                    os.unlink(tmp_file_path)
                    
                    # Display results
                    st.success("Image uploaded successfully!")
                    st.write("**Generated Tags:**", ", ".join(result.get('tags', [])))
                    st.write("**Image URL:**", result['secure_url'])
                    
                    # Clear cache to refresh the image list
                    st.cache_data.clear()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error uploading image: {str(e)}")
    
    st.divider()
    
    # Existing tag selection
    st.subheader("Browse Existing Images")
    options = sorted_tag_strings[:20]
    for item in most_common_combs:
        options.append(f"{item[0][0]}, {item[0][1]} ({item[1]})")

    tag = st.selectbox("Select tag", options)

    if tag:
        idx = tag.find("(")
        tag = tag[: idx - 1]
    if tag and "," in tag:
        # multiple tags
        tag1, tag2 = tag.split(",")
        tag1, tag2 = tag1.strip(), tag2.strip()
        images_with_tag = [
            img for img in all_images if tag1 in img["tags"] and tag2 in img["tags"]
        ]
    else:
        images_with_tag = [img for img in all_images if tag in img["tags"]]
    show_images(images_with_tag)


def stats_page():
    # Get all tags sorted by frequency
    sorted_tag_items = sorted(tag_counter.items(), key=lambda x: -x[1])
    labels = [item[0] for item in sorted_tag_items]
    counts = [item[1] for item in sorted_tag_items]

    st.markdown(f"#### All Tags Distribution")

    df = pd.DataFrame(list(zip(labels, counts)), columns=["Tags", "Counts"])
    fig = px.pie(df, values="Counts", names="Tags")
    fig.update_traces(textinfo="label+percent")
    fig.update_layout(width=700, height=700)
    st.plotly_chart(fig)

    st.markdown(f"#### Top 10 Tags")
    df_top10 = pd.DataFrame(list(zip(labels[:10], counts[:10])), columns=["Tags", "Counts"])
    fig = px.bar(df_top10, x="Tags", y="Counts")
    fig.update_layout(width=800, height=500)
    st.plotly_chart(fig)

    st.markdown(f"#### Most common combinations")

    labels = [str(x[0]) for x in most_common_combs][::-1]
    counts = [x[1] for x in most_common_combs][::-1]

    df = pd.DataFrame(list(zip(labels, counts)), columns=["Combinations", "Counts"])
    fig = px.bar(df, x="Counts", y="Combinations", orientation="h")
    fig.update_layout(width=800, height=600)
    st.plotly_chart(fig)


if __name__ == "__main__":
    options = ("Image Gallery", "Image Stats")
    selection = st.sidebar.selectbox("Menu", options)

    if selection == "Image Gallery":
        st.title("Image Gallery")
        image_page()
    else:
        st.title("Image Stats")
        stats_page()
