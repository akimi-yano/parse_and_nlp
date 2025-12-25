"""
API キーの確認用スクリプト
"""
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# APIキーを取得
llama_key = os.getenv("LLAMA_PARSE_API_KEY", "")
anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")

print("="*60)
print("API キーの確認")
print("="*60)

# Llama Parse APIキー
print("\n[Llama Parse API Key]")
if llama_key:
    print(f"✓ 設定済み")
    print(f"  長さ: {len(llama_key)} 文字")
    print(f"  先頭: {llama_key[:10]}...")
    print(f"  末尾: ...{llama_key[-10:]}")
    
    # 形式チェック
    if llama_key.startswith("llx-"):
        print("  ✓ 形式: 正しい (llx- で始まる)")
    else:
        print("  ✗ 警告: llx- で始まっていません")
        print(f"    実際の先頭: {llama_key[:4]}")
    
    # スペースチェック
    if llama_key != llama_key.strip():
        print("  ✗ 警告: 前後にスペースがあります")
    else:
        print("  ✓ スペース: なし")
else:
    print("✗ 設定されていません")

# Anthropic APIキー
print("\n[Anthropic API Key]")
if anthropic_key:
    print(f"✓ 設定済み")
    print(f"  長さ: {len(anthropic_key)} 文字")
    print(f"  先頭: {anthropic_key[:10]}...")
    print(f"  末尾: ...{anthropic_key[-10:]}")
    
    # 形式チェック
    if anthropic_key.startswith("sk-ant-"):
        print("  ✓ 形式: 正しい (sk-ant- で始まる)")
    else:
        print("  ✗ 警告: sk-ant- で始まっていません")
        print(f"    実際の先頭: {anthropic_key[:7]}")
    
    # スペースチェック
    if anthropic_key != anthropic_key.strip():
        print("  ✗ 警告: 前後にスペースがあります")
    else:
        print("  ✓ スペース: なし")
else:
    print("✗ 設定されていません")

print("\n" + "="*60)

# .envファイルの存在確認
from pathlib import Path
env_path = Path(".env")
if env_path.exists():
    print(f"\n✓ .env ファイルが存在します: {env_path.absolute()}")
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"  行数: {len(lines)}")
else:
    print("\n✗ .env ファイルが見つかりません")
    print("  .env ファイルをプロジェクトのルートに作成してください")

print("\n" + "="*60)

