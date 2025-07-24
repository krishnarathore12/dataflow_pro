from dotenv import load_dotenv
import os

import streamlit as st

from browser_use.llm import ChatOpenAI
from browser_use.browser.profile import BrowserProfile
from browser_use.browser.session import BrowserSession
from browser_use.llm import ChatGoogle
from browser_use import Agent
from browser_use import Controller, ActionResult
import asyncio

load_dotenv()
controller = Controller()

@controller.action('Search the database for related workflow on the basis query made by the user')
async def search_db(query: str) -> ActionResult:
    try:
        import pandas as pd
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np

        df = pd.read_csv('data.csv')

        model = SentenceTransformer('all-MiniLM-L6-v2')

        df['combined_text'] = df['title'].fillna('') + ' ' + df['description'].fillna('') + ' ' + df['code'].fillna('')

        db_embeddings = model.encode(df['combined_text'].tolist())

        query_embedding = model.encode([query])

        similarities = cosine_similarity(query_embedding, db_embeddings)[0]

        most_similar_idx = np.argmax(similarities)
        max_similarity = similarities[most_similar_idx]

        threshold = 0.3

        if max_similarity > threshold:
            most_similar_record = df.iloc[most_similar_idx]
            answer = f"Found similar request (similarity: {max_similarity:.2f}):\n"
            answer += f"Title: {most_similar_record['title']}\n"
            answer += f"Description: {most_similar_record['description']}\n"
            answer += f"Code: {most_similar_record['code']}"
        else:
            answer = "No sufficiently similar requests found in the database."

    except FileNotFoundError:
        answer = "Database file 'data.csv' not found."
    except Exception as e:
        answer = f"Error searching database: {str(e)}"

    return ActionResult(extracted_content=f'The most similar workflow found: {answer}', include_in_memory=True)

# llm = ChatOpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=os.getenv("OPENROUTER_API_KEY"),
#   model= os.getenv("OPENROUTER_MODEL_NAME"),
# )

def get_llm():
    llm = ChatGoogle(model='gemini-2.5-pro')
    return llm


def initialize_agent(query: str, control):
	llm = get_llm()
	controller = control
	browser_session = BrowserSession()

	return Agent(
		task=query,
		llm=llm,
		controller=controller,
		browser_session=browser_session,
		use_vision=True,
		max_actions_per_step=1,
	), browser_session

# Streamlit UI
st.title('PP :<>')

query = st.text_input('Enter your query:', 'go to reddit and search for posts about browser-use')

if st.button('Run Agent'):

	agent, browser_session = initialize_agent(query, controller)
	async def run_agent():
		with st.spinner('Running automation...'):
			result = await agent.run(max_steps=25)
		st.success('Task completed! 🎉')

	asyncio.run(run_agent())


	st.button('Close Browser', on_click=lambda: asyncio.run(browser_session.close()))
