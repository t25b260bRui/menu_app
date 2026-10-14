"""献立スライド画面の試作品。

準備: python -m pip install nicegui
起動: python menu_app.py
ブラウザで http://localhost:8081 を開いてください。
画像と栄養値は表示用のサンプルです。記録の保存はしません。
"""

import base64
from nicegui import ui

#gitのテスト2

# 献立はここを編集します。画像を写真にする場合は image を変更します。
# 例: "image": "images/chicken.jpg"
MENUS = [
    {"name": "鶏むね肉の彩り定食", "tag": "しっかり食べたい日に",
     "foods": ["ご飯", "鶏むね肉のソテー", "ブロッコリー", "みそ汁"],
     "kcal": 620, "protein": 38, "carbs": 74, "fat": 19,
     "color": "#d4a06a", "background": "#f0e8dc", "image": None},
    {"name": "焼き鮭と小鉢の定食", "tag": "魚が主役の献立",
     "foods": ["ご飯", "焼き鮭", "冷ややっこ", "小松菜のおひたし"],
     "kcal": 580, "protein": 32, "carbs": 69, "fat": 20,
     "color": "#ed987e", "background": "#e4ece8", "image": None},
    {"name": "豆腐ハンバーグ定食", "tag": "気分を変えたい日に",
     "foods": ["ご飯", "豆腐ハンバーグ", "サラダ", "きのこスープ"],
     "kcal": 510, "protein": 25, "carbs": 65, "fat": 17,
     "color": "#9c674b", "background": "#eee5de", "image": None},
]


def meal_image(menu):
    """写真が未登録でも動くように、仮の献立イラストを用意します。"""
    if menu["image"]:
        return menu["image"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="460" viewBox="0 0 900 460">
      <rect width="900" height="460" fill="{menu['background']}"/>
      <rect x="145" y="42" width="610" height="380" rx="28" fill="#b18b66"/>
      <rect x="157" y="54" width="586" height="356" rx="22" fill="#c9a57e"/>
      <ellipse cx="464" cy="210" rx="175" ry="123" fill="#000" opacity=".09"/>
      <ellipse cx="454" cy="197" rx="175" ry="123" fill="#fbfaf5"/>
      <ellipse cx="454" cy="197" rx="150" ry="100" fill="#f1efe7"/>
      <g transform="rotate(-12 436 188)">
        <rect x="343" y="139" width="185" height="95" rx="35" fill="{menu['color']}"/>
        <path d="M377 152l-10 67 M412 149l-10 73 M447 148l-10 76 M482 153l-10 66" stroke="#78452e" stroke-width="5" opacity=".45"/>
      </g>
      <g fill="#638a46"><circle cx="546" cy="170" r="22"/><circle cx="567" cy="195" r="24"/><circle cx="539" cy="217" r="20"/></g>
      <g fill="#d65f46"><circle cx="520" cy="238" r="14"/><circle cx="555" cy="243" r="12"/></g>
      <ellipse cx="276" cy="322" rx="91" ry="63" fill="#203b44"/>
      <ellipse cx="276" cy="312" rx="79" ry="49" fill="#f6f2df"/>
      <g fill="#fffdf0"><circle cx="244" cy="305" r="19"/><circle cx="276" cy="296" r="24"/><circle cx="306" cy="307" r="21"/><circle cx="274" cy="322" r="25"/></g>
      <ellipse cx="627" cy="325" rx="73" ry="54" fill="#653e31"/>
      <ellipse cx="627" cy="318" rx="61" ry="40" fill="#b78b52"/>
      <g fill="#e8d9af"><rect x="607" y="300" width="16" height="14" rx="3"/><rect x="632" y="321" width="17" height="13" rx="3"/></g>
      <g fill="#496a3e"><ellipse cx="647" cy="307" rx="9" ry="4"/><ellipse cx="605" cy="331" rx="8" ry="4"/></g>
      <path d="M701 91v232 M713 91v232" stroke="#654735" stroke-width="7" stroke-linecap="round"/>
    </svg>'''
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


@ui.page("/")
def main_page():
    # 各ブラウザの画面内で選択を管理します。
    selected = {"menu": None}
    ui.colors(primary="#39705a")
    ui.add_css('''
        body {background:#f6f7f3; color:#263c32; font-family: sans-serif;}
        .page {width:100%; max-width:1120px; margin:auto; padding:28px 16px;}
        .layout {display:grid; grid-template-columns:300px minmax(0,1fr); gap:24px; width:100%;}
        .panel {border:1px solid #e1e7df; border-radius:22px; box-shadow:none; padding:24px; background:white;}
        .muted {color:#78877d;}
        .q-carousel {border-radius:18px; background:#eef2eb;}
        .q-carousel__slide {padding:0;}
        @media(max-width:760px) {.layout {grid-template-columns:1fr;} .page {padding:16px 10px;}}
    ''')

    def select_menu(menu):
        selected["menu"] = menu
        selection.refresh()
        ui.notify(f"{menu['name']}を選びました", type="positive")

    @ui.refreshable
    def selection():
        menu = selected["menu"]
        with ui.column().classes("w-full gap-4"):
            ui.label("選んだ献立の栄養素").classes("text-lg font-bold")
            ui.label("1食分 / すべてサンプル値です").classes("muted text-xs")
            for label, key, target, color in [
                ("タンパク質", "protein", 40, "#39705a"),
                ("炭水化物", "carbs", 80, "#d6ab61"),
                ("脂質", "fat", 20, "#a789aa"),
            ]:
                amount = menu[key] if menu else 0
                with ui.row().classes("w-full justify-between"):
                    ui.label(label)
                    ui.label(f"{amount} / {target} g").classes("font-bold")
                ui.linear_progress(value=min(amount / target, 1), color=color, show_value=False).props("rounded size=12px")
            ui.separator()
            ui.label(f"{menu['kcal']} kcal" if menu else "献立を選んでください").classes("text-2xl font-bold")
            ui.label(menu["name"] if menu else "右側の写真を切り替えて選べます").classes("muted text-sm")
            ui.label("バーの基準は動作確認用の仮の値です。個人に合わせた栄養目標ではありません。").classes("muted text-xs")

    with ui.column().classes("page gap-6"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-1"):
                ui.label("MENU DAYS").classes("text-xs font-bold tracking-widest muted")
                ui.label("今日、何を食べよう？").classes("text-3xl font-bold")
            ui.label("献立を選ぶ画面の試作品").classes("muted text-sm")
        ui.label("用意されたセットから、今日の気分に合う献立を選びましょう。").classes("muted")

        with ui.element("div").classes("layout"):
            with ui.card().classes("panel h-fit"):
                selection()
            with ui.column().classes("w-full gap-4"):
                with ui.card().classes("panel w-full gap-4"):
                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label("おすすめの献立セット").classes("text-xl font-bold")
                        ui.label("3セット").classes("muted text-sm")
                    ui.label("左右の矢印、下の丸、またはスワイプで切り替え").classes("muted text-xs")
                    with ui.carousel(animated=True, arrows=True, navigation=True).props(
                        "height=285px infinite swipeable control-color=primary"
                    ).classes("w-full") as carousel:
                        for i, menu in enumerate(MENUS):
                            with ui.carousel_slide(name=str(i)):
                                ui.image(meal_image(menu)).classes("w-full h-full").props("fit=cover no-spinner")

                    @ui.refreshable
                    def menu_detail():
                        menu = MENUS[int(carousel.value or 0)]
                        ui.label(menu["tag"]).classes("text-sm text-green-700")
                        ui.label(menu["name"]).classes("text-2xl font-bold")
                        with ui.row().classes("gap-2"):
                            for food in menu["foods"]:
                                ui.label(food).classes("bg-gray-100 rounded-full px-3 py-1 text-sm")
                        ui.label(f"{menu['kcal']} kcal ・ タンパク質 {menu['protein']} g").classes("muted text-sm")
                        ui.button("この献立にする", icon="check", on_click=lambda: select_menu(menu)).classes("w-full rounded-xl").props("unelevated size=lg")

                    menu_detail()
                    carousel.on_value_change(menu_detail.refresh)
                ui.label("写真の代わりに仮のイラストを表示しています。献立の保存や自動提案はまだ行いません。").classes("muted text-xs px-2")


if __name__ == "__main__":
    ui.run(title="MENU DAYS | 献立セット", host="127.0.0.1", port=8081, reload=False)
    #a