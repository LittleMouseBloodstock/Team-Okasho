import pandas as pd
import streamlit as st

# CSVファイルのパスを指定（例: CSVファイルが同じディレクトリに保存されている場合）
csv_file_path = "output_with_all_keywords.csv"

# CSVファイルを読み込む
df = pd.read_csv(csv_file_path)

# キーワードのリスト（後半の列名）
keywords = ["どうぶつ", "きょうりゅう", "いぬ", "ねこ", "のりもの", 
            "むし", "おばけ", "あんぱんまん", "そら", "まほう"]

# 追加のキーワードリスト
additional_keywords = ["わくわく", "どきどき", "いらいら", "きらきら", "楽しい", 
                       "かわいい", "シリーズ", "世界", "もの", "シール", "登場"]

# Streamlit UI
st.title("📚 楽しい絵本を見つけよう！")  # 親しみやすいアイコンとタイトル
st.write("こんにちは！絵本の中から、どんなお話が気になるかな？\n")

# 1つ目のキーワードを選んでね
selected_keyword1 = st.selectbox("まずは、絵本に出てくるキャラクターやテーマを選ぼう！", keywords)

# 2つ目のキーワードを選んでね
selected_keyword2 = st.selectbox("次に、どんな気持ちが出てくる絵本が良いかな？", additional_keywords)

# キーワード1と追加のキーワード列が存在するか確認
if selected_keyword1 in df.columns and selected_keyword2 in df.columns:
    # 2つのキーワードに1が入っているデータをフィルタリング
    filtered_df = df[(df[selected_keyword1] == 1) & (df[selected_keyword2] == 1)]
    
    # レビュー点数が高いものを5つ抽出
    if not filtered_df.empty:
        # 'reviewAverage' 列に基づいて降順でソートし、上位5件を表示
        top_5_recommended = filtered_df.sort_values(by='reviewAverage', ascending=False).head(5)
        
        st.write("これらの絵本は、君の選んだテーマと気持ちにぴったりだよ！✨")

        # リコメンドデータを見やすく表示
        for _, row in top_5_recommended.iterrows():
            st.markdown(f"### {row['title']}")
            st.write(f"**著者**: {row['author']}")
            st.write(f"**出版社**: {row['publisherName']}")
            st.write(f"**価格**: {row['itemPrice']}円")
            st.write(f"**発売日**: {row['salesDate']}")
            st.write(f"**レビュー**: {row['reviewAverage']}点")
            
            if 'largeImageUrl' in row and pd.notna(row['largeImageUrl']):
                st.image(row['largeImageUrl'], width=100)  # 絵本の画像を表示
            st.write(f"[詳細はこちら]({row['itemUrl']})\n")

    else:
        st.write("ごめんね、選んだキーワードに合う絵本が見つからなかったよ。別のキーワードで試してみよう！")
else:
    st.write("あれ？選んだキーワードがデータにないみたいだよ。別のキーワードで試してみてね！")
