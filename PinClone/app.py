import os
import json
import torch
import clip
import numpy as np
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Load CLIP model
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL, PREPROCESS = clip.load("ViT-B/32", device=DEVICE)

TAGS = ["fantasy", "sci-fi", "warrior", "mech", "landscape", "dark", "cute", "robot", "mage", "dinosaur", "nature", "cyberpunk", "steampunk", "abstract", "anime", "art", "arknights", "magic", "gun"]

IMAGE_FOLDER = "./drawings"
DATA_FILE = "image_data.json"

def extract_features_and_tags(image_path):
    image = PREPROCESS(Image.open(image_path)).unsqueeze(0).to(DEVICE)
    text_tokens = clip.tokenize(TAGS).to(DEVICE)

    with torch.no_grad():
        image_features = MODEL.encode_image(image).cpu().numpy()[0]
        text_features = MODEL.encode_text(text_tokens)
        sims = (MODEL.encode_image(image) @ text_features.T).squeeze(0)
        top_tags = [TAGS[i] for i in sims.topk(3).indices]

    return image_features.tolist(), top_tags

def index_images():
    data = {}
    for file in os.listdir(IMAGE_FOLDER):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            path = os.path.join(IMAGE_FOLDER, file)
            features, tags = extract_features_and_tags(path)
            data[file] = {"features": features, "tags": tags}
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def find_similar_images(selected_file, data, top_k=5):
    selected_vector = np.array(data[selected_file]["features"]).reshape(1, -1)
    all_vectors = [np.array(info["features"]) for info in data.values()]
    keys = list(data.keys())
    sims = cosine_similarity(selected_vector, all_vectors)[0]
    top_indices = np.argsort(sims)[-top_k - 1:][::-1]  # skip self
    return [keys[i] for i in top_indices if keys[i] != selected_file][:top_k]

# Streamlit UI
st.title("🖼️ Personal Pinterest - AI Tagger & Recommender")

if st.button("📦 Index All Images"):
    index_images()
    st.success("Images indexed and tagged!")

if os.path.exists(DATA_FILE):
    data = load_data()
    selected_file = st.selectbox("Choose an image", list(data.keys()))
    if selected_file:
        st.image(os.path.join(IMAGE_FOLDER, selected_file), caption=selected_file)
        st.write("Tags:", ", ".join(data[selected_file]["tags"]))

        st.subheader("🔁 Similar Images")
        similar_files = find_similar_images(selected_file, data)
        for fname in similar_files:
            st.image(os.path.join(IMAGE_FOLDER, fname), caption=fname, width=200)
else:
    st.warning("No image data found. Click the index button above.")
