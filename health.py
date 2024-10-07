from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API key is missing. Please check your environment variables.")
else:
    genai.configure(api_key=api_key)

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_prompt, image):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        st.error(f"Error in API call: {e}")
        return None

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health App")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit = st.button("Tell me the total calories")

    input_prompt = """
    You are an expert in nutrition. Please analyze the food items in the image.
    Tell us the items or ingredients that can be seen in the image, and calculate the total calories.
    Provide the details of every food item with calorie intake in the format below:

    1. Item 1 - number of calories
    2. Item 2 - number of calories
    ----
    ----

    Also, tell what the image contains.
    """

    # If submit button is clicked
    if submit:
        with st.spinner("Processing image..."):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)

            if response:
                st.subheader("The Response is")
                st.write(response)
