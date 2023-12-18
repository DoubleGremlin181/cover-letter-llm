import streamlit as st
from utils.utils import *
from prompts import cover_letter_prompts
import pyperclip
from dotenv import load_dotenv
load_dotenv()


def main():
    if 'cover_letter' not in st.session_state:
        st.session_state.cover_letter = None

    st.title("Cover Letter Generator")

    # Upload Resume
    st.header("1. Upload Resume")
    resume_file = st.file_uploader("Choose a file or drag and drop", type=["pdf"])
    resume_text = None
    if resume_file is not None:
        resume_text = parse_resume(resume_file)

    # Input Job Listing
    st.header("2. Input Job Listing")
    job_listing_type = st.radio("Select input type", ("URL", "Text"))
    job_listing_text = st.session_state.job_listing_text if "job_listing_text" in st.session_state else None
    if job_listing_type == "URL":
        job_listing_url = st.text_input("Enter job listing URL", "")
        if st.button("Fetch Job Listing"):
            job_listing_text = parse_job_listing(job_listing_url)
            st.session_state.job_listing_text = job_listing_text
    elif job_listing_type == "Text":
        job_listing_text = st.text_area("Enter job listing text", "")

    # Select Cover Letter Style
    st.header("3. Select Cover Letter Style")
    cover_letter_style = st.radio("Select style", ("Classic", "Modern"))

    # Generate Cover Letter
    st.header("4. Generate Cover Letter")
    if st.button("Generate Cover Letter"):
        if resume_text is not None and job_listing_text is not None:
            prompt_template = cover_letter_prompts.prompt_template_classic if cover_letter_style == "Classic" else cover_letter_prompts.prompt_template_modern
            cover_letter = generate_cover_letter(resume_text, job_listing_text, prompt_template)
            st.subheader("Cover Letter:")
            st.markdown(cover_letter)
            st.session_state.cover_letter = cover_letter
        else:
            st.warning("Please upload a resume and provide a job listing.")

    # Output Cover Letter
    if st.session_state.cover_letter is not None:
        if st.button("Copy to Clipboard"):
            pyperclip.copy(st.session_state.cover_letter)
            st.success("Cover letter copied to clipboard!")


if __name__ == "__main__":
    main()
