# Basic Document Q&A Bot using RAG

A Retrieval-Augmented Generation (RAG) based document question-answering system that allows users to ask questions about a collection of PDF documents.

The system retrieves relevant document chunks using semantic similarity and uses Google Gemini to generate answers grounded only in the retrieved content.

## Features

- PDF document ingestion using PyMuPDF
- Text extraction with page-level source tracking
- Text chunking with overlap
- Semantic embeddings using Sentence Transformers
- Persistent FAISS vector database
- Configurable Top-K retrieval
- Google Gemini for grounded answer generation
- Source citations with document filename and page number
- Separate indexing and querying workflows
- Command-line interface for querying
- Handles questions that cannot be answered from the provided documents

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python 3.11+ |
| PDF Processing | PyMuPDF |
| Text Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| LLM | Google Gemini |
| Environment Variables | python-dotenv |
| Interface | Command Line |

## Architecture

The project has two main workflows.

### 1. Indexing Workflow

```text
PDF Documents
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Sentence Transformer Embeddings
     ↓
FAISS Vector Index
     ↓
Persistent Vector Store

### 2. Querying Workflow
User Question
     ↓
Question Embedding
     ↓
FAISS Similarity Search
     ↓
Top-K Relevant Chunks
     ↓
Retrieved Context
     ↓
Google Gemini
     ↓
Grounded Answer + Source Citations

### Project Structure
document-qa-rag/
│
├── data/
│   ├── ai_risk_management.pdf
│   ├── generative_ai.pdf
│   ├── cybersecurity.pdf
│   ├── cloud_computing.pdf
│   └── machine_learning_bias.pdf
│
├── vector_store/
│   ├── index.faiss
│   └── metadata.pkl
│
├── src/
│   ├── __init__.py
│   ├── ingest.py
│   ├── verify_documents.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── index.py
│   ├── retriever.py
│   ├── generator.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── app.py

## How the System Works

### Document Ingestion

The `ingest.py` module reads PDF files from the `data/` directory using PyMuPDF.

For each page, the system stores:

- Extracted text
- PDF filename
- Page number

The page information is preserved so that the final answers can include source citations.

### Text Chunking

The extracted text is divided into smaller chunks.

Current configuration:

- Chunk size: 500 words
- Chunk overlap: 100 words

The overlap helps preserve context between neighboring chunks.

The current document collection produces:

- 237 pages
- 322 chunks

### Embeddings

Each document chunk is converted into a numerical vector using:

`all-MiniLM-L6-v2`

The resulting embeddings have 384 dimensions.

Embeddings are generated in batches during the indexing process.

### Vector Store

FAISS is used as the vector database for similarity search.

The project uses:

`FAISS IndexFlatIP`

The embeddings are normalized before indexing, allowing inner-product similarity to approximate cosine similarity.

The vector store is saved locally:

```text
vector_store/
├── index.faiss
└── metadata.pkl

### Retrieval

When a user asks a question:

The question is converted into an embedding.
FAISS searches for similar document chunks.
The Top-K relevant chunks are retrieved.
The retrieved chunks are passed to Gemini as context.

The default Top-K value is:

5

This value can be changed in retriever.py.

Answer Generation

Google Gemini receives the user's question and the retrieved document context.

The prompt instructs Gemini to answer using only the retrieved information.

If the answer cannot be found in the provided documents, the system responds:

I could not find the answer in the provided documents.

This helps prevent the system from generating unsupported answers.
## Setup

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd document-qa-rag
2. Create a Virtual Environment
python -m venv venv

Activate the virtual environment on Windows:

venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure the Gemini API Key

Create a .env file in the project root directory.

Add:

GEMINI_API_KEY=your_api_key_here

The API key should not be committed to GitHub.

Indexing Documents

Before asking questions, build the vector store by running:

python src/index.py

This performs the following steps:

PDF Documents
     ↓
Text Extraction
     ↓
Text Chunking
     ↓
Embedding Generation
     ↓
FAISS Index Creation
     ↓
Persistent Vector Store

After successful indexing, the following files are created:

vector_store/
├── index.faiss
└── metadata.pkl
Running the Q&A Bot

After indexing, run:

python src/main.py

The application will display:

DOCUMENT Q&A BOT
Type 'exit' to stop.

Enter a question when prompted.

To stop the application, type:

exit
## Example Questions

### 1. Cloud Computing

**Question:**

What are the essential characteristics of cloud computing?

**Result:**

The system retrieves the five essential characteristics of cloud computing from `cloud_computing.pdf`, including:

- On-demand self-service
- Broad network access
- Resource pooling
- Rapid elasticity
- Measured service

**Source:** `cloud_computing.pdf`, Page 6

### 2. Cybersecurity

**Question:**

What are the core functions of the NIST Cybersecurity Framework?

**Result:**

The system retrieves the six core functions:

- GOVERN
- IDENTIFY
- PROTECT
- DETECT
- RESPOND
- RECOVER

**Source:** `cybersecurity.pdf`, Pages 8–9

### 3. Cross-Document Question

**Question:**

What privacy, environmental, and security risks are associated with AI systems?

**Result:**

The system retrieves relevant information from multiple documents and generates an answer covering privacy, environmental, and security risks.

**Sources include:**

- `ai_risk_management.pdf`
- `generative_ai.pdf`
- `machine_learning_bias.pdf`

### 4. Unanswerable Question

**Question:**

What is the capital of France?

**Result:**

```text
I could not find the answer in the provided documents.
## Technical Decisions

### Why Sentence Transformers?

Sentence Transformers are used to convert document chunks and user questions into numerical vectors.

The `all-MiniLM-L6-v2` model was selected because it is lightweight and suitable for semantic similarity search.

### Why FAISS?

FAISS is used as the vector database for similarity search.

It allows the document embeddings to be stored locally and searched efficiently without requiring an external vector database service.

### Why Fixed-Size Chunking?

The project uses fixed-size chunking with overlap because it is simple, predictable, and easy to explain.

Current configuration:

- Chunk size: 500 words
- Chunk overlap: 100 words

The overlap helps preserve context between neighboring chunks.

### Why Separate Indexing and Querying?

Document embeddings only need to be generated when the documents are indexed.

The indexing workflow creates and saves the persistent FAISS vector store.

During querying, the system only creates an embedding for the user's question and searches the existing vector store.

This avoids regenerating all document embeddings for every question.
## Limitations

- The current system is designed for PDF documents.
- Retrieval quality depends on the quality of the document chunks and embeddings.
- Very broad questions may retrieve less relevant context.
- The system does not currently perform OCR for image-only scanned PDFs.
- The current chunk size and overlap are fixed.
- The answer quality depends on the retrieved context and the language model.
- The current interface is command-line based.

## Future Improvements

Possible improvements include:

- Add a Streamlit web interface.
- Add conversation history.
- Implement improved chunking strategies.
- Add hybrid keyword and semantic retrieval.
- Add retrieval score thresholding.
- Add OCR support for scanned documents.
- Add reranking of retrieved chunks.
- Support additional document formats.
- Add automated evaluation of retrieval and answer quality.
## Security

The Gemini API key is stored using an environment variable in the `.env` file.

The `.env` file is excluded from version control using `.gitignore`.

Never commit or share your API key publicly.

## License

This project was created as an AI/ML internship assignment and educational project.