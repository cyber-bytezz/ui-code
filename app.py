import streamlit as st
import pathlib
from PIL import Image
import google.generativeai as genai

# Configure the API key directly in the script
API_KEY = 'AIzaSyBxFW_BlYYlTcMvw4IH6_SB08d-T_0uSHw'
genai.configure(api_key=API_KEY)

# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# Model name
MODEL_NAME = "gemini-1.5-pro-latest"

# Sidebar for framework selection
st.sidebar.title("Settings")
framework = st.sidebar.selectbox("Select Framework", ["Regular CSS", "Bootstrap"])

# Create the model
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Start a chat session
chat_session = model.start_chat(history=[])

# Function to send a message to the model
def send_message_to_model(message, image_path):
    image_input = {
        'mime_type': 'image/jpeg',
        'data': pathlib.Path(image_path).read_bytes()
    }
    response = chat_session.send_message([message, image_input])
    return response.text

# Streamlit app
def main():
    st.markdown(
        """
        <style>
        .title {
            font-size: 3em;
            font-weight: bold;
            animation: fadeIn 2s;
        }
        .subheader {
            font-size: 1.5em;
            color: #555;
            font-size: 1.2em;
            background: linear-gradient(270deg, #ff007a, #ffcc00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 400% 400%;
            animation: gradient 3s ease infinite;
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .progress-bar {
            height: 30px;
            width: 0;
            background-color: #4CAF50;
            animation: loadProgress 5s forwards;
        }
        @keyframes loadProgress {
            0% { width: 0; }
            100% { width: 100%; }
        }
        .loading-message span {
            font-size: 1.2em;
            background: linear-gradient(270deg, #ff007a, #ffcc00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 400% 400%;
            animation: gradient 3s ease infinite;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="title">Magic UI Transformer✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheader">Crafted with 💡 by <a href="https://www.linkedin.com/in/-aro-barath-chandru--12725622a/?originalSubdomain=in">Aro</a></div>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            # Load and display the image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)

            # Convert image to RGB mode if it has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Save the uploaded image temporarily
            temp_image_path = pathlib.Path("temp_image.jpg")
            image.save(temp_image_path, format="JPEG")

            # Progress bar
            st.markdown('<div class="progress-bar" id="progress-bar"></div>', unsafe_allow_html=True)

            # Generate UI description
            if st.button("Transform to Code"):
                st.markdown('<div class="loading-message"><span>🧑‍💻 Looking at your UI...</span></div>', unsafe_allow_html=True)
                prompt = "Describe this UI in accurate details. When you reference a UI element put its name and bounding box in the format: [object name (y_min, x_min, y_max, x_max)]. Also Describe the color of the elements."
                description = send_message_to_model(prompt, temp_image_path)
                st.write(description)
                st.markdown('<script>document.getElementById("progress-bar").style.width = "33%";</script>', unsafe_allow_html=True)

                # Refine the description
                st.markdown('<div class="loading-message"><span>🔍 Refining description with visual comparison...</span></div>', unsafe_allow_html=True)
                refine_prompt = f"Compare the described UI elements with the provided image and identify any missing elements or inaccuracies. Also Describe the color of the elements. Provide a refined and accurate description of the UI elements based on this comparison. Here is the initial description: {description}"
                refined_description = send_message_to_model(refine_prompt, temp_image_path)
                st.write(refined_description)
                st.markdown('<script>document.getElementById("progress-bar").style.width = "66%";</script>', unsafe_allow_html=True)

                # Generate HTML
                st.markdown('<div class="loading-message"><span>🛠️ Generating website...</span></div>', unsafe_allow_html=True)
                html_prompt = f"Create an HTML file based on the following UI description, using the UI elements described in the previous response. Include {framework} CSS within the HTML file to style the elements. Make sure the colors used are the same as the original UI. The UI needs to be responsive and mobile-first, matching the original UI as closely as possible. Do not include any explanations or comments. Avoid using ```html. and ``` at the end. ONLY return the HTML code with inline CSS. Here is the refined description: {refined_description}"
                initial_html = send_message_to_model(html_prompt, temp_image_path)
                st.code(initial_html, language='html')
                st.markdown('<script>document.getElementById("progress-bar").style.width = "90%";</script>', unsafe_allow_html=True)

                # Refine HTML
                st.markdown('<div class="loading-message"><span>🔧 Refining website...</span></div>', unsafe_allow_html=True)
                refine_html_prompt = f"Validate the following HTML code based on the UI description and image and provide a refined version of the HTML code with {framework} CSS that improves accuracy, responsiveness, and adherence to the original design. ONLY return the refined HTML code with inline CSS. Avoid using ```html. and ``` at the end. Here is the initial HTML: {initial_html}"
                refined_html = send_message_to_model(refine_html_prompt, temp_image_path)
                st.code(refined_html, language='html')
                st.markdown('<script>document.getElementById("progress-bar").style.width = "100%";</script>', unsafe_allow_html=True)

                # Save the refined HTML to a file
                with open("index.html", "w") as file:
                    file.write(refined_html)
                st.success("HTML file 'index.html' has been created.")
                st.balloons()

                # Provide download link for HTML
                st.download_button(label="Download HTML", data=refined_html, file_name="index.html", mime="text/html")

                # Feedback form
                with st.form(key='feedback_form'):
                    st.markdown("### 📝 Feedback Form")
                    name = st.text_input("Your Name")
                    rating = st.slider("How would you rate this app?", 1, 5)
                    comments = st.text_area("Any comments or suggestions?")
                    submit_button = st.form_submit_button(label='Submit')
                
                if submit_button:
                    st.success("Thank you for your feedback!")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
