"""
generator.py
Claude API 呼び出し・ストリーミング処理モジュール
"""

import os
from typing import Generator

import anthropic
from dotenv import load_dotenv

from prompt import build_article_prompt

# .env ファイルから環境変数を読み込む
load_dotenv()

# 使用するモデル
MODEL_NAME = "claude-sonnet-4-6"

# 生成トークンの上限（約4,000字相当）
MAX_TOKENS = 4096


def _get_client() -> anthropic.Anthropic:
    """
    Anthropic クライアントを生成して返す。
    APIキーが未設定の場合は ValueError を発生させる。
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY が設定されていません。\n"
            "プロジェクトフォルダに .env ファイルを作成し、\n"
            "ANTHROPIC_API_KEY=your_api_key_here と記述してください。"
        )
    return anthropic.Anthropic(api_key=api_key)


def generate_article_stream(
    keyword: str,
    title: str,
    audience: str,
    purpose: str,
    word_count: int,
    related_keywords: str = "",
    tone: str = "丁寧（です・ます調）",
) -> Generator[str, None, None]:
    """
    Claude API をストリーミングモードで呼び出し、
    生成されたテキストを1チャンクずつ yield する。

    Parameters
    ----------
    keyword : str
        メインキーワード
    title : str
        記事タイトル
    audience : str
        ターゲット読者
    purpose : str
        記事の目的
    word_count : int
        目標文字数
    related_keywords : str
        関連キーワード（カンマ区切り・任意）
    tone : str
        トーン・文体

    Yields
    ------
    str
        ストリーミングで受信したテキストの断片
    """
    client = _get_client()

    # プロンプトを組み立てる
    user_prompt = build_article_prompt(
        keyword=keyword,
        title=title,
        audience=audience,
        purpose=purpose,
        word_count=word_count,
        related_keywords=related_keywords,
        tone=tone,
    )

    # ストリーミングで API 呼び出し
    with client.messages.stream(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        system=(
            "あなたはSEOに精通した日本語のプロブログライターです。"
            "指定された条件に従い、読者に価値を提供する高品質な記事を執筆してください。"
        ),
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    ) as stream:
        for text_chunk in stream.text_stream:
            yield text_chunk
