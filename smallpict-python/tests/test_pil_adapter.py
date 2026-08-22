import pytest
from smallpict.pil_adapter import extract_pil_bytes, is_pil_image

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


@pytest.mark.skipif(not HAS_PIL, reason="Pillow not installed")
def test_pil_adapter_extract_bytes():
    img = Image.new("RGB", (100, 100), color="red")
    assert is_pil_image(img) is True

    raw_bytes, mime, fn = extract_pil_bytes(img, default_format="JPEG", quality=80)
    assert len(raw_bytes) > 0
    assert mime == "image/jpeg"
    assert fn == "image.jpeg"
