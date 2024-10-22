# documents-llm

Sample cripts to summarize and query documents using LLMs.

THIS IS NOT ROBUST OR PRODUCTION-READY! FOR DEMONSTRATION PURPOSES ONLY!

## References

This is the sample code for the following video and blog post:

- [Summarize and Query PDFs with a Private Local GPT for Free using Ollama and Langchain (YouTube)](https://youtu.be/Tnu_ykn1HmI)
- [Summarize and Query PDFs with AI using Ollama](https://vincent.codes.finance/posts/documents-llm/)

## Setup

### Dependencies

All you have to do is install the dependencies in `pyproject.toml`:

Using poetry, that would be:

```bash
poetry install
```

Using pip, that would be (It is better to activate your virtual env before):
```bash
pip install -r requirements.txt
```

and setup your environment variables. The recommended way is to use a `.env` file. Just copy
and rename one of `.env-ollama` or `.env-openai` to `.env`. If you use
OpenAI, you will need to also set your API key in `.env`

If you want to use Mistral AI, check `.env-mistralai`, copy or rename or symlink into  `.env`. Set your API key.


## Streamlit App Usage

```bash
streamlit run doc_app.py
```

## CLI Usage

There are two scripts, one for summarizing and one for querying documents.

### Summary

To summarize `document.pdf` from the first page, excluding the last two, using mixtral with a temperature of 0.2:

```bash
python summarize.py document.pdf -s 0 -e "-2" -m mixtral -t 0.2
```

### Query

To query `document.pdf` from the first page, excluding the last two, using mixtral with a temperature of 0.2:

```bash
python query.py document.pdf "What is the data used in this paper?" -s 0 -e "-2" -m mixtral -t 0.2
```