# To run in local
# clear && python3.11 -m pip install -qU -r requirements.txt && streamlit run app.py

# Import required libraries
import streamlit as st  # for creating the web app
from dotenv import load_dotenv  # for loading API key from .env file
import os
import google.generativeai as genai  # Google's AI model
from PIL import Image  # for handling images

# Load the API key from .env file
load_dotenv()
genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])

# Function to get AI response about the food image
def get_gemini_response(image, prompt):
    """Send image to Google's AI and get calorie information"""
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to prepare the uploaded image for AI processing
def prepare_image(uploaded_file):
    """Convert uploaded image to format required by Google's AI"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    return None

# Main web app
def main():
    # Page configuration
    st.set_page_config(
        page_title="Calorie Advisor",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Header section with full-width background
    st.markdown("""
        <div style='background-color: #161922; padding: 2rem 0; margin: -6rem -4rem 2rem -4rem;'>
            <div style='text-align: center; max-width: 1200px; margin: 0 auto;'>
                <h1 style='color: #fafafa; margin-bottom: 1rem; margin-top: 1rem;'>🍽️ Calorie Advisor AI</h1>
                <p style='color: #a8e6cf; font-size: 1.2rem;'>Get instant calorie information and health advice for your meals!</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Create two columns for layout
    col1, col2 = st.columns([1, 1], gap="large")

    # Left column - Upload section
    with col1:
        st.markdown("### 📸 Upload Your Food Image")
        st.markdown("Take a photo or upload an existing image of your meal")
        
        # Create file uploader with supported formats
        uploaded_file = st.file_uploader(
            "Supported formats: JPG, JPEG, PNG",
            type=["jpg", "jpeg", "png"],
            help="Make sure the image is clear and well-lit for best results"
        )

    # Right column - Display and Analysis section
    with col2:
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Your Meal", use_container_width=True)

            # Create analyze button
            analyze_button = st.button(
                "🔍 Analyze Meal",
                help="Click to get detailed calorie information",
                type="primary",
                use_container_width=True
            )

            # Process image when button is clicked
            if analyze_button:
                with st.spinner("🤖 AI is analyzing your meal..."):
                    # Prepare prompt for AI analysis
                    prompt = """
                    Please analyze this food image and provide:
                    1. List each food item and its calories
                    2. Total calories
                    3. Simple health advice

                    Format like this:
                    🍽️ FOOD ITEMS:
                    • [Food Item] - [Calories]
                    • [Food Item] - [Calories]

                    📊 TOTAL CALORIES: [Number]

                    💡 HEALTH TIPS:
                    • [Tip 1]
                    • [Tip 2]
                    """

                    # Get and display AI response
                    image_data = prepare_image(uploaded_file)
                    if image_data is not None:
                        response = get_gemini_response(image_data, prompt)
                        st.success("✨ Analysis Complete!")
                        
                        # Display formatted results
                        st.markdown("""
                            <div style='padding: 1.5rem; border-radius: 8px; margin-top: 1rem;'>
                            {}
                            </div>
                        """.format(response.replace('\n', '<br>').replace('•', '◆')), unsafe_allow_html=True)
        else:
            # Show placeholder when no image is uploaded
            st.markdown("""
                <div style='text-align: center; padding: 2rem;'>
                    <h3>Ready to analyze your meal?</h3>
                    <p>Upload a photo to get started!</p>
                </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style='text-align: center; padding: 2rem; margin-top: 3rem;'>
            <p>Powered by AI • Made with ❤️ for healthy eating</p>
        </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
