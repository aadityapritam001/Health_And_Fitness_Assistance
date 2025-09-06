from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate,PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_models import *
import streamlit as st


# Prompt template
def prompt_template():
    PROMPT_TEMPLATE = """
    You are a certified fitness and health assistant.

    Your job is to give personalized, accurate, and practical advice to users based on their profile and query.

    User Profile:
    - Name: {name}
    - Age: {age}
    - Weight: {weight}
    - Height: {height}
    - Gender: {gender}
    - Fitness Goal: {goal} (e.g., lose weight, build muscle, stay fit)
    - Dietary Preferences: {diet} (e.g., vegetarian, keto, none)

    User Question:
    {question}

    Instructions:
    - Give concise but detailed answers
    - Include health-based reasoning (e.g., caloric needs, macros)
    - Warn if question is unsafe or medical advice is needed
    - Output should be structured: Advice + Rationale + Suggested Action

    Respond in a friendly, supportive tone.
    """
    return PROMPT_TEMPLATE


prompt = ChatPromptTemplate.from_template(prompt_template())

# ---- Streamlit UI ----
st.set_page_config(page_title="Health & Fitness Assistant", layout="centered")
st.title("🏋️‍♀️ Health & Fitness Assistant")

st.markdown("Ask health-related questions and get personalized responses!")

with st.form("user_form"):
    st.subheader("👤 Your Profile")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100, value=25)
    weight = st.text_input("Weight (e.g., 70kg)")
    height = st.text_input("Height (e.g., 170cm)")
    gender = st.selectbox("Gender", ["male", "female", "other"])
    goal = st.selectbox("Fitness Goal", ["lose weight", "build muscle", "stay fit", "gain weight"])
    diet = st.selectbox("Dietary Preference", ["none", "vegetarian", "vegan", "keto", "paleo"])

    st.subheader("🧠 LLM Model Selection")
    llm_choice = st.selectbox("Choose an LLM to generate the response", ["OpenAI", "Groq", "HuggingFace"])

    st.subheader("💬 Your Question")
    question = st.text_area("Ask a question", placeholder="e.g., What should I eat for dinner to build muscle?")

    submitted = st.form_submit_button("Get Advice")


# ---- Handle Submission ----
if submitted and question.strip():
    with st.spinner("Thinking..."):
        # Choose the correct LLM object
        if llm_choice == "OpenAI":
            llm = openai_llm()  # should be a LangChain-compatible LLM instance
        elif llm_choice == "Groq":
            llm = groq_llm()
        elif llm_choice == "HuggingFace":
            llm = huggingface_llm()
        else:
            st.error("❌ Unknown model selected.")
            st.stop()

        # Set up the full chain
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        # Run the chain
        output = chain.invoke({
            "name": name,
            "age": age,
            "weight": weight,
            "height": height,
            "gender": gender,
            "goal": goal,
            "diet": diet,
            "question": question
        })

        st.success("✅ Here's your personalized advice:")
        st.markdown(output)
