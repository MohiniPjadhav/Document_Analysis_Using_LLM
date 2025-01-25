
import streamlit as st
from groq import Groq
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import docx

# Initialize Groq API client
client = Groq(api_key="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")

# Load a pre-trained embedding model from sentence-transformers
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Function to summarize text using sentence embeddings
def summarize_text(text, max_sentences=3):
    sentences = text.split(". ")  # Split text into sentences
    sentence_embeddings = embedding_model.encode(sentences)  # Generate embeddings
    summary = ". ".join(sentences[:max_sentences])  # Select top N sentences
    return summary

# Function to extract insights using Groq API
def extract_insights(text):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts insights from text."},
            {"role": "user", "content": f"Extract key insights from the following text:\n{text}"}
        ]
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Document Analysis using LLM")
st.write("Upload a document to extract insights, summarize content, and interpret contextual information.")

# File upload
uploaded_file = st.file_uploader("Upload a document (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    # Extract text based on file type
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        text = extract_text_from_docx(uploaded_file)
    else:
        st.error("Unsupported file type. Please upload a PDF or DOCX file.")
        st.stop()

    st.subheader("Extracted Text")
    st.text_area("Text", text, height=300)

    # Analysis options
    st.subheader("Analysis Options")
    col1, col2= st.columns(2)
    with col1:
        summarize = st.button("Summarize Content")
    with col2:
        extract = st.button("Extract Insights")


    # Perform analysis based on user selection
    if summarize:
        with st.spinner("Summarizing content..."):
            summary = summarize_text(text)
            st.subheader("Summary")
            st.write(summary)

    if extract:
        with st.spinner("Extracting insights..."):
            insights = extract_insights(text)
            st.subheader("Key Insights")
            st.write(insights)
