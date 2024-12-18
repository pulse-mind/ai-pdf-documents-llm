import argparse
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console

from documents_llm.document import load_pdf, load_text
from documents_llm.query import query_document

start = time.time()

# Load environment variables
load_dotenv()

# Initialize rich console
console = Console()

# Load model parameters
MODEL_NAME = os.getenv("MODEL_NAME")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_URL = os.getenv("OPENAI_URL")
AI_PROVIDER = os.getenv("AI_PROVIDER")

# Initialize argument parser
parser = argparse.ArgumentParser(description="Query a document.")
parser.add_argument("file", type=str, help="The file to query.")
parser.add_argument("user_query", type=str, help="User query about the document.")
parser.add_argument(
    "-s", "--start", type=int, default=0, help="The start page for PDF files."
)
parser.add_argument(
    "-e", "--end", type=int, default=-1, help="The end page for PDF files."
)
parser.add_argument("-t", "--temp", type=float, default=0.1, help="Temperature.")
parser.add_argument("-m", "--model", type=str, help="Model name.", default=MODEL_NAME)
parser.add_argument("-o", "--output", type=str, help="The output file.")
args = parser.parse_args()

# Load document
file_path = Path(args.file)
console.print(f"Loading document: [blue]{file_path}[/blue]")
if file_path.suffix == ".pdf":
    docs = load_pdf(file_path, args.start, args.end)
elif file_path.suffix == ".txt":
    docs = load_text(file_path)
else:
    console.print(f"Unsupported file type: {file_path.suffix}", style="bold red")
    exit(1)

user_query = args.user_query
console.print(f"[bold blue]User query:[/]{user_query}")
# Summarize document
console.print("[bold blue]Querying the document...[/]")
answer = query_document(
    docs,
    user_query=user_query,
    model_name=args.model,
    openai_api_key=OPENAI_API_KEY,
    base_url=OPENAI_URL,
    temperature=args.temp,
    ai_provider=AI_PROVIDER,
    )
console.print(f"Completed in : {time.time() - start:.2f} seconds\n")

console.print("Summary:", style="bold green")

console.print(answer)

# Output summary
if args.output:
    with open(args.output, "w") as f:
        f.write(answer)
