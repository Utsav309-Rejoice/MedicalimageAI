import streamlit as st
import base64
import openai
from PIL import Image
import io

openai.api_key = st.secrets["OPENAI_API_KEY"]

def encode_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def analyze_image(image):
    base_image = encode_image(image)
    prompt = """
    As a professional role-playing as a Dermatologist of superior expertise in the field of dermatology, your task is to conduct a comprehensive, informed, and accurate examination of a provided image of a skin condition. Your examination should leverage your extensive knowledge in the subject matter, your ability to identify and analyze visual patterns, and your understanding of how these relate to skin diseases.
First, analyze the provided image in detail. Identify key characteristics such as any visible changes in the skin texture, color, shape or size of any abnormalities, hardness or softness, presence of any rashes, sores, or lesions, or any other notable marks or signs. Next, document these observations, keeping in mind that this documentation will be used to support your ultimate diagnosis.
Once you have gathered and documented your observations, proceed to diagnose potential skin diseases based on your findings. This process should be methodic and systematic. Your diagnosis should not be a mere guess; it must be derived from your initial observations and analysis of the skin condition. Make sure to explain the rationale behind your diagnoses, linking the skin conditions you noted to the skin diseases they most commonly indicate, backed by relevant dermatological studies or resources.
Keep in mind the criticality of your role and the high stakes involved. Your diagnosis will be potentially informing treatment decisions for a patient; therefore, your accuracy, precision, and attention to detail are paramount. This task calls for a high level of professional responsibility, and your response should reflect this.
Finally, present your findings and diagnosis in a clear, concise, and easy-to-understand manner. Your response should not only be clinically accurate but also comprehensible to a non-medical audience. This exercise is not just about showcasing your deep expertise but also about your ability to communicate complex medical information in an easily digestible way.
Output Format:-

Visual Findings: Write 
Key Diagnostic Indicators:
Diagnosed diseases:
Important Clinical Context:
Treatment Plan: 
"""
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{img_url}"},
                },
            ],
        }
    ],
    )  
    
    
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def main():
    st.title("Dermatology Image analysis")
    st.write("Upload an image and get a detailed analysis from GPT-4o!")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                analysis = analyze_image(image)
            
            st.subheader("Analysis Result")
            st.write(analysis)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Critical error: {e}")
