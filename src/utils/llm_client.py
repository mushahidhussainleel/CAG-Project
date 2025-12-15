from google import genai
from google.genai import types
import os
from dotenv import load_dotenv , find_dotenv 

# load the environament  variable
load_dotenv(find_dotenv())

def get_llm_response(context:str , query:str)->dict:
    """
    Send a user query and context to Google Gemini and return the assistant's response.

    Args:
        Context (str): Background information delimited by triple backticks.
        query (str): The user's question to be answered based on the context.

    Returns:
        str: The assistant's generated text response

    Raises:
        ValueError: If the GEMINI_API_KEY environment variable is not set.

    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set. "
            "Please set it to your Google Gemini API key (get key from  https://aistudio.google.com )"
        )
    # Intialize the GenAI client
    
    client = genai.Client(api_key=api_key)
    model = "gemini-2.5-flash"
    contents = [
        types.Content(
            role = "user",
            parts = [types.Part.from_text(text=query)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction= [
            types.Part.from_text(
                text=(
                    "You are a helpful assistant that can answer questions based on the provided context delimited "
                    "with triple backticks.\n\n"
                    "You will be given a context and a user query. Your task is to generate a response that is "
                    "relevant to the query based on the context provided. If the context does not contain enough "
                    "information to answer the query, you should indicate that you do not have enough information "
                    "to provide a complete answer.\n\n"
                    "If the context is empty, you should respond with a message indicating that you do not have "
                    "enough information to answer the query.\n\n"
                    "You should always respond in a friendly and helpful manner. You should not include any "
                    "personal opinions or information.\n\n"
                    f"Context:\n```{context}```"
                )
            ),
        ],
    )

    response =  client.models.generate_content(
        model= model,
        contents = contents,
        config = generate_content_config
    )
    response_text = response.text  # Correct attribute
    tokens_used = response.usage_metadata.total_token_count if hasattr(response, 'usage_metadata') else 0

    return {
        "text": response_text,
        "tokens_used": tokens_used,
    }