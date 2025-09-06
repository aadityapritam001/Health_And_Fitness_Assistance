from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser,JsonOutputParser
from dotenv import load_dotenv

import os 

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# langsmith tracking
os.environ["LANGCHAIN_TRACKING_V1"] = "true"


###### OpenAI LLM ######
def openai_llm():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    return llm


###### Groq LLM ######
def groq_llm():
    # Initialize Groq LLM
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )
    return llm

###### HuggingFace LLM ######
def huggingface_llm():
    llm = HuggingFaceEndpoint(
        repo_id="deepseek-ai/DeepSeek-R1-0528",
        task="text-generation",
        max_new_tokens=512,
        do_sample=False,
        repetition_penalty=1.03,
        provider="auto",  # let Hugging Face choose the best provider for you
    )
    chat_model = ChatHuggingFace(llm=llm)
    return chat_model

