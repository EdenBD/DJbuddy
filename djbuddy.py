# Refactored from https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/mrkl_demo.py
from pathlib import Path

import streamlit as st

from langchain import OpenAI, LLMChain
from langchain.agents import initialize_agent, Tool, AgentType, load_tools
from langchain.callbacks import StreamlitCallbackHandler

# TODO: switch TODO to "illenium.pickle" files
SAVED_SESSIONS = {
    "Which songs can I mix after the track 'We don't talk anymore'?": "TODO",
    "Which songs can I mix after 'Crawl outta Love' according to Illenium pervious mixes?": "TODO",
}

# Configure page outlook
st.set_page_config(
    page_title="DJ Buddy",
    page_icon=":musical_keyboard:",
    layout="wide",
    initial_sidebar_state="expanded",  # "collapsed"
)

"# DJ With Inspiration [WIP]"

# Setup user's OpenAI key
with st.sidebar:
    st.title("Settings")
    openai_api_key = "not_supplied"
    enable_custom = False
    user_openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="Set this to run your own custom questions.",
    )
    if not (user_openai_api_key.startswith("sk-") and len(user_openai_api_key) == 51):
        st.warning("Please enter your credentials!", icon="⚠️")
    else:
        openai_api_key = user_openai_api_key
        enable_custom = True
        st.success("Proceed to entering your custom message!", icon="👉")


##### Langchain #####

# Initialize tools
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, streaming=True)
tools = load_tools(["llm-math"], llm=llm)

# prompt
prefix = """Answer the following questions first using the tools, then your DJing and music knowledge. You have access to the following tools:"""
suffix = """Begin! When given a track to mix, remember to consider the user's track bpm and key."

Question: {input}
{agent_scratchpad}"""

# Initialize agent
buddy = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"prefix": prefix, "suffix": suffix},
)

# User form to submit a question
with st.form(key="form"):
    st.write(
        f"Ask one of the sample questions, or {'enter your API Key in the sidebar to' if not enable_custom else ''} submit your own question."
    )

    selected = st.selectbox("Sample questions", sorted(SAVED_SESSIONS.keys())) or ""
    user_input = st.text_input("Custom question") if enable_custom else selected
    submit_clicked = st.form_submit_button("Submit Question")

# Output populated once question submitted
output_container = st.empty()
if submit_clicked:
    output_container = output_container.container()
    output_container.chat_message("user").write(user_input)
    answer_container = output_container.chat_message("buddy", avatar="🦜")
    # To display agent's actions
    st_callback = StreamlitCallbackHandler(answer_container)

    # If we've saved this question, play it back instead of actually running LangChain
    if user_input in SAVED_SESSIONS:
        session_name = SAVED_SESSIONS[user_input]
        session_path = Path(__file__).parent / "runs" / session_name
        print(f"Playing saved session: {session_path}")
        # TODO
        # answer = playback_callbacks([st_callback], str(session_path), max_pause_time=2)
        answer = ""
    else:
        answer = buddy.run(user_input, callbacks=[st_callback])

    answer_container.write(answer)
