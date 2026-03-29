"""
app.py
ArticleForge — SEO記事自動生成ツール
Streamlit メインアプリケーション
"""

import streamlit as st

from generator import generate_article_stream

# ─────────────────────────────────────────────
# ページ設定（必ず最初に呼ぶ）
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ArticleForge｜SEO記事自動生成ツール",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# カスタムCSS（見た目の微調整）
# ─────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* サイドバーの幅を広げる */
    [data-testid="stSidebar"] { min-width: 340px; max-width: 380px; }
    /* 生成ボタンを目立たせる */
    div.stButton > button[kind="primary"] {
        font-size: 1.05rem;
        padding: 0.6rem 1rem;
    }
    /* コードブロックのフォントサイズ調整 */
    .stCodeBlock { font-size: 0.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# ヘッダー
# ─────────────────────────────────────────────
st.title("✍️ ArticleForge")
st.caption("キーワードを入力するだけで、SEO最適化されたブログ記事を自動生成します。")

# ─────────────────────────────────────────────
# サイドバー：入力フォーム
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("📝 記事の設定")
    st.markdown("---")

    # ── 必須項目 ──
    st.subheader("必須項目")

    keyword = st.text_input(
        "🔑 メインキーワード",
        placeholder="例：副業 おすすめ",
        help="記事の中心となるSEOキーワードを入力してください。",
    )

    title = st.text_input(
        "📌 記事タイトル",
        placeholder="例：副業で月5万円稼ぐ方法",
        help="生成する記事のタイトルを入力してください。",
    )

    audience = st.text_input(
        "👤 ターゲット読者",
        placeholder="例：副業に興味がある30代の会社員",
        help="誰に向けて書くかを具体的に入力してください。",
    )

    purpose = st.text_input(
        "🎯 記事の目的",
        placeholder="例：商品購入を促す・情報提供",
        help="この記事で読者に何をしてほしいか入力してください。",
    )

    word_count = st.select_slider(
        "📏 目標文字数",
        options=[1000, 1500, 2000, 2500, 3000],
        value=1500,
        help="生成する記事のおおよその文字数を選んでください。",
    )

    st.markdown("---")

    # ── 任意項目 ──
    st.subheader("任意項目（より精度UP）")

    related_keywords = st.text_input(
        "🔗 関連キーワード",
        placeholder="例：在宅, ネット副業, 初心者",
        help="共起語・LSIキーワードをカンマ区切りで入力してください（省略可）。",
    )

    tone = st.selectbox(
        "🎨 トーン・文体",
        options=[
            "丁寧（です・ます調）",
            "カジュアル",
            "フォーマル（硬め）",
            "フレンドリー",
        ],
        index=0,
        help="記事の文体・雰囲気を選んでください。",
    )

    st.markdown("---")

    # ── 生成ボタン ──
    generate_btn = st.button(
        "🚀 記事を生成する",
        type="primary",
        use_container_width=True,
    )

# ─────────────────────────────────────────────
# メインエリア：出力
# ─────────────────────────────────────────────

# セッションステートで生成済み記事を保持する（再レンダリング対策）
if "generated_article" not in st.session_state:
    st.session_state["generated_article"] = ""
if "generation_done" not in st.session_state:
    st.session_state["generation_done"] = False

# ── 生成ボタンが押されたとき ──
if generate_btn:
    # ── 入力バリデーション ──
    missing = []
    if not keyword.strip():
        missing.append("メインキーワード")
    if not title.strip():
        missing.append("記事タイトル")
    if not audience.strip():
        missing.append("ターゲット読者")
    if not purpose.strip():
        missing.append("記事の目的")

    if missing:
        st.error(f"⚠️ 以下の必須項目を入力してください：{', '.join(missing)}")
        st.stop()

    # ── 前回の記事をリセット ──
    st.session_state["generated_article"] = ""
    st.session_state["generation_done"] = False

    # ── ステータス表示エリア ──
    status_area = st.empty()
    status_area.info("✍️ 記事を生成中です。しばらくお待ちください…")

    # ── 記事表示エリア ──
    article_area = st.empty()

    # ── ストリーミング生成 ──
    try:
        full_text = ""
        for chunk in generate_article_stream(
            keyword=keyword.strip(),
            title=title.strip(),
            audience=audience.strip(),
            purpose=purpose.strip(),
            word_count=word_count,
            related_keywords=related_keywords.strip(),
            tone=tone,
        ):
            full_text += chunk
            article_area.markdown(full_text)

        # 生成完了
        st.session_state["generated_article"] = full_text
        st.session_state["generation_done"] = True
        status_area.success("✅ 記事の生成が完了しました！")

    except ValueError as ve:
        # APIキー未設定など設定ミス
        status_area.error(f"⚙️ 設定エラー：{ve}")
        st.stop()
    except Exception as e:
        # その他の予期せぬエラー
        status_area.error(
            f"⚠️ エラーが発生しました。\n\n"
            f"エラー内容：{e}\n\n"
            "しばらく待ってから再度お試しください。"
            "問題が続く場合はAPIキーや通信環境をご確認ください。"
        )
        st.stop()

# ── 生成済み記事のダウンロード・コピーUIを表示 ──
if st.session_state["generation_done"] and st.session_state["generated_article"]:
    article_text = st.session_state["generated_article"]

    st.markdown("---")
    st.subheader("💾 保存・コピー")

    # コピー用コードブロック（右上のコピーアイコンで1クリックコピー可能）
    with st.expander("📋 Markdownテキストをコピーする（クリックして展開）", expanded=False):
        st.code(article_text, language="markdown")

    # ダウンロードボタン（.txt / .md）
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇️ .txt でダウンロード",
            data=article_text.encode("utf-8"),
            file_name="article.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col2:
        st.download_button(
            label="⬇️ .md でダウンロード",
            data=article_text.encode("utf-8"),
            file_name="article.md",
            mime="text/markdown",
            use_container_width=True,
        )

# ── 初期状態（まだ何も生成していないとき）のガイダンス ──
elif not st.session_state["generation_done"]:
    st.markdown(
        """
        ### 使い方

        1. 👈 左のサイドバーで記事の設定を入力する
        2. **「🚀 記事を生成する」** ボタンを押す
        3. ここに記事がリアルタイムで表示される
        4. 完成したら **コピー** または **ダウンロード** して使う

        ---

        #### ✅ より良い記事を生成するコツ

        | 項目 | 入力例 |
        |---|---|
        | メインキーワード | `副業 おすすめ 初心者` |
        | ターゲット読者 | `月収を増やしたい30代の会社員` |
        | 記事の目的 | `おすすめ副業サービスへの登録を促す` |
        | 関連キーワード | `在宅, スキマ時間, ネット副業` |

        > 💡 **ターゲット読者** と **記事の目的** を具体的に書くほど、記事の精度が上がります！
        """,
        unsafe_allow_html=False,
    )
