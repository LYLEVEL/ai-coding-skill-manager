import os
from pathlib import Path
from PIL import Image, ImageDraw

def create_app_icon():
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    static_dir = Path("static")

    # 创建 256x256 高清原图
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制清新圆角渐变底色
    # 从 (16, 185, 129) 到 (13, 148, 136)
    margin = 12
    corner_radius = 52
    
    # 底板渐变
    for y in range(margin, size - margin):
        ratio = (y - margin) / float(size - 2 * margin)
        r = int(16 * (1 - ratio) + 13 * ratio)
        g = int(185 * (1 - ratio) + 148 * ratio)
        b = int(129 * (1 - ratio) + 136 * ratio)
        draw.line([(margin, y), (size - margin, y)], fill=(r, g, b, 255))

    # 应用圆角遮罩
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([margin, margin, size - margin, size - margin], radius=corner_radius, fill=255)
    
    # 遮罩融合
    rounded_bg = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    rounded_bg.paste(img, (0, 0), mask=mask)
    
    # 绘制内部白色高光标志（Antigravity 风格的四角星芒与核心微光）
    draw_fg = ImageDraw.Draw(rounded_bg)
    cx, cy = size // 2, size // 2

    # 四角星芒
    sparkle = [
        (cx, cy - 64),
        (cx + 18, cy - 20),
        (cx + 64, cy),
        (cx + 18, cy + 20),
        (cx, cy + 64),
        (cx - 18, cy + 20),
        (cx - 64, cy),
        (cx - 18, cy - 20)
    ]
    draw_fg.polygon(sparkle, fill=(255, 255, 255, 255))
    
    # 内部小星芒微光
    small_sparkle = [
        (cx + 42, cy - 42 - 18),
        (cx + 42 + 6, cy - 42 - 6),
        (cx + 42 + 18, cy - 42),
        (cx + 42 + 6, cy - 42 + 6),
        (cx + 42, cy - 42 + 18),
        (cx + 42 - 6, cy - 42 + 6),
        (cx + 42 - 18, cy - 42),
        (cx + 42 - 6, cy - 42 - 6)
    ]
    draw_fg.polygon(small_sparkle, fill=(255, 255, 255, 220))

    # 生成各尺寸并打包为 ico
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    ico_path = assets_dir / "app.ico"
    rounded_bg.save(ico_path, format="ICO", sizes=icon_sizes)
    
    # 同时也保存一份到 static/favicon.ico
    rounded_bg.save(static_dir / "favicon.ico", format="ICO", sizes=icon_sizes)
    rounded_bg.save(assets_dir / "app.png", format="PNG")
    print(f"Icon created successfully: {ico_path}")

if __name__ == "__main__":
    create_app_icon()
