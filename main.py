"""
Main pipeline script to parse PDFs and convert to natural language
"""
import argparse
import asyncio
from pathlib import Path
import sys
from typing import List, Optional

import config
from pdf_parser import PDFParser, get_all_pdfs_in_directory
from nlp_processor import NLPProcessor


class Pipeline:
    """Main pipeline for PDF to Natural Language conversion"""
    
    def __init__(
        self,
        llama_api_key: str = None,
        anthropic_api_key: str = None,
        use_async: bool = False
    ):
        """
        Initialize the pipeline
        
        Args:
            llama_api_key: Llama Parse API key
            anthropic_api_key: Anthropic API key
            use_async: Whether to use async processing for PDF parsing
        """
        self.pdf_parser = PDFParser(api_key=llama_api_key)
        self.nlp_processor = NLPProcessor(api_key=anthropic_api_key)
        self.use_async = use_async
    
    def process_single_pdf(
        self,
        pdf_path: Path,
        use_table_prompt: bool = None,
        save_markdown: bool = True,
        save_natural_language: bool = True
    ) -> dict:
        """
        Process a single PDF file through the entire pipeline
        
        Args:
            pdf_path: Path to PDF file
            use_table_prompt: Whether to use table-specific prompt
            save_markdown: Whether to save the markdown output
            save_natural_language: Whether to save the natural language output
        
        Returns:
            Dictionary with all processing results
        """
        print(f"\n{'='*60}")
        print(f"Processing: {pdf_path.name}")
        print(f"{'='*60}")
        
        # Step 1: Parse PDF to Markdown
        print("\n[Step 1/3] Parsing PDF to Markdown...")
        parsed_data = self.pdf_parser.parse_single_pdf(pdf_path)
        print(f"✓ Parsed {parsed_data['page_count']} pages")
        
        # Save markdown if requested
        markdown_path = None
        if save_markdown:
            markdown_path = self.pdf_parser.save_markdown(parsed_data)
        
        # Step 2: Convert to Natural Language
        print("\n[Step 2/3] Converting to Natural Language...")
        nl_result = self.nlp_processor.process_markdown(
            parsed_data["markdown"],
            use_table_prompt=use_table_prompt
        )
        print(f"✓ Generated natural language output")
        
        # Save natural language if requested
        nl_path = None
        if save_natural_language:
            print("\n[Step 3/3] Saving results...")
            nl_result["source_file"] = pdf_path.name
            nl_path = self.nlp_processor.save_natural_language(
                nl_result,
                filename=pdf_path.stem + "_nl.txt"
            )
        
        print(f"\n{'='*60}")
        print(f"✓ Completed: {pdf_path.name}")
        print(f"{'='*60}\n")
        
        return {
            "pdf_file": pdf_path.name,
            "markdown": parsed_data["markdown"],
            "markdown_path": markdown_path,
            "natural_language": nl_result["natural_language"],
            "natural_language_path": nl_path,
            "page_count": parsed_data["page_count"],
            "model": nl_result["model"],
            "input_tokens": nl_result["input_tokens"],
            "output_tokens": nl_result["output_tokens"]
        }
    
    async def process_single_pdf_async(
        self,
        pdf_path: Path,
        use_table_prompt: bool = None,
        save_markdown: bool = True,
        save_natural_language: bool = True
    ) -> dict:
        """
        Process a single PDF file asynchronously
        
        Args:
            pdf_path: Path to PDF file
            use_table_prompt: Whether to use table-specific prompt
            save_markdown: Whether to save the markdown output
            save_natural_language: Whether to save the natural language output
        
        Returns:
            Dictionary with all processing results
        """
        print(f"\n{'='*60}")
        print(f"Processing (async): {pdf_path.name}")
        print(f"{'='*60}")
        
        # Step 1: Parse PDF to Markdown (async)
        print("\n[Step 1/3] Parsing PDF to Markdown (async)...")
        parsed_data = await self.pdf_parser.parse_single_pdf_async(pdf_path)
        print(f"✓ Parsed {parsed_data['page_count']} pages")
        
        # Save markdown if requested
        markdown_path = None
        if save_markdown:
            markdown_path = self.pdf_parser.save_markdown(parsed_data)
        
        # Step 2: Convert to Natural Language
        print("\n[Step 2/3] Converting to Natural Language...")
        nl_result = self.nlp_processor.process_markdown(
            parsed_data["markdown"],
            use_table_prompt=use_table_prompt
        )
        print(f"✓ Generated natural language output")
        
        # Save natural language if requested
        nl_path = None
        if save_natural_language:
            print("\n[Step 3/3] Saving results...")
            nl_result["source_file"] = pdf_path.name
            nl_path = self.nlp_processor.save_natural_language(
                nl_result,
                filename=pdf_path.stem + "_nl.txt"
            )
        
        print(f"\n{'='*60}")
        print(f"✓ Completed: {pdf_path.name}")
        print(f"{'='*60}\n")
        
        return {
            "pdf_file": pdf_path.name,
            "markdown": parsed_data["markdown"],
            "markdown_path": markdown_path,
            "natural_language": nl_result["natural_language"],
            "natural_language_path": nl_path,
            "page_count": parsed_data["page_count"],
            "model": nl_result["model"],
            "input_tokens": nl_result["input_tokens"],
            "output_tokens": nl_result["output_tokens"]
        }
    
    def process_multiple_pdfs(
        self,
        pdf_paths: List[Path],
        use_table_prompt: bool = None,
        save_markdown: bool = True,
        save_natural_language: bool = True
    ) -> List[dict]:
        """
        Process multiple PDF files
        
        Args:
            pdf_paths: List of PDF file paths
            use_table_prompt: Whether to use table-specific prompt
            save_markdown: Whether to save markdown outputs
            save_natural_language: Whether to save natural language outputs
        
        Returns:
            List of result dictionaries
        """
        results = []
        
        for pdf_path in pdf_paths:
            try:
                result = self.process_single_pdf(
                    pdf_path,
                    use_table_prompt=use_table_prompt,
                    save_markdown=save_markdown,
                    save_natural_language=save_natural_language
                )
                results.append(result)
            except Exception as e:
                print(f"✗ Error processing {pdf_path.name}: {e}")
                results.append({
                    "pdf_file": pdf_path.name,
                    "error": str(e)
                })
        
        return results
    
    async def process_multiple_pdfs_async(
        self,
        pdf_paths: List[Path],
        use_table_prompt: bool = None,
        save_markdown: bool = True,
        save_natural_language: bool = True
    ) -> List[dict]:
        """
        Process multiple PDF files asynchronously
        
        Args:
            pdf_paths: List of PDF file paths
            use_table_prompt: Whether to use table-specific prompt
            save_markdown: Whether to save markdown outputs
            save_natural_language: Whether to save natural language outputs
        
        Returns:
            List of result dictionaries
        """
        tasks = []
        for pdf_path in pdf_paths:
            task = self.process_single_pdf_async(
                pdf_path,
                use_table_prompt=use_table_prompt,
                save_markdown=save_markdown,
                save_natural_language=save_natural_language
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for pdf_path, result in zip(pdf_paths, results):
            if isinstance(result, Exception):
                print(f"✗ Error processing {pdf_path.name}: {result}")
                processed_results.append({
                    "pdf_file": pdf_path.name,
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Parse PDFs to Markdown and convert to Natural Language using Llama Parse and Claude AI"
    )
    
    parser.add_argument(
        "pdf_path",
        nargs="?",
        default=None,
        help="Path to a PDF file or directory containing PDFs. If not provided, processes all PDFs in the 'data' folder."
    )
    
    parser.add_argument(
        "--llama-api-key",
        help="Llama Parse API key (or set LLAMA_PARSE_API_KEY env variable)"
    )
    
    parser.add_argument(
        "--anthropic-api-key",
        help="Anthropic API key (or set ANTHROPIC_API_KEY env variable)"
    )
    
    parser.add_argument(
        "--table-prompt",
        action="store_true",
        help="Force use of table-specific prompt"
    )
    
    parser.add_argument(
        "--general-prompt",
        action="store_true",
        help="Force use of general prompt"
    )
    
    parser.add_argument(
        "--no-save-markdown",
        action="store_true",
        help="Don't save markdown output"
    )
    
    parser.add_argument(
        "--no-save-nl",
        action="store_true",
        help="Don't save natural language output"
    )
    
    parser.add_argument(
        "--async",
        dest="use_async",
        action="store_true",
        help="Use async processing for PDF parsing"
    )
    
    args = parser.parse_args()
    
    # Determine prompt type
    use_table_prompt = None
    if args.table_prompt:
        use_table_prompt = True
    elif args.general_prompt:
        use_table_prompt = False
    
    # Get PDF paths
    if args.pdf_path:
        pdf_path = Path(args.pdf_path)
        if pdf_path.is_dir():
            pdf_paths = get_all_pdfs_in_directory(pdf_path)
        else:
            pdf_paths = [pdf_path]
    else:
        # Use default data directory
        pdf_paths = get_all_pdfs_in_directory(config.DATA_DIR)
    
    if not pdf_paths:
        print("No PDF files found.")
        sys.exit(1)
    
    print(f"Found {len(pdf_paths)} PDF file(s) to process")
    
    # Initialize pipeline
    try:
        pipeline = Pipeline(
            llama_api_key=args.llama_api_key,
            anthropic_api_key=args.anthropic_api_key,
            use_async=args.use_async
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    # Process PDFs
    if args.use_async:
        results = asyncio.run(
            pipeline.process_multiple_pdfs_async(
                pdf_paths,
                use_table_prompt=use_table_prompt,
                save_markdown=not args.no_save_markdown,
                save_natural_language=not args.no_save_nl
            )
        )
    else:
        results = pipeline.process_multiple_pdfs(
            pdf_paths,
            use_table_prompt=use_table_prompt,
            save_markdown=not args.no_save_markdown,
            save_natural_language=not args.no_save_nl
        )
    
    # Print summary
    print("\n" + "="*60)
    print("PROCESSING SUMMARY")
    print("="*60)
    
    successful = [r for r in results if "error" not in r]
    failed = [r for r in results if "error" in r]
    
    print(f"\nTotal: {len(results)} files")
    print(f"Successful: {len(successful)} files")
    print(f"Failed: {len(failed)} files")
    
    if successful:
        total_tokens = sum(r["input_tokens"] + r["output_tokens"] for r in successful)
        print(f"\nTotal tokens used: {total_tokens:,}")
    
    if failed:
        print("\nFailed files:")
        for result in failed:
            print(f"  - {result['pdf_file']}: {result['error']}")
    
    print("\nOutput directories:")
    print(f"  - Markdown: {config.MARKDOWN_DIR}")
    print(f"  - Natural Language: {config.NATURAL_LANGUAGE_DIR}")


if __name__ == "__main__":
    main()

