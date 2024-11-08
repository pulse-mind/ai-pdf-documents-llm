import argparse
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from tabulate import tabulate
import requests

from documents_llm.document import load_pdf, load_text
from documents_llm.summarize import summarize_document

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
parser = argparse.ArgumentParser(description="Summarize a document.")
parser.add_argument("file", type=str, help="The file to summarize.")
parser.add_argument(
    "-s", "--start", type=int, default=0, help="The start page for PDF files."
)
parser.add_argument(
    "-e", "--end", type=int, default=-1, help="The end page for PDF files."
)
parser.add_argument("-t", "--temp", type=float, default=0.1, help="Temperature.")
parser.add_argument("-m", "--model", type=str, help="Model name.", default=MODEL_NAME)
parser.add_argument("-l", "--model_list", type=str, help="List of models names.", default=None)
parser.add_argument("-o", "--output", type=str, help="The output file.")
args = parser.parse_args()


# Load document
file_path = Path(args.file)
console.print(f"Loading document: [blue]\"{file_path}\"[/blue]")
if file_path.suffix == ".pdf":
    docs = load_pdf(file_path, args.start, args.end)
elif file_path.suffix == ".txt":
    docs = load_text(file_path)
else:
    console.print(f"Unsupported file type: {file_path.suffix}", style="bold red")
    exit(1)

print_details = True
args_models = []
if args.model_list:
    if args.model_list == "all":
        response = requests.get(OPENAI_URL + '/models')
        response.raise_for_status()
        models_list = response.json()
        for model_def in models_list['data']:
            args_models.append(model_def['id'])
        args_models.sort()
    else:
        args_models = args.model_list.split(',')
    print_details = len(args_models) == 1
else:
    args_models = [args.model]

console.print(f"Models : {args_models}")

results = [["model_name", "Time", "Summary"]]
for model_name in args_models:
    start = time.time()
    model_result = [model_name]
    # Summarize document
    if print_details:
        console.print(f"Summarizing document with [green]{model_name}[/green]...", style="bold blue")
    summary = summarize_document(
        docs,
        model_name=model_name,
        openai_api_key=OPENAI_API_KEY,
        base_url=OPENAI_URL,
        temperature=args.temp,
        ai_provider=AI_PROVIDER,
        print_details=print_details
    )
    computing_time = time.time() - start
    model_result.append(computing_time)
    model_result.append(summary.replace("\n", "<br/>"))

    console.print(f"Completed {model_name} in : {computing_time:.2f} seconds\n")
    if print_details:
        console.print("Summary:", style="bold green")
        console.print(summary)

    # Output summary
    if args.output:
        with open(args.output, "w") as f:
            f.write(summary)

    if AI_PROVIDER and AI_PROVIDER == "MISTRAL_AI" and not MODEL_NAME == list[-1]:
        console.print("Sleep to avoid rate limit 429")
        time.sleep(5)

    results.append(model_result)

console.print(tabulate(results, headers="firstrow", floatfmt=".2f", tablefmt="unsafehtml"))