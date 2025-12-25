# PDF to Natural Language Converter

このプロジェクトは、PDFファイルを**Llama Parse**でMarkdownに変換し、**Claude AI (Sonnet 4.5)** を使って構造化された自然言語テキストに変換するパイプラインです。RAGシステムでの活用に最適化されています。

## 機能

- 🔍 **PDF解析**: Llama Parseを使用して高精度なPDF→Markdown変換
- 🤖 **自然言語変換**: Claude AI Sonnet 4.5で構造化データを自然言語に変換
- 📊 **テーブル対応**: 複雑な表やチャートも情報を欠落させずに処理
- 🔄 **汎用的**: 様々な形式・構造のPDFに対応
- 📝 **RAG最適化**: 検索拡張生成(RAG)システムでの活用に最適化された出力形式

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. API キーの設定

`env.example` をコピーして `.env` ファイルを作成し、APIキーを設定します：

```bash
# Windows PowerShell
Copy-Item env.example .env

# Linux/Mac
cp env.example .env
```

`.env` ファイルを編集して、以下のAPIキーを設定してください：

```
LLAMA_PARSE_API_KEY=your_actual_api_key_here
ANTHROPIC_API_KEY=your_actual_api_key_here
```

**APIキーの取得方法：**
- **Llama Parse**: https://developers.llamaindex.ai/python/cloud/general/api_key/
- **Anthropic**: https://console.anthropic.com/

### 3. 環境変数の読み込み

プロジェクトは自動的に `.env` ファイルから環境変数を読み込みません。以下のいずれかの方法で設定してください：

**方法1: 環境変数として設定 (推奨)**

```bash
# Windows PowerShell
$env:LLAMA_PARSE_API_KEY="your_key_here"
$env:ANTHROPIC_API_KEY="your_key_here"

# Linux/Mac
export LLAMA_PARSE_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"
```

**方法2: コマンドライン引数で指定**

```bash
python main.py --llama-api-key "your_key" --anthropic-api-key "your_key"
```

**方法3: python-dotenvを使用 (オプション)**

`config.py` の先頭に以下を追加：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 使い方

### 基本的な使い方

1. `data` フォルダにPDFファイルを配置

2. パイプラインを実行：

```bash
python main.py
```

これで `data` フォルダ内のすべてのPDFが処理されます。

### 特定のPDFファイルを処理

```bash
python main.py path/to/your/file.pdf
```

### 特定のディレクトリ内のすべてのPDFを処理

```bash
python main.py path/to/your/directory/
```

### オプション

- `--table-prompt`: テーブル専用プロンプトを強制使用
- `--general-prompt`: 汎用プロンプトを強制使用（デフォルトは自動検出）
- `--no-save-markdown`: Markdown出力を保存しない
- `--no-save-nl`: 自然言語出力を保存しない
- `--async`: 非同期処理を使用（高速化）
- `--llama-api-key`: Llama Parse APIキーを指定
- `--anthropic-api-key`: Anthropic APIキーを指定

### 使用例

```bash
# テーブル専用プロンプトを使用
python main.py data/chart.pdf --table-prompt

# 非同期処理で高速化
python main.py --async

# APIキーを直接指定
python main.py --llama-api-key "your_key" --anthropic-api-key "your_key"
```

## プロジェクト構成

```
parse_and_nlp/
├── data/                           # PDFファイルを配置
├── output/
│   ├── markdown/                   # Markdown出力
│   └── natural_language/           # 自然言語出力
├── config.py                       # 設定ファイル
├── pdf_parser.py                   # PDF解析モジュール
├── nlp_processor.py                # NLP処理モジュール
├── prompts.py                      # プロンプトテンプレート
├── main.py                         # メインパイプラインスクリプト
├── requirements.txt                # 依存関係
├── env.example                     # 環境変数のサンプル
└── README.md                       # このファイル
```

## Pythonスクリプトでの使用

### 基本的な使用例

```python
from pathlib import Path
from main import Pipeline

# パイプラインの初期化
pipeline = Pipeline(
    llama_api_key="your_llama_key",
    anthropic_api_key="your_anthropic_key"
)

# 単一PDFの処理
result = pipeline.process_single_pdf(
    Path("data/sample.pdf"),
    use_table_prompt=True,  # Noneで自動検出
    save_markdown=True,
    save_natural_language=True
)

print(result["natural_language"])
```

### 複数PDFの処理

```python
from pdf_parser import get_all_pdfs_in_directory

# ディレクトリ内のすべてのPDFを取得
pdf_paths = get_all_pdfs_in_directory("data")

# 一括処理
results = pipeline.process_multiple_pdfs(
    pdf_paths,
    use_table_prompt=None,  # 自動検出
    save_markdown=True,
    save_natural_language=True
)

for result in results:
    if "error" not in result:
        print(f"{result['pdf_file']}: {result['page_count']} pages processed")
```

### 非同期処理

```python
import asyncio

async def process_pdfs():
    pipeline = Pipeline(use_async=True)
    
    # 非同期で単一PDFを処理
    result = await pipeline.process_single_pdf_async(
        Path("data/sample.pdf")
    )
    
    # または複数PDFを非同期処理
    pdf_paths = get_all_pdfs_in_directory("data")
    results = await pipeline.process_multiple_pdfs_async(pdf_paths)
    
    return results

# 実行
results = asyncio.run(process_pdfs())
```

### カスタムプロンプトの使用

```python
from nlp_processor import NLPProcessor
from prompts import create_custom_prompt

# NLPプロセッサーの初期化
nlp = NLPProcessor(api_key="your_anthropic_key")

# Markdownコンテンツ
markdown_content = "# Sample\n\nThis is a test."

# カスタムプロンプトの作成
custom_prompt = create_custom_prompt(
    markdown_content=markdown_content,
    task_description="このドキュメントの要点を箇条書きで抽出してください。",
    requirements="""
    - 各要点は1行で記述
    - 重要度の高い順に並べる
    - 具体的な数値や名称を含める
    """
)

# 処理
result = nlp.process_markdown(
    markdown_content,
    custom_prompt=custom_prompt
)

print(result["natural_language"])
```

### ストリーミング処理

```python
# リアルタイムで出力を取得
for chunk in nlp.process_with_streaming(markdown_content):
    print(chunk, end="", flush=True)
```

## プロンプトの詳細

### テーブル専用プロンプト

複雑な表やチャートを処理するための専用プロンプト：

- **定義フェーズ**: 縦軸・横軸・凡例の抽出
- **抽出フェーズ**: すべてのセルデータを逐次記述
- **統合フェーズ**: 注釈・補足情報の論理合成
- **要約フェーズ**: 人間が読みやすい形式で解説
- **検証フェーズ**: 3回の精度確認

### 汎用プロンプト

通常の文書やテキストベースのPDFに対応：

- 情報の完全性を保持
- 構造を明確に保つ
- RAGシステムでの検索可能性を重視

## Llama Parse の設定

`config.py` で以下の設定をカスタマイズできます：

```python
LLAMA_PARSE_CONFIG = {
    "tier": "agentic_plus",              # 解析ティア
    "version": "latest",                  # バージョン
    "high_res_ocr": True,                 # 高解像度OCR
    "adaptive_long_table": True,          # 長い表の適応的処理
    "outlined_table_extraction": True,    # アウトライン表の抽出
    "output_tables_as_HTML": True,        # テーブルをHTMLで出力
    "precise_bounding_box": True,         # 精密なバウンディングボックス
    "page_separator": "\n\n---\n\n",     # ページ区切り文字
    "max_pages": 0,                       # 最大ページ数（0=無制限）
}
```

## Claude AI の設定

`config.py` でモデルとトークン数を設定：

```python
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # 使用するClaudeモデル
CLAUDE_MAX_TOKENS = 8000                    # 最大出力トークン数
```

## トラブルシューティング

### APIキーエラー

```
ValueError: Llama Parse API key is required.
```

→ 環境変数またはコマンドライン引数でAPIキーを設定してください。

### PDFが見つからない

```
FileNotFoundError: PDF file not found
```

→ `data` フォルダにPDFファイルが配置されているか確認してください。

### メモリ不足

大きなPDFファイルを処理する場合、メモリ不足になる可能性があります：

- `--async` オプションは使わない（メモリ使用量が増える可能性）
- 1つずつ処理する
- Claude AIの `max_tokens` を調整

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## サポート

問題が発生した場合は、以下を確認してください：

1. APIキーが正しく設定されているか
2. 依存関係がすべてインストールされているか
3. PDFファイルが正しいディレクトリにあるか
4. Python 3.8以上を使用しているか

---

**注意**: このツールはAPIを使用するため、使用量に応じて課金されます。大量のPDFを処理する前に、APIの料金体系を確認してください。
