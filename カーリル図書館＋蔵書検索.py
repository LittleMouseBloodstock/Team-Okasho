import streamlit as st
import requests
import os

def get_title_from_isbn(isbn):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": f"isbn:{isbn}"}
    r = requests.get(url, params=params)
    data = r.json()
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["volumeInfo"].get("title", "タイトル情報なし")
    else:
        return "タイトル情報なし"
    
# 1. 都道府県リスト
pref_list = [
    "北海道", "青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県",
    "茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",
    "新潟県", "富山県", "石川県", "福井県", "山梨県", "長野県",
    "岐阜県", "静岡県", "愛知県", "三重県",
    "滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",
    "鳥取県", "島根県", "岡山県", "広島県", "山口県",
    "徳島県", "香川県", "愛媛県", "高知県",
    "福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県", "沖縄県"
]

st.title("カーリル貸出可図書館検索")

# 2. 都道府県選択
pref = st.selectbox("都道府県を選択してください", pref_list)
isbn = st.text_input("調べたい本のISBNを入力してください", "9784097252900")

if st.button("検索"):
    #  タイトル取得
    title = get_title_from_isbn(isbn)
    st.info(f"書名: {title}")

    appkey = os.getenv("CALIL_API_KEY")
    # 3. 県内の図書館情報取得
    lib_resp = requests.get(
        "https://api.calil.jp/library",
        params={"appkey": appkey, "pref": pref, "format": "json","callback": "no"}
    )
    libraries = lib_resp.json()
    # systemidのユニークリストを作成
    systemids = list(set([lib["systemid"] for lib in libraries]))
    if not systemids:
        st.warning("この都道府県には対応図書館がありません。")
    else:
        # 4. /check APIで蔵書検索
        check_resp = requests.get(
            "https://api.calil.jp/check",
            params={
                "appkey": appkey,
                "isbn": isbn,
                "systemid": ",".join(systemids),
                "format": "json",
                "callback": "no"
            }
        )
        check_data = check_resp.json()
        # 5. 貸出可の図書館だけ抽出
        found = False
        for sysid, sys_result in check_data["books"][isbn].items():
            libkey = sys_result.get("libkey", {})
            for libname, status in libkey.items():
                if status in ["貸出可", "蔵書あり"]:
                    found = True
                    st.success(f"{libname}（{sysid}）: {status}")
        if not found:
            st.info("貸出可の図書館は見つかりませんでした。")
