import hashlib
import os

def clean_images(image_paths):
    unique_images = []
    seen_hashes = set()

    for img_path in image_paths:
        try:
            with open(img_path, "rb") as f:
                img_bytes = f.read()
                img_hash = hashlib.md5(img_bytes).hexdigest()

            # ✅ skip duplicate
            if img_hash in seen_hashes:
                continue

            seen_hashes.add(img_hash)
            unique_images.append(img_path)

        except:
            continue

    print("After cleaning:", len(unique_images))

    return unique_images[:100]  # limit for safety