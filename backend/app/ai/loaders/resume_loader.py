from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


class ResumeLoader:
    """Extracts raw text from a PDF resume using LangChain's PyPDF loader."""

    def load_text(self, file_path: str | Path) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Resume file not found: {path}")
        loader = PyPDFLoader(str(path))
        pages = loader.load()
        return "\n\n".join(page.page_content for page in pages if page.page_content)

    def load_documents(self, file_path: str | Path):
        return PyPDFLoader(str(file_path)).load()
