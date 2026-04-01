def match_images(observations, images):
    if not images:
        return observations

    valid_images = []

    #  Step 1: Filter useless images (icons, tiny files, noise)
    for img in images:
        name = img.lower()

        if any(x in name for x in ["icon", "logo", "symbol"]):
            continue

        valid_images.append(img)

    used_images = set()

    for obs in observations:
        obs["images"] = []

        text = (
            (obs.get("area", "") + " " +
             obs.get("issue", "") + " " +
             obs.get("details", ""))
            .lower()
        )

        matched = None

        #  Step 2: Try basic keyword match
        for img in valid_images:
            img_name = img.lower()

            if any(word in img_name for word in text.split()):
                matched = img
                break

        # REMOVE RANDOM FALLBACK
        # no fallback = no wrong images

        if matched:
            used_images.add(matched)
            obs["images"].append(matched)

    return observations
