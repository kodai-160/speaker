import os
font_path = 'C:\\Windows\\Fonts\\Cambria.ttf'  # 正しいフォントファイルのパスに変更してください

if os.path.exists(font_path):
    print(f"ファイルが存在します: {font_path}")
else:
    print(f"ファイルが見つかりません: {font_path}")
