import streamlit as st

from langchain_ollama import OllamaLLM

from utils.rag import create_vector_store
from utils.rag import retrieve_context

from utils.ats import calculate_ats_score
from utils.resume_parser import extract_resume_text
from utils.keyword_extractor import extract_keywords


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

if uploaded_file:

    resume_text = extract_resume_text(
        uploaded_file
    )

    with st.expander("View Resume"):
        st.write(resume_text)

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Analyze Resume"):

            llm = OllamaLLM(model="mistral")

            prompt = f"""
            Analyze this resume.

            Resume:
            {resume_text}

            Provide:

            1. Summary
            2. Strengths
            3. Weaknesses
            4. Suggestions
            """

            with st.spinner("Analyzing Resume..."):

                result = llm.invoke(prompt)

            st.subheader("AI Analysis")

            st.write(result)

    with col2:

        if st.button("Match With JD"):

            if not job_description:

                st.warning(
                    "Paste a Job Description first."
                )

            else:

                score, matched, missing = (
                    calculate_ats_score(
                        resume_text,
                        job_description
                    )
                )

                st.subheader("ATS Result")

                st.metric(
                    "ATS Score",
                    f"{score}%"
                )

                st.markdown("### ✅ Matched Keywords")

                if matched:
                    st.write(", ".join(sorted(matched)))
                else:
                    st.write("No matches found")

                st.markdown("### ❌ Missing Keywords")

                if missing:
                    st.write(", ".join(sorted(missing)))
                else:
                    st.write("No missing keywords")

                llm = OllamaLLM(model="mistral")

                prompt = f"""
                Compare this resume with
                the job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Provide:

                1. Match Summary
                2. Strengths
                3. Weaknesses
                4. Improvement Suggestions
                """

                with st.spinner("Generating AI Feedback..."):

                    result = llm.invoke(prompt)

                st.markdown("### 🤖 AI Suggestions")

                st.write(result)

                st.markdown("---")
                st.subheader("💬 Chat With Resume")

                question = st.text_input(
                "Ask a question about your resume"
                )

                if question and uploaded_file:

                 vector_db = create_vector_store(
                 resume_text
                 )

                 context = retrieve_context(
                 vector_db,
                 question
                 )

                llm = OllamaLLM(model="mistral")

                prompt = f"""
                Answer ONLY using the resume context.

                Resume Context:
                {context}

                Question:
                {question}
                """

                with st.spinner("Thinking..."):
                  answer = llm.invoke(prompt)

                st.success(answer)