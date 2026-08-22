import io
from typing import Tuple, Any, Optional

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    Image = None  # type: ignore


def is_pil_image(obj: Any) -> bool:
    """Check if an object is an instance of PIL.Image.Image."""
    if not PIL_AVAILABLE or Image is None:
        return False
    return isinstance(obj, Image.Image)


def extract_pil_bytes(
    image: Any,
    default_format: str = "PNG",
    quality: int = 80,
) -> Tuple[bytes, str, str]:
    """
    Convert a PIL Image instance to raw bytes with MIME type and filename.
    Returns: (image_bytes, mime_type, filename)
    """
    if not PIL_AVAILABLE or Image is None:
        raise ImportError(
            "Pillow is not installed. Install the PIL extra via `pip install smallpict[pil]`."
        )

    img_format = image.format or default_format
    if img_format.upper() == "JPG":
        img_format = "JPEG"

    buffer = io.BytesIO()
    save_kwargs = {}
    if img_format.upper() in ("JPEG", "WEBP"):
        save_kwargs["quality"] = quality

    # Convert RGBA to RGB if saving as JPEG
    if img_format.upper() == "JPEG" and image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(buffer, format=img_format, **save_kwargs)
    image_bytes = buffer.getvalue()

    mime_type = f"image/{img_format.lower()}"
    filename = f"image.{img_format.lower()}"

    return image_bytes, mime_type, filename
