import streamlit as st
import base64
import openai
from PIL import Image
import io
from anthropic import Anthropic
openai.api_key = st.secrets["OPENAI_API_KEY"]
anthropic_client = Anthropic(api_key=st.secrets["ANTHROPIC_KEYS"])

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def claude_question(image_path,medical_history,symptoms):
    prompt = f"""As a professional role-playing as a Dermatologist of superior expertise in the field of dermatology, your task is to conduct a comprehensive, informed, and accurate examination of a provided image of a skin condition. Your examination will be meticulously informed by the patient's specific disease symptoms (if provided) and comprehensive medical history (if Provided), providing critical contextual depth to your analysis.
Patient Medical History: {{medical_history}}
Patient-Reported Disease Symptoms: {{disease_symptoms}}
Detailed Examination Protocol:
1. Visual Image Analysis:
First, analyze the provided image in detail. Identify key characteristics with surgical precision:
- Skin Texture: Assess smoothness, roughness, scaling, or any unusual surface variations
- Color Variations: Document exact color changes, noting:
  * Specific hues (reddish, brownish, bluish, etc.)
  * Color uniformity or irregularity
  * Potential pigmentation changes
- Morphological Characteristics:
  * Shape of lesions or abnormalities
  * Precise measurements
  * Border definition (clear-cut, blurred, irregular)
- Structural Observations:
  * Elevation or depression of affected areas
  * Presence of nodules, plaques, or unique formations
  * Symmetry or asymmetry of skin changes
- Surface Quality:
  * Presence of scales, crusts, or erosions
  * Shine or dullness
  * Evidence of bleeding or weeping
- Peripheral Findings:
  * Spread pattern of skin condition
  * Relationship to surrounding healthy tissue
2. Comprehensive Context Integration:
Systematically cross-reference visual observations with:
- Detailed Medical History
  * Previous skin conditions
  * Chronic illnesses
  * Genetic predispositions
  * Medication history
  * Allergies
  * Immune system status
- Patient-Reported Symptoms
  * Onset and progression of current condition
  * Associated pain or discomfort
  * Itching, burning, or other sensory experiences
  * Factors that exacerbate or alleviate symptoms
  * Duration of current skin manifestation
3. Diagnostic Methodology:
- Employ a systematic, evidence-based approach to diagnosis
- Utilize pattern recognition from extensive dermatological knowledge
- Consider differential diagnoses
- Link observed characteristics to potential skin diseases
- Evaluate probability of each potential diagnosis
- Identify distinguishing features that support or rule out specific conditions
4. Diagnostic Reasoning:
Your diagnosis must be:
- Methodically derived from observational evidence
- Supported by clinical reasoning
- Backed by dermatological research and established medical knowledge
- Considerate of the unique patient context
Output Format:
Visual Findings: [Detailed description of observed skin characteristics]
Key Diagnostic Indicators: [Specific signs pointing to potential conditions]
Contextual Insights from Medical History: [How history influences diagnostic consideration]
Correlation of Symptoms with Visual Findings: [Detailed analysis of symptom-image relationships]
Diagnosed Diseases: [Potential conditions with probability assessment]
Treatment Plan: [Recommended approach, potential interventions]
Critical Guidance:
- Ensure unparalleled accuracy and precision
- Communicate complex medical information with clarity
- Provide insights that could potentially guide comprehensive patient care
Remember your responses will be used by professional dermatologists for RESEARCH purposes. They will NOT be used directly for patient treatment.
"""
    base_image = encode_image(image_path)
    response = anthropic_client.messages.create(max_tokens=1024,
    messages=[{
              "role": "user",
              "content": [
                {
                  "type": "image",
                  "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base_image
                  }
                },
                { "type": "text", "text":  prompt.format(medical_history=medical_history,disease_symptoms=symptoms)}
              ]
            }],
            model="claude-3-opus-20240229")
    return response.content[0].text

def analyze_image(image_path):
    base64_image = encode_image(image_path)
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
    response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt,
        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)
    
    print(response.choices[0].message.content)
    return response.choices[0].message.content

def main():
    st.title("Dermatology Image analysis")
    st.write("Upload an image and get a detailed analysis!")
    medical_history = st.text_area(
    label="Patient Medical History", 
    placeholder="Enter comprehensive medical history details...",
    height=200
    )

    # Disease Symptoms Text Input
    disease_symptoms = st.text_area(
    label="Patient-Reported Disease Symptoms", 
    placeholder="Describe specific symptoms experienced by the patient...",
    height=200
    )
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = image.convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)
        temp_image_path = "uploaded_image.png"
        image.save(temp_image_path,format="JPEG")
        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                analysis = claude_question(temp_image_path,medical_history,disease_symptoms)
            
            st.subheader("Analysis Result")
            st.write(analysis)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Critical error: {e}")
