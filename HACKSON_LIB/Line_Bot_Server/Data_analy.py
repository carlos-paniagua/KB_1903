###データ解析モジュール

##現時点ではテキストに次の単語が含まれていたら、単語を返す。
words = ["スポーツ", "アニメ", "ゲーム", "ゲーム", "プログラム"]


def analy(text: str):
    for t in words:
        if t in text:
            return t
