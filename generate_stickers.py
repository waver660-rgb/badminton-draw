"""
まるぼん LINE スタンプ生成スクリプト
オリジナルキャラクター「まるぼん」の24種スタンプをSVG→PNG変換で生成
LINE スタンプ規格: 370×320px, PNG形式
"""

import os
import cairosvg

OUTPUT_DIR = "stickers"
W, H = 370, 320

# カラーパレット
BODY_FILL = "#FFD166"
BODY_STROKE = "#E8A000"
CHEEK = "#FFB3BA"
EYE = "#2D2D2D"
WHITE = "#FFFFFF"
BG = "none"

def svg_header(extra_defs=""):
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>{extra_defs}</defs>
'''

def svg_footer():
    return "</svg>"

def body(cx=185, cy=170, r=110, stroke_w=5):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="{BODY_FILL}" stroke="{BODY_STROKE}" stroke-width="{stroke_w}"/>'

def eye_dot(cx, cy, r=9):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{EYE}"/>'
            f'<circle cx="{cx-3}" cy="{cy-3}" r="3" fill="{WHITE}"/>')

def cheek(cx, cy):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="18" ry="12" fill="{CHEEK}" opacity="0.7"/>'

def text_label(label, x=185, y=305, size=22, color="#444"):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="sans-serif" font-size="{size}" fill="{color}">{label}</text>'

def save(name, content):
    svg_path = os.path.join(OUTPUT_DIR, f"{name}.svg")
    png_path = os.path.join(OUTPUT_DIR, f"{name}.png")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print(f"  ✓ {name}.png")

# ───────────────────────────────────────────────
# 24スタンプ定義
# ───────────────────────────────────────────────

def sticker_01_normal():
    """にこにこ（通常）"""
    return (svg_header()
        + body()
        + eye_dot(155, 160) + eye_dot(215, 160)
        + cheek(145, 185) + cheek(225, 185)
        + '<path d="M165 190 Q185 210 205 190" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + text_label("よろしく！")
        + svg_footer())

def sticker_02_bigsmile():
    """大笑い"""
    return (svg_header()
        + body()
        + '<path d="M148 155 Q155 148 162 155" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M208 155 Q215 148 222 155" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + cheek(143, 182) + cheek(227, 182)
        + '<path d="M155 185 Q185 225 215 185" stroke="#2D2D2D" stroke-width="6" fill="{}" stroke-linecap="round"/>'.format(WHITE)
        + '<path d="M155 185 Q185 225 215 185 Z" fill="#2D2D2D"/>'
        + text_label("わははは！")
        + svg_footer())

def sticker_03_wave():
    """手を振る（やっほー）"""
    return (svg_header()
        + body()
        + eye_dot(155, 160) + eye_dot(215, 160)
        + cheek(145, 185) + cheek(225, 185)
        + '<path d="M165 190 Q185 210 205 190" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 右腕（振る）
        + '<line x1="290" y1="140" x2="330" y2="90" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="290" y1="140" x2="330" y2="90" stroke="{}" stroke-width="18" stroke-linecap="round" fill="none"/>'.format(BODY_STROKE)
        # 左腕
        + '<line x1="80" y1="170" x2="50" y2="200" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + text_label("やっほー！")
        + svg_footer())

def sticker_04_sad():
    """しょんぼり"""
    return (svg_header()
        + body()
        + '<path d="M148 162 Q155 170 162 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M208 162 Q215 170 222 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M168 200 Q185 185 202 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + text_label("しょんぼり…")
        + svg_footer())

def sticker_05_cry():
    """号泣"""
    return (svg_header()
        + body()
        + '<path d="M148 162 Q155 170 162 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M208 162 Q215 170 222 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M168 200 Q185 185 202 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 涙
        + '<ellipse cx="148" cy="188" rx="7" ry="10" fill="#7EC8E3" opacity="0.85"/>'
        + '<ellipse cx="222" cy="188" rx="7" ry="10" fill="#7EC8E3" opacity="0.85"/>'
        + '<ellipse cx="145" cy="205" rx="6" ry="9" fill="#7EC8E3" opacity="0.7"/>'
        + '<ellipse cx="225" cy="205" rx="6" ry="9" fill="#7EC8E3" opacity="0.7"/>'
        + text_label("えーんえーん")
        + svg_footer())

def sticker_06_angry():
    """怒り"""
    return (svg_header()
        + body(cy=175)
        # 眉毛（怒り）
        + '<line x1="140" y1="145" x2="168" y2="155" stroke="#2D2D2D" stroke-width="6" stroke-linecap="round"/>'
        + '<line x1="202" y1="155" x2="230" y2="145" stroke="#2D2D2D" stroke-width="6" stroke-linecap="round"/>'
        + eye_dot(155, 165) + eye_dot(215, 165)
        + '<path d="M165 200 Q185 188 205 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 怒りマーク
        + '<text x="255" y="115" font-size="36" fill="#E74C3C">💢</text>'
        + text_label("もーっ！！")
        + svg_footer())

def sticker_07_surprise():
    """びっくり"""
    return (svg_header()
        + body()
        + '<circle cx="155" cy="160" r="13" fill="{}" stroke="{}" stroke-width="3"/>'.format(EYE, EYE)
        + '<circle cx="215" cy="160" r="13" fill="{}" stroke="{}" stroke-width="3"/>'.format(EYE, EYE)
        + '<circle cx="150" cy="156" r="4" fill="{}" />'.format(WHITE)
        + '<circle cx="210" cy="156" r="4" fill="{}" />'.format(WHITE)
        + '<ellipse cx="185" cy="198" rx="15" ry="18" fill="#2D2D2D"/>'
        + text_label("びっくり！！")
        + svg_footer())

def sticker_08_sleep():
    """ぐっすり"""
    return (svg_header()
        + body(cy=185)
        # 目（閉じてる）
        + '<path d="M143 162 Q155 155 167 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M203 162 Q215 155 227 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + cheek(145, 182) + cheek(225, 182)
        # zzz
        + '<text x="240" y="120" font-family="sans-serif" font-size="30" fill="#7EC8E3" font-weight="bold">z</text>'
        + '<text x="258" y="100" font-family="sans-serif" font-size="22" fill="#7EC8E3" font-weight="bold">z</text>'
        + '<text x="272" y="83" font-family="sans-serif" font-size="16" fill="#7EC8E3" font-weight="bold">z</text>'
        + text_label("おやすみ〜")
        + svg_footer())

def sticker_09_think():
    """考え中"""
    return (svg_header()
        + body()
        + eye_dot(155, 158) + eye_dot(215, 158)
        + '<path d="M165 192 Q185 185 205 192" stroke="#2D2D2D" stroke-width="4" fill="none" stroke-linecap="round"/>'
        # 手（アゴに当てる）
        + '<line x1="290" y1="150" x2="250" y2="195" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        # 吹き出し
        + '<ellipse cx="310" cy="80" rx="40" ry="25" fill="{}" stroke="#ccc" stroke-width="2"/>'.format(WHITE)
        + '<text x="310" y="88" text-anchor="middle" font-size="22">🤔</text>'
        + text_label("うーん…")
        + svg_footer())

def sticker_10_love():
    """大好き"""
    return (svg_header()
        + body()
        # ハートの目
        + '<text x="137" y="175" font-size="30">❤️</text>'
        + '<text x="195" y="175" font-size="30">❤️</text>'
        + cheek(145, 188) + cheek(225, 188)
        + '<path d="M162 200 Q185 220 208 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # ハートたくさん
        + '<text x="60" y="90" font-size="24">💕</text>'
        + '<text x="270" y="80" font-size="20">💕</text>'
        + '<text x="40" y="130" font-size="16">💕</text>'
        + text_label("だいすき〜！")
        + svg_footer())

def sticker_11_thumbsup():
    """グッド！"""
    return (svg_header()
        + body()
        + eye_dot(155, 158) + eye_dot(215, 158)
        + cheek(145, 185) + cheek(225, 185)
        + '<path d="M165 190 Q185 208 205 190" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 親指
        + '<rect x="290" y="130" width="28" height="45" rx="12" fill="{}" stroke="{}" stroke-width="4"/>'.format(BODY_FILL, BODY_STROKE)
        + '<rect x="290" y="95" width="22" height="38" rx="10" fill="{}" stroke="{}" stroke-width="4"/>'.format(BODY_FILL, BODY_STROKE)
        + text_label("グッド！👍")
        + svg_footer())

def sticker_12_run():
    """走る"""
    return (svg_header()
        + body(cx=200, cy=168)
        + eye_dot(170, 155) + eye_dot(230, 155)
        + cheek(162, 178) + cheek(238, 178)
        + '<path d="M180 185 Q200 200 220 185" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 腕
        + '<line x1="300" y1="140" x2="340" y2="110" stroke="{}" stroke-width="16" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="110" y1="155" x2="75" y2="130" stroke="{}" stroke-width="16" stroke-linecap="round"/>'.format(BODY_FILL)
        # 足
        + '<line x1="200" y1="278" x2="230" y2="305" stroke="{}" stroke-width="16" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="200" y1="278" x2="170" y2="310" stroke="{}" stroke-width="16" stroke-linecap="round"/>'.format(BODY_FILL)
        # 速度線
        + '<line x1="30" y1="145" x2="85" y2="145" stroke="#AAA" stroke-width="3" stroke-dasharray="6,4"/>'
        + '<line x1="20" y1="165" x2="78" y2="165" stroke="#AAA" stroke-width="3" stroke-dasharray="6,4"/>'
        + text_label("ダッシュ！！")
        + svg_footer())

def sticker_13_eat():
    """もぐもぐ"""
    return (svg_header()
        + body()
        + '<path d="M143 155 Q155 148 167 155" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M203 155 Q215 148 227 155" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + cheek(143, 178) + cheek(227, 178)
        # もぐもぐ口
        + '<ellipse cx="185" cy="200" rx="22" ry="14" fill="#2D2D2D"/>'
        + '<ellipse cx="185" cy="196" rx="22" ry="9" fill="{}" />'.format(WHITE)
        # 食べ物
        + '<text x="265" y="155" font-size="34">🍙</text>'
        + text_label("もぐもぐ〜")
        + svg_footer())

def sticker_14_dance():
    """ダンス"""
    return (svg_header()
        + body(cx=185, cy=168)
        + eye_dot(155, 155) + eye_dot(215, 155)
        + cheek(145, 178) + cheek(225, 178)
        + '<path d="M165 188 Q185 206 205 188" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 腕（両方上げ）
        + '<line x1="75" y1="140" x2="45" y2="105" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="295" y1="140" x2="325" y2="105" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        # 音符
        + '<text x="50" y="70" font-size="26">🎵</text>'
        + '<text x="290" y="65" font-size="22">🎶</text>'
        + text_label("ノリノリ〜♪")
        + svg_footer())

def sticker_15_ok():
    """OK！"""
    return (svg_header()
        + body()
        + eye_dot(155, 158) + eye_dot(215, 158)
        + cheek(145, 185) + cheek(225, 185)
        + '<path d="M165 190 Q185 210 205 190" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # OKサイン
        + '<circle cx="315" cy="135" r="22" fill="none" stroke="{}" stroke-width="8"/>'.format(BODY_FILL)
        + '<line x1="330" y1="118" x2="348" y2="100" stroke="{}" stroke-width="8" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="330" y1="118" x2="348" y2="100" stroke="{}" stroke-width="8" stroke-linecap="round"/>'.format(BODY_STROKE)
        + '<text x="185" y="52" text-anchor="middle" font-family="sans-serif" font-size="32" fill="#27AE60" font-weight="bold">OK!</text>'
        + text_label("まかせて！")
        + svg_footer())

def sticker_16_no():
    """だめー"""
    return (svg_header()
        + body()
        # バツ目
        + '<line x1="143" y1="148" x2="163" y2="168" stroke="#E74C3C" stroke-width="6" stroke-linecap="round"/>'
        + '<line x1="163" y1="148" x2="143" y2="168" stroke="#E74C3C" stroke-width="6" stroke-linecap="round"/>'
        + '<line x1="203" y1="148" x2="223" y2="168" stroke="#E74C3C" stroke-width="6" stroke-linecap="round"/>'
        + '<line x1="223" y1="148" x2="203" y2="168" stroke="#E74C3C" stroke-width="6" stroke-linecap="round"/>'
        + '<path d="M168 200 Q185 188 202 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # ×マーク大
        + '<text x="185" y="52" text-anchor="middle" font-size="30" fill="#E74C3C">✕ だめ！✕</text>'
        + text_label("それはNO！")
        + svg_footer())

def sticker_17_dizzy():
    """ぐるぐる（混乱）"""
    return (svg_header()
        + body()
        # グルグル目
        + '<text x="133" y="178" font-size="32">🌀</text>'
        + '<text x="191" y="178" font-size="32">🌀</text>'
        + '<path d="M168 200 Q185 192 202 200" stroke="#2D2D2D" stroke-width="4" fill="none" stroke-linecap="round"/>'
        # 星くるくる
        + '<text x="55" y="105" font-size="20">⭐</text>'
        + '<text x="285" y="100" font-size="16">✨</text>'
        + text_label("ぐるぐる〜")
        + svg_footer())

def sticker_18_sick():
    """ぐったり"""
    return (svg_header()
        + body(cy=185)
        + '<path d="M143 162 Q155 170 167 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M203 162 Q215 170 227 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M168 200 Q185 190 202 200" stroke="#2D2D2D" stroke-width="4" fill="none" stroke-linecap="round"/>'
        # 青顔
        + '<ellipse cx="185" cy="185" rx="108" ry="108" fill="#D5E8FF" opacity="0.35"/>'
        # 体温計
        + '<text x="270" y="130" font-size="28">🌡️</text>'
        + text_label("つかれた〜")
        + svg_footer())

def sticker_19_jump():
    """やったー！"""
    return (svg_header()
        + body(cy=150)
        + eye_dot(155, 137) + eye_dot(215, 137)
        + cheek(145, 162) + cheek(225, 162)
        + '<path d="M162 168 Q185 190 208 168" stroke="#2D2D2D" stroke-width="6" fill="none" stroke-linecap="round"/>'
        # 両腕バンザイ
        + '<line x1="76" y1="118" x2="40" y2="75" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="294" y1="118" x2="330" y2="75" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        # 紙吹雪
        + '<text x="38" y="55" font-size="18">🎉</text>'
        + '<text x="295" y="52" font-size="18">🎊</text>'
        + text_label("やったー！！")
        + svg_footer())

def sticker_20_bow():
    """よろしくおねがい"""
    return (svg_header()
        + body(cx=185, cy=200)
        + eye_dot(155, 187) + eye_dot(215, 187)
        + cheek(145, 208) + cheek(225, 208)
        + '<path d="M165 218 Q185 232 205 218" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # おじぎ線
        + '<line x1="185" y1="90" x2="230" y2="50" stroke="#ccc" stroke-width="2" stroke-dasharray="5,3"/>'
        + '<text x="185" y="45" text-anchor="middle" font-size="20" fill="#888">ペコリ</text>'
        + text_label("よろしく！")
        + svg_footer())

def sticker_21_cheer():
    """がんばれ！"""
    return (svg_header()
        + body()
        + eye_dot(155, 158) + eye_dot(215, 158)
        + cheek(145, 182) + cheek(225, 182)
        + '<path d="M162 190 Q185 210 208 190" stroke="#2D2D2D" stroke-width="6" fill="none" stroke-linecap="round"/>'
        # 応援
        + '<text x="45" y="120" font-size="26">📣</text>'
        + '<text x="280" y="120" font-size="26">📣</text>'
        + '<text x="185" y="52" text-anchor="middle" font-family="sans-serif" font-size="28" fill="#E74C3C" font-weight="bold">ファイト！</text>'
        + text_label("がんばれ〜！")
        + svg_footer())

def sticker_22_sorry():
    """ごめんなさい"""
    return (svg_header()
        + body()
        + '<path d="M143 162 Q155 170 167 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M203 162 Q215 170 227 162" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        + '<path d="M168 200 Q185 188 202 200" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # 両手合わせ（ごめん）
        + '<line x1="76" y1="170" x2="50" y2="200" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="294" y1="170" x2="320" y2="200" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<text x="185" y="52" text-anchor="middle" font-size="22" fill="#888">ごめんなさい🙏</text>'
        + text_label("ごめんね！")
        + svg_footer())

def sticker_23_lol():
    """爆笑"""
    return (svg_header()
        + body()
        # 目（笑い）
        + '<path d="M140 152 Q155 165 170 152" stroke="#2D2D2D" stroke-width="6" fill="none" stroke-linecap="round"/>'
        + '<path d="M200 152 Q215 165 230 152" stroke="#2D2D2D" stroke-width="6" fill="none" stroke-linecap="round"/>'
        + cheek(143, 178) + cheek(227, 178)
        # 大笑いの口
        + '<path d="M150 190 Q185 235 220 190" stroke="#2D2D2D" stroke-width="6" fill="#2D2D2D" stroke-linecap="round"/>'
        + '<path d="M150 190 Q185 235 220 190 Q185 205 150 190" fill="{}" />'.format(WHITE)
        # 涙
        + '<ellipse cx="143" cy="195" rx="6" ry="9" fill="#7EC8E3" opacity="0.85"/>'
        + '<ellipse cx="227" cy="195" rx="6" ry="9" fill="#7EC8E3" opacity="0.85"/>'
        + text_label("ウケるwww")
        + svg_footer())

def sticker_24_bye():
    """バイバイ"""
    return (svg_header()
        + body()
        + eye_dot(155, 158) + eye_dot(215, 158)
        + cheek(145, 182) + cheek(225, 182)
        + '<path d="M165 192 Q185 210 205 192" stroke="#2D2D2D" stroke-width="5" fill="none" stroke-linecap="round"/>'
        # バイバイの手
        + '<line x1="290" y1="138" x2="335" y2="95" stroke="{}" stroke-width="18" stroke-linecap="round"/>'.format(BODY_FILL)
        + '<line x1="290" y1="138" x2="335" y2="95" stroke="{}" stroke-width="3" stroke-linecap="round"/>'.format(BODY_STROKE)
        # キラキラ
        + '<text x="298" y="75" font-size="18">✨</text>'
        + text_label("またね〜！")
        + svg_footer())

# ───────────────────────────────────────────────
# 生成実行
# ───────────────────────────────────────────────

stickers = [
    ("01_normal",    sticker_01_normal),
    ("02_bigsmile",  sticker_02_bigsmile),
    ("03_wave",      sticker_03_wave),
    ("04_sad",       sticker_04_sad),
    ("05_cry",       sticker_05_cry),
    ("06_angry",     sticker_06_angry),
    ("07_surprise",  sticker_07_surprise),
    ("08_sleep",     sticker_08_sleep),
    ("09_think",     sticker_09_think),
    ("10_love",      sticker_10_love),
    ("11_thumbsup",  sticker_11_thumbsup),
    ("12_run",       sticker_12_run),
    ("13_eat",       sticker_13_eat),
    ("14_dance",     sticker_14_dance),
    ("15_ok",        sticker_15_ok),
    ("16_no",        sticker_16_no),
    ("17_dizzy",     sticker_17_dizzy),
    ("18_sick",      sticker_18_sick),
    ("19_jump",      sticker_19_jump),
    ("20_bow",       sticker_20_bow),
    ("21_cheer",     sticker_21_cheer),
    ("22_sorry",     sticker_22_sorry),
    ("23_lol",       sticker_23_lol),
    ("24_bye",       sticker_24_bye),
]

os.makedirs(OUTPUT_DIR, exist_ok=True)
print("まるぼん スタンプ生成中...")
for name, fn in stickers:
    save(name, fn())
print(f"\n完了！{len(stickers)}枚のスタンプを {OUTPUT_DIR}/ に保存しました。")
