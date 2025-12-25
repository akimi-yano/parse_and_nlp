"""
使用例のサンプルスクリプト
"""
import asyncio
from pathlib import Path
from main import Pipeline
from pdf_parser import get_all_pdfs_in_directory
from nlp_processor import NLPProcessor
from prompts import create_custom_prompt


def example_1_basic_usage():
    """例1: 基本的な使い方"""
    print("\n" + "="*60)
    print("例1: 基本的な使い方")
    print("="*60)
    
    # パイプラインの初期化
    pipeline = Pipeline()
    
    # 単一PDFの処理
    result = pipeline.process_single_pdf(
        Path("data/sample.pdf"),
        use_table_prompt=None,  # 自動検出
        save_markdown=True,
        save_natural_language=True
    )
    
    print(f"\n処理完了:")
    print(f"- ファイル: {result['pdf_file']}")
    print(f"- ページ数: {result['page_count']}")
    print(f"- 使用トークン: {result['input_tokens'] + result['output_tokens']:,}")


def example_2_multiple_pdfs():
    """例2: 複数PDFの処理"""
    print("\n" + "="*60)
    print("例2: 複数PDFの処理")
    print("="*60)
    
    pipeline = Pipeline()
    
    # ディレクトリ内のすべてのPDFを取得
    pdf_paths = get_all_pdfs_in_directory("data")
    
    if not pdf_paths:
        print("PDFファイルが見つかりません")
        return
    
    # 一括処理
    results = pipeline.process_multiple_pdfs(
        pdf_paths,
        use_table_prompt=None,
        save_markdown=True,
        save_natural_language=True
    )
    
    print(f"\n処理完了: {len(results)}ファイル")
    for result in results:
        if "error" not in result:
            print(f"- {result['pdf_file']}: {result['page_count']}ページ")
        else:
            print(f"- {result['pdf_file']}: エラー - {result['error']}")


async def example_3_async_processing():
    """例3: 非同期処理"""
    print("\n" + "="*60)
    print("例3: 非同期処理")
    print("="*60)
    
    pipeline = Pipeline(use_async=True)
    
    # 非同期で単一PDFを処理
    result = await pipeline.process_single_pdf_async(
        Path("data/sample.pdf")
    )
    
    print(f"\n処理完了:")
    print(f"- ファイル: {result['pdf_file']}")
    print(f"- ページ数: {result['page_count']}")


def example_4_custom_prompt():
    """例4: カスタムプロンプトの使用"""
    print("\n" + "="*60)
    print("例4: カスタムプロンプトの使用")
    print("="*60)
    
    # NLPプロセッサーの初期化
    nlp = NLPProcessor()
    
    # サンプルMarkdownコンテンツ
    markdown_content = """
# 会議議事録

## 日時
2025年1月15日 14:00-16:00

## 参加者
- 田中（プロジェクトマネージャー）
- 佐藤（エンジニアリングリーダー）
- 鈴木（デザイナー）

## 議題
1. プロジェクトの進捗確認
2. 次フェーズの計画
3. 予算の見直し
"""
    
    # カスタムプロンプトの作成
    custom_prompt = create_custom_prompt(
        markdown_content=markdown_content,
        task_description="この議事録から、アクションアイテムと決定事項を抽出してください。",
        requirements="""
        - アクションアイテムを箇条書きで列挙
        - 各アイテムに担当者と期限を明記（記載があれば）
        - 決定事項を別セクションで記述
        - 重要度の高い順に並べる
        """
    )
    
    # 処理
    result = nlp.process_markdown(
        markdown_content,
        custom_prompt=custom_prompt
    )
    
    print("\n出力:")
    print(result["natural_language"])


def example_5_table_specific():
    """例5: テーブル専用プロンプトの使用"""
    print("\n" + "="*60)
    print("例5: テーブル専用プロンプトの使用")
    print("="*60)
    
    pipeline = Pipeline()
    
    # テーブルを含むPDFを強制的にテーブルプロンプトで処理
    result = pipeline.process_single_pdf(
        Path("data/table_document.pdf"),
        use_table_prompt=True,  # テーブルプロンプトを強制
        save_markdown=True,
        save_natural_language=True
    )
    
    print(f"\n処理完了:")
    print(f"- ファイル: {result['pdf_file']}")
    print(f"- プロンプトタイプ: テーブル専用")


def example_6_streaming():
    """例6: ストリーミング処理"""
    print("\n" + "="*60)
    print("例6: ストリーミング処理（リアルタイム出力）")
    print("="*60)
    
    nlp = NLPProcessor()
    
    markdown_content = "# サンプルドキュメント\n\nこれはテストです。"
    
    print("\nストリーミング出力開始:")
    print("-" * 60)
    
    # リアルタイムで出力を取得
    for chunk in nlp.process_with_streaming(markdown_content):
        print(chunk, end="", flush=True)
    
    print("\n" + "-" * 60)
    print("ストリーミング出力完了")


def example_7_markdown_only():
    """例7: Markdown変換のみ（自然言語変換なし）"""
    print("\n" + "="*60)
    print("例7: Markdown変換のみ")
    print("="*60)
    
    from pdf_parser import PDFParser
    
    parser = PDFParser()
    
    # PDFをMarkdownに変換（自然言語変換はスキップ）
    parsed_data = parser.parse_single_pdf(Path("data/sample.pdf"))
    
    # Markdownを保存
    markdown_path = parser.save_markdown(parsed_data)
    
    print(f"\nMarkdown保存完了:")
    print(f"- ファイル: {markdown_path}")
    print(f"- ページ数: {parsed_data['page_count']}")


def main():
    """メイン関数"""
    print("\n" + "="*60)
    print("PDF to Natural Language Converter - 使用例")
    print("="*60)
    
    print("\n実行可能な例:")
    print("1. 基本的な使い方")
    print("2. 複数PDFの処理")
    print("3. 非同期処理")
    print("4. カスタムプロンプトの使用")
    print("5. テーブル専用プロンプトの使用")
    print("6. ストリーミング処理")
    print("7. Markdown変換のみ")
    
    print("\n注意:")
    print("- これらの例を実行する前に、APIキーを設定してください")
    print("- dataフォルダにサンプルPDFを配置してください")
    print("- 各例は個別に実行することをお勧めします")
    
    # 実際に実行する場合は、以下のコメントを解除
    # try:
    #     example_1_basic_usage()
    #     example_2_multiple_pdfs()
    #     asyncio.run(example_3_async_processing())
    #     example_4_custom_prompt()
    #     example_5_table_specific()
    #     example_6_streaming()
    #     example_7_markdown_only()
    # except Exception as e:
    #     print(f"\nエラー: {e}")
    #     print("APIキーが設定されているか、PDFファイルが存在するか確認してください")


if __name__ == "__main__":
    main()

