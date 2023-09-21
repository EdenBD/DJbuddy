from pydantic_settings import BaseSettings
import streamlit as st


class Setting(BaseSettings):
    OPENAI_API_KEY: str = ""


# Get keys from st.secrets instead of .env
settings = Setting(**st.secrets)
