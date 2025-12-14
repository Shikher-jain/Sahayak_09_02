# SAHAYAK AI Teaching Assistant

This project is a simple proof-of-concept teaching assistant that
extracts text from uploaded documents (PDFs, images, audio, URLs, YouTube),
creates embeddings, and performs basic RAG-style retrieval to answer questions
from the uploaded content. It includes a small FastAPI backend and a
Streamlit frontend.

**Current status (implemented):**

- Extraction: PDF (`PyMuPDF`), images (`pytesseract`), audio (`whisper`),
	web pages (`requests` + `BeautifulSoup`), and YouTube transcripts.
- Embeddings: `sentence-transformers` (model: `all-MiniLM-L6-v2`, dim=384).
- Storage: local SQLite DB (`pdf_memory.db`) with embedded vectors stored as
	pickled blobs; FAISS (`faiss-cpu`) is used to build an in-memory index on
	demand for nearest-neighbour search.
- Backend: FastAPI app (`backend/main.py`) with endpoints:
	- `POST /upload` — upload PDF or image, extract text, chunk and store
	- `GET /ask` — query the index; currently returns concatenated retrieved
		chunks as the response (no external LLM integrated yet)
- Frontend: Streamlit app (`frontend/app.py`) to upload files and ask questions.

## Project structure

```
Sahayak_09_02/
├── backend/            # FastAPI app and processing modules
├── data/               # datasets and storage (pdf_storage/)
├── frontend/           # Streamlit UI
├── requirements.txt    # top-level Python dependencies
└── README.md
```

## Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. Run the backend:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

3. Run the frontend (in a second terminal):

```bash
streamlit run frontend/app.py
```

4. In the Streamlit UI you can upload a PDF or image and then ask a question.
	 Uploaded files are saved to `data/pdf_storage/`, and chunks/embeddings go
	 into `pdf_memory.db`.

## Limitations & notes

- The `GET /ask` handler currently returns concatenated retrieved chunks as a
	basic answer; integrating a local LLM or external LLM API to form natural
	language answers is a planned next step.
- No deduplication or chunk overlap handling yet; chunk size is a simple
	slicing strategy (500 characters) in `backend/main.py`.
- FAISS index is built in-memory from DB embeddings on every query; it is
	suitable for prototypes but not optimized for large datasets.

## Next steps / Roadmap

1. Integrate a generative model (local LLM or API) to synthesize answers from
	 retrieved context.
2. Add endpoints for `/summarize`, `/ocr` and fine-tune status (finetune flow).
3. Improve chunking, add deduplication and metadata (source, page numbers).
4. Add tests, CI, and containerization (Docker) for deployment.

## Contributing

Open an issue or a PR with a short description of the change. If you add
heavy dependencies, update `requirements.txt` and document the rationale.

## License

This repository currently has no license specified.
