# DJbuddy [In development]

This app aims to help DJs find inspiration from other DJ tracks and data bases. 

## Demo
<!-- TODO -->
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://djbuddy.streamlit.app/)

## Requirements:

You must get an OpenAI API key to usen this app. you can follow [these instructions](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) to get it. 

## Set-up (development)

1. Clone the repo and create a virtual enviroment: 

```
conda create -n djbuddy python=3.11
conda activate djbuddy
pip install -r requirements.txt
```

Optionally, you can also add an Ipython kerenl for Jupyter notebook:
```
python -m ipykernel install --user --name djbuddy --display-name djbuddy
```

2. Create a .streamlit/secrets.toml file and add the following:

```secrets.toml
OPENAI_API_KEY='sk_xxxxxxx'
```

3. Run the app:

```
streamlit run djbuddy.py
```

## Credits:
- This app is refactored from [LangChain](https://www.langchain.com/) [MRKL](https://github.com/langchain-ai/streamlit-agent/blob/main/streamlit_agent/mrkl_demo.py) demo app. 
