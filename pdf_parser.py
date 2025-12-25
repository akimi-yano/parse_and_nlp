"""
PDF to Markdown converter using Llama Parse
"""
import asyncio
from pathlib import Path
from typing import List, Union
from llama_cloud_services import LlamaParse
import config


class PDFParser:
    """Parse PDF files to Markdown using Llama Parse"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the PDF Parser
        
        Args:
            api_key: Llama Parse API key. If None, uses config.LLAMA_PARSE_API_KEY
        """
        self.api_key = api_key or config.LLAMA_PARSE_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Llama Parse API key is required. "
                "Set LLAMA_PARSE_API_KEY environment variable or pass it to the constructor."
            )
        
        self.parser = LlamaParse(
            api_key=self.api_key,
            **config.LLAMA_PARSE_CONFIG
        )
    
    def parse_single_pdf(self, pdf_path: Union[str, Path]) -> dict:
        """
        Parse a single PDF file synchronously
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing markdown text and metadata
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Parsing {pdf_path.name}...")
        result = self.parser.parse(str(pdf_path))
        
        # Extract markdown content
        markdown_documents = result.get_markdown_documents(split_by_page=True)
        
        # Combine all pages
        full_markdown = "\n\n".join([doc.text for doc in markdown_documents])
        
        return {
            "filename": pdf_path.name,
            "markdown": full_markdown,
            "page_count": len(markdown_documents),
            "result": result
        }
    
    def parse_multiple_pdfs(self, pdf_paths: List[Union[str, Path]]) -> List[dict]:
        """
        Parse multiple PDF files synchronously in batch
        
        Args:
            pdf_paths: List of paths to PDF files
            
        Returns:
            List of dictionaries containing markdown text and metadata
        """
        pdf_paths = [Path(p) for p in pdf_paths]
        
        # Verify all files exist
        for pdf_path in pdf_paths:
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Parsing {len(pdf_paths)} PDF files...")
        results = self.parser.parse([str(p) for p in pdf_paths])
        
        parsed_results = []
        for pdf_path, result in zip(pdf_paths, results):
            markdown_documents = result.get_markdown_documents(split_by_page=True)
            full_markdown = "\n\n".join([doc.text for doc in markdown_documents])
            
            parsed_results.append({
                "filename": pdf_path.name,
                "markdown": full_markdown,
                "page_count": len(markdown_documents),
                "result": result
            })
        
        return parsed_results
    
    async def parse_single_pdf_async(self, pdf_path: Union[str, Path]) -> dict:
        """
        Parse a single PDF file asynchronously
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing markdown text and metadata
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Parsing {pdf_path.name} (async)...")
        result = await self.parser.aparse(str(pdf_path))
        
        markdown_documents = result.get_markdown_documents(split_by_page=True)
        full_markdown = "\n\n".join([doc.text for doc in markdown_documents])
        
        return {
            "filename": pdf_path.name,
            "markdown": full_markdown,
            "page_count": len(markdown_documents),
            "result": result
        }
    
    async def parse_multiple_pdfs_async(self, pdf_paths: List[Union[str, Path]]) -> List[dict]:
        """
        Parse multiple PDF files asynchronously in batch
        
        Args:
            pdf_paths: List of paths to PDF files
            
        Returns:
            List of dictionaries containing markdown text and metadata
        """
        pdf_paths = [Path(p) for p in pdf_paths]
        
        for pdf_path in pdf_paths:
            if not pdf_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        print(f"Parsing {len(pdf_paths)} PDF files (async)...")
        results = await self.parser.aparse([str(p) for p in pdf_paths])
        
        parsed_results = []
        for pdf_path, result in zip(pdf_paths, results):
            markdown_documents = result.get_markdown_documents(split_by_page=True)
            full_markdown = "\n\n".join([doc.text for doc in markdown_documents])
            
            parsed_results.append({
                "filename": pdf_path.name,
                "markdown": full_markdown,
                "page_count": len(markdown_documents),
                "result": result
            })
        
        return parsed_results
    
    def save_markdown(self, parsed_data: dict, output_dir: Path = None) -> Path:
        """
        Save markdown content to a file
        
        Args:
            parsed_data: Dictionary returned from parse methods
            output_dir: Directory to save the markdown file. Defaults to config.MARKDOWN_DIR
            
        Returns:
            Path to the saved markdown file
        """
        output_dir = output_dir or config.MARKDOWN_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filename = Path(parsed_data["filename"]).stem + ".md"
        output_path = output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(parsed_data["markdown"])
        
        print(f"Saved markdown to {output_path}")
        return output_path


def get_all_pdfs_in_directory(directory: Union[str, Path]) -> List[Path]:
    """
    Get all PDF files in a directory
    
    Args:
        directory: Path to directory
        
    Returns:
        List of PDF file paths
    """
    directory = Path(directory)
    return sorted(directory.glob("*.pdf"))

