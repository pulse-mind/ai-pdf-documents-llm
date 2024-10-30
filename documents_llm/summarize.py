from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain_anthropic import ChatAnthropic
from langchain_core.documents.base import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from langchain_openai import ChatOpenAI
from rich.console import Console

console = Console()


def summarize_document(
    docs: list[Document],
    model_name: str,
    openai_api_key: str,
    base_url: str,
    temperature: float = 0.1,
    ai_provider: str = None,
    print_details: bool = False,
) -> str:
    pass

    if ai_provider and ai_provider == "MISTRAL_AI":
        if print_details:
            console.print(f"AI Provider: {ai_provider}")
        llm = ChatMistralAI(
            temperature=temperature,
            model_name=model_name,
            api_key=openai_api_key,
        )
    elif ai_provider and ai_provider == "ANTHROPIC_AI":
        if print_details:
            console.print(f"AI Provider: {ai_provider}")
        llm = ChatAnthropic(
            temperature=temperature,
            model_name=model_name,
            api_key=openai_api_key,
        )
    elif ai_provider and ai_provider == "GOOGLE_AI":
        if print_details:
            console.print(f"AI Provider: {ai_provider}")
        llm = ChatGoogleGenerativeAI(
            temperature=temperature,
            model_name=model_name,
            model=model_name,
            google_api_key=openai_api_key,
        )
    else:
        if print_details:
            console.print(f"AI Provider: {"ChatOpenAI"}")
        # Define LLM chain
        llm = ChatOpenAI(
            temperature=temperature,
            model_name=model_name,
            api_key=openai_api_key,
            base_url=base_url,
        )

    prompt_template_en = """Write a summary in 5 lines maximum of the following document. 
    Only include information that is part of the document. 
    Do not include your own opinion or analysis.

    Document:
    "{document}"
    Summary:"""

    prompt_template_fr = """Rédige en Français un résumé en 5 lignes maximum du document suivant. 
        Inclus seulement des informations provenant de ce document. 
        N'incluez pas votre propre opinion ou analyse.

        Document:
        "{document}"
        Résumé:"""
    prompt = PromptTemplate.from_template(prompt_template_fr)

    llm_chain = prompt | llm | StrOutputParser()

    try:
        result = llm_chain.invoke(docs)
        return result
    except Exception as e:
        return f"Exception using {model_name}: {e.message}"



