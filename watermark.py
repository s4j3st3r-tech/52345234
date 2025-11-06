from PIL import Image, ImageDraw, ImageFont
import moviepy.editor as mp
from config import COLORS, FONTS

def add_watermark_image(img_path, output_path, text, position, color, font_name, transparency, size):
    image = Image.open(img_path).convert("RGBA")
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)
    font = ImageFont.truetype(FONTS[font_name], size)
    text_w, text_h = draw.textsize(text, font)

    positions = {
        "Сверху-Слева": (10, 10),
        "Сверху-Справа": (image.width - text_w - 10, 10),
        "Снизу-Слева": (10, image.height - text_h - 10),
        "Снизу-Справа": (image.width - text_w - 10, image.height - text_h - 10),
        "Центр": ((image.width - text_w)//2, (image.height - text_h)//2)
    }

    x, y = positions.get(position, (10, 10))
    draw.text((x, y), text, fill=COLORS[color] + (transparency,), font=font)
    result = Image.alpha_composite(image, txt_layer)
    result.convert("RGB").save(output_path, "JPEG")

def add_watermark_video(input_path, output_path, text, position, color, size):
    clip = mp.VideoFileClip(input_path)
    txt_clip = mp.TextClip(text, fontsize=size, color=color).set_duration(clip.duration)
    txt_clip = txt_clip.set_position(position)
    video = mp.CompositeVideoClip([clip, txt_clip])
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")
