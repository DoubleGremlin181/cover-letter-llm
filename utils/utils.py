from langchain_community.document_loaders import AsyncChromiumLoader
from pypdf import PdfReader
from langchain_community.document_transformers import Html2TextTransformer
from agents.gpt_35_turbo import get_agent
from prompts import job_listing_prompt


def parse_resume(path):
    loader = PdfReader(path)
    text = loader.pages[0].extract_text()
    return text


def parse_job_listing(url):
    # Load HTML
    loader = AsyncChromiumLoader([url])
    html = loader.load()
    # Extract text from HTML
    html2text = Html2TextTransformer()
    raw_text = html2text.transform_documents(html)[0].page_content
    # Find relevant text
    agent = get_agent(temperature=1.0)
    prompt_template = job_listing_prompt.prompt_template.format(raw_text=raw_text)
    resp = agent.invoke(prompt_template.format(raw_text=raw_text))
    text = resp.content
    return text


def generate_cover_letter(resume_text, job_listing_text, prompt_template):
    agent = get_agent()
    resp = agent.invoke(prompt_template.format(resume=resume_text, job_listing=job_listing_text))
    text = resp.content
    return text