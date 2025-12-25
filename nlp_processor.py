"""
Natural Language Processor using Claude AI (Anthropic)
"""
from pathlib import Path
from typing import Union, Optional
import anthropic
import config
import prompts


class NLPProcessor:
    """Process markdown content to natural language using Claude AI"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize the NLP Processor
        
        Args:
            api_key: Anthropic API key. If None, uses config.ANTHROPIC_API_KEY
            model: Claude model to use. If None, uses config.CLAUDE_MODEL
        """
        self.api_key = api_key or config.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Anthropic API key is required. "
                "Set ANTHROPIC_API_KEY environment variable or pass it to the constructor."
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = model or config.CLAUDE_MODEL
    
    def process_markdown(
        self, 
        markdown_content: str, 
        use_table_prompt: bool = None,
        custom_prompt: str = None,
        max_tokens: int = None
    ) -> dict:
        """
        Process markdown content to natural language
        
        Args:
            markdown_content: Markdown content to process
            use_table_prompt: If True, use table-specific prompt. If False, use general prompt.
                            If None, automatically detect based on content.
            custom_prompt: Custom prompt to use instead of default prompts
            max_tokens: Maximum tokens for response. If None, uses config.CLAUDE_MAX_TOKENS
        
        Returns:
            Dictionary containing the natural language output and metadata
        """
        max_tokens = max_tokens or config.CLAUDE_MAX_TOKENS
        
        # Get appropriate prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = prompts.get_prompt_for_data(markdown_content, use_table_prompt)
        
        print(f"Processing with Claude AI ({self.model})...")
        print(f"Input length: {len(markdown_content)} characters")
        
        # Call Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract response
        response_text = message.content[0].text
        
        print(f"Output length: {len(response_text)} characters")
        print(f"Tokens used - Input: {message.usage.input_tokens}, Output: {message.usage.output_tokens}")
        
        return {
            "natural_language": response_text,
            "model": self.model,
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
            "prompt_type": "custom" if custom_prompt else ("table" if use_table_prompt else "general")
        }
    
    def process_markdown_file(
        self, 
        markdown_path: Union[str, Path],
        use_table_prompt: bool = None,
        custom_prompt: str = None,
        max_tokens: int = None
    ) -> dict:
        """
        Process a markdown file to natural language
        
        Args:
            markdown_path: Path to markdown file
            use_table_prompt: If True, use table-specific prompt. If False, use general prompt.
                            If None, automatically detect based on content.
            custom_prompt: Custom prompt to use instead of default prompts
            max_tokens: Maximum tokens for response
        
        Returns:
            Dictionary containing the natural language output and metadata
        """
        markdown_path = Path(markdown_path)
        
        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
        
        with open(markdown_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()
        
        result = self.process_markdown(
            markdown_content, 
            use_table_prompt=use_table_prompt,
            custom_prompt=custom_prompt,
            max_tokens=max_tokens
        )
        
        result["source_file"] = markdown_path.name
        return result
    
    def save_natural_language(
        self, 
        processed_data: dict, 
        output_dir: Path = None,
        filename: str = None
    ) -> Path:
        """
        Save natural language content to a file
        
        Args:
            processed_data: Dictionary returned from process methods
            output_dir: Directory to save the file. Defaults to config.NATURAL_LANGUAGE_DIR
            filename: Output filename. If None, uses source filename or generates one
        
        Returns:
            Path to the saved file
        """
        output_dir = output_dir or config.NATURAL_LANGUAGE_DIR
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if filename is None:
            if "source_file" in processed_data:
                filename = Path(processed_data["source_file"]).stem + "_nl.txt"
            else:
                filename = "natural_language_output.txt"
        
        output_path = output_dir / filename
        
        # Create output with metadata
        output_content = f"""# 自然言語処理結果
# Model: {processed_data['model']}
# Prompt Type: {processed_data['prompt_type']}
# Input Tokens: {processed_data['input_tokens']}
# Output Tokens: {processed_data['output_tokens']}

{processed_data['natural_language']}
"""
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_content)
        
        print(f"Saved natural language output to {output_path}")
        return output_path
    
    def process_with_streaming(
        self,
        markdown_content: str,
        use_table_prompt: bool = None,
        custom_prompt: str = None,
        max_tokens: int = None
    ):
        """
        Process markdown content with streaming output
        
        Args:
            markdown_content: Markdown content to process
            use_table_prompt: If True, use table-specific prompt
            custom_prompt: Custom prompt to use
            max_tokens: Maximum tokens for response
        
        Yields:
            Chunks of text as they are generated
        """
        max_tokens = max_tokens or config.CLAUDE_MAX_TOKENS
        
        # Get appropriate prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = prompts.get_prompt_for_data(markdown_content, use_table_prompt)
        
        print(f"Processing with Claude AI ({self.model}) - Streaming...")
        
        # Stream response
        with self.client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        ) as stream:
            for text in stream.text_stream:
                yield text

