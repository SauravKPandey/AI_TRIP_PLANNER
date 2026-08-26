import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


class ConfigLoader:
    def __init__(self):
        print(f"Loaded config.....")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq", "gemini"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model.
        """
        load_dotenv()
        print("LLM loading...")
        print(f"Loading model from provider: {self.model_provider}")
        if self.model_provider == "groq":
            print("Loading LLM from Groq..............")
            groq_api_key = os.getenv("GROQ_API_KEY")
            model_name = self.config["llm"]["groq"]["model_name"]
            llm=ChatGroq(model=model_name, api_key=groq_api_key)
        elif self.model_provider == "gemini":
            print("Loading LLM from Gemini..............")
            #gemini_api_key = os.getenv("GEMINI_API_KEY")
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            print(f"gemini api key: {gemini_api_key}")
            if not gemini_api_key:
                raise ValueError("GEMINI_API_KEY environment variable is not set.")
            model_name = self.config["llm"]["gemini"]["model_name"]
            llm = ChatGoogleGenerativeAI(model=model_name, api_key=gemini_api_key)
        
        return llm
    