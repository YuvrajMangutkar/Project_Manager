"""
Shared utility to encode PlantUML source and return a public server URL.

Instead of running Java + plantuml.jar locally (which breaks on cloud servers
like Render), we encode the diagram source and send it to the free
PlantUML public server at https://www.plantuml.com/plantuml/png/<encoded>.

No Java, no file storage, no ephemeral filesystem issues.
"""
import zlib
import base64

# PlantUML public server — free, no auth required
PLANTUML_SERVER = "https://www.plantuml.com/plantuml/png"

# PlantUML uses a custom base64 alphabet
_PLANTUML_B64 = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "-_"
)


def _encode6bit(b):
    return _PLANTUML_B64[b & 0x3F]


def _append3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return (
        _encode6bit(c1)
        + _encode6bit(c2)
        + _encode6bit(c3)
        + _encode6bit(c4)
    )


def encode_plantuml(text: str) -> str:
    """Compress + base64-encode PlantUML source for the public server."""
    data = zlib.compress(text.encode("utf-8"), 9)[2:-4]  # raw deflate
    result = ""
    i = 0
    while i < len(data):
        b1 = data[i] if i < len(data) else 0
        b2 = data[i + 1] if i + 1 < len(data) else 0
        b3 = data[i + 2] if i + 2 < len(data) else 0
        result += _append3bytes(b1, b2, b3)
        i += 3
    return result


def plantuml_url(plantuml_code: str) -> str:
    """Return the public server PNG URL for the given PlantUML source."""
    encoded = encode_plantuml(plantuml_code)
    return f"{PLANTUML_SERVER}/{encoded}"
