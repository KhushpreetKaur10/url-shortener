import os
import qrcode

def generate_qr(short_code):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    qr_dir = os.path.join(base_dir, "..", "static", "qrcodes")

    os.makedirs(qr_dir, exist_ok=True)

    # IMPORTANT: use nginx entrypoint
    url = f"http://localhost/{short_code}"

    file_path = os.path.join(qr_dir, f"{short_code}.png")

    if not os.path.exists(file_path):
        img = qrcode.make(url)
        img.save(file_path)

    return f"/static/qrcodes/{short_code}.png"