import streamlit as st
from ai_helper import generate_study_content
from pdf_helper import extract_text_from_pdf


st.set_page_config(
    page_title="StudyMate AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 StudyMate AI")
st.subheader("Your personal AI-powered learning assistant")

st.write(
    "Upload your notes or enter a topic to generate explanations, "
    "summaries, flashcards and quizzes."
)

input_method = st.radio(
    "How would you like to provide your study material?",
    ["Enter text", "Upload PDF"]
)

# Default values
study_text = ""
uploaded_file = None

# Get study material
if input_method == "Enter text":
    study_text = st.text_area(
        "Enter your study topic or notes",
        height=200
    )

else:
    uploaded_file = st.file_uploader(
        "Upload your study notes",
        type=["pdf"]
    )

    if uploaded_file is not None:
        try:
            study_text = extract_text_from_pdf(uploaded_file)

            if study_text:
                st.success("PDF text extracted successfully!")
            else:
                st.error(
                    "No readable text was found. "
                    "The PDF may contain scanned images."
                )

        except Exception as error:
            st.error(f"Unable to read the PDF: {error}")


language = st.selectbox(
    "Select explanation language",
    ["English", "Hindi"]
)

feature = st.selectbox(
    "What would you like StudyMate AI to generate?",
    [
        "Easy Explanation",
        "Summary",
        "Flashcards",
        "Quiz"
    ]
)

# Generate content
if st.button("Generate", type="primary"):

    if input_method == "Enter text" and not study_text.strip():
        st.warning("Please enter a topic or paste your notes.")

    elif input_method == "Upload PDF" and uploaded_file is None:
        st.warning("Please upload a PDF file.")

    elif not study_text.strip():
        st.warning("The uploaded PDF does not contain readable text.")

    else:
        try:
            with st.spinner(
                "StudyMate AI is generating your content..."
            ):
                result = generate_study_content(
                    study_text,
                    feature,
                    language
                )

            st.success("Content generated successfully!")
            st.subheader("Generated Content")
            st.markdown(result)

        except Exception as error:
            st.error(f"Unable to generate content: {error}")