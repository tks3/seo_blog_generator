"""
prompt.py
プロンプトテンプレート管理モジュール
"""


def build_article_prompt(
    keyword: str,
    title: str,
    audience: str,
    purpose: str,
    word_count: int,
    related_keywords: str = "",
    tone: str = "丁寧（です・ます調）",
) -> str:
    """
    SEO記事生成用のプロンプトを組み立てて返す。

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

    Returns
    -------
    str
        Claude API に送信するプロンプト文字列
    """

    # 関連キーワードの行は入力がある場合のみ追加
    related_kw_line = ""
    if related_keywords and related_keywords.strip():
        related_kw_line = f"- 関連キーワード（本文中に自然に組み込む）：{related_keywords.strip()}"

    prompt = f"""あなたはSEOに精通したプロのブログライターです。
以下の条件に従い、検索上位を狙える高品質なブログ記事を日本語で執筆してください。

【記事条件】
- メインキーワード：{keyword}
- 記事タイトル：{title}
- ターゲット読者：{audience}
- 記事の目的：{purpose}
- 目標文字数：{word_count}字前後
- トーン・文体：{tone}
{related_kw_line}

【構成ルール】
1. 導入文（リード文）
   - 読者の悩みや疑問に共感し、記事を読むメリットを明示する
   - メインキーワードを冒頭付近に自然に含める

2. 本文
   - H2見出し（## ）を3〜5個設ける
   - 必要に応じてH3見出し（### ）で細分化する
   - 各セクションは200〜400字程度でまとめる
   - 箇条書きや番号リストを適切に使い読みやすくする
   - メインキーワードおよび関連キーワードを不自然にならない程度に本文に散りばめる

3. まとめ
   - 記事全体の要点を簡潔に整理する
   - 読者への行動喚起（CTA）を入れる
   - メインキーワードを1回以上含める

【SEOルール】
- タイトルタグに相当する # 見出し（H1）を記事の先頭に1つだけ置く
- メインキーワードをタイトル・導入・まとめに必ず含める
- 共起語・LSIキーワードを本文全体に散りばめる
- 文章は読者目線で分かりやすく、専門用語には簡単な説明を添える

【出力形式】
- Markdown形式で出力する
- コードブロック（```）で囲まない
- 余計な前置きや後書きは不要。記事本文のみ出力する

それでは、上記の条件を満たした記事を執筆してください。
"""

    return prompt.strip()
