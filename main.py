import streamlit as st
from gpt4all import GPT4All
import PyPDF2
from prompts import explanation_prompt, code_generation_prompt, debug_prompt

# Load the GPT4All model
@st.cache_resource
def load_model():
    return GPT4All(model_name="mistral-7b-openorca.Q4_0.gguf")  # Update path if needed

model = load_model()

st.title("🧠 AI Python Learning Assistant (with Doc Reading & Memory)")

# File uploader for txt or pdf
uploaded_file = st.file_uploader("Upload a document (txt or pdf)", type=["txt", "pdf"])

doc_text = ""
if uploaded_file:
    if uploaded_file.type == "text/plain":
        doc_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        pages = [page.extract_text() for page in reader.pages]
        doc_text = "\n".join(pages)
    st.markdown("**Document preview:**")
    st.write(doc_text[:1000])  # preview first 1000 characters

# Initialize memory in session state
if "history" not in st.session_state:
    st.session_state.history = []

def add_to_memory(user_query, assistant_response):
    st.session_state.history.append({"user": user_query, "assistant": assistant_response})

def get_memory_text():
    # Get last 3 interactions for context
    history = st.session_state.history[-3:]
    memory_text = ""
    for turn in history:
        memory_text += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n\n"
    return memory_text

# UI Inputs
mode = st.selectbox("Choose mode:", ["Explain Concept", "Generate Code", "Debug Code"])
user_input = st.text_area("Enter your Python topic, task, or code:")

if st.button("Submit") and user_input.strip():
    memory_text = get_memory_text()

    # Build prompt with memory and doc context
    if mode == "Explain Concept":
        prompt = explanation_prompt(user_input, memory=memory_text, doc=doc_text)
    elif mode == "Generate Code":
        prompt = code_generation_prompt(user_input, memory=memory_text, doc=doc_text)
    elif mode == "Debug Code":
        prompt = debug_prompt(user_input, memory=memory_text, doc=doc_text)

    with st.spinner("Thinking..."):
        with model.chat_session():
            response = model.generate(prompt)

    st.markdown("### 💡 Response")
    st.code(response, language='python')

    # Save interaction to memory
    add_to_memory(user_input, response)
