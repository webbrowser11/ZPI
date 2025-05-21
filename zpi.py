from mpmath import mp
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import os

# === SETTINGS ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CHUNK_DIR = os.path.join(SCRIPT_DIR, "pi_chunks")
PDF_PATH = os.path.join(SCRIPT_DIR, "pi_million_digits.pdf")
TXT_CHUNK_SIZE = 10_000
FONT_NAME = "Helvetica"  # Proportional font
FONT_SIZE = 11
LINE_SPACING = FONT_SIZE + 4  # Extra padding between lines
MARGIN_LEFT = 50
MARGIN_TOP = 40
MARGIN_BOTTOM = 40
MAX_LINE_WIDTH = 500  # max width in points for text block
CHARS_PER_LINE = 80  # for Helvetica at size 11, this is a safe fit
CHAR_SPACING = 0.1  # Adjust this value to fine-tune character spacing

# === GENERATE PI ===
mp.dps = 1_000_010
pi_str = str(mp.pi)

# === WRITE 100 CHUNKS ===
os.makedirs(CHUNK_DIR, exist_ok=True)
for i in range(100):
    start = i * TXT_CHUNK_SIZE
    end = (i + 1) * TXT_CHUNK_SIZE
    chunk = pi_str[start:end]
    with open(os.path.join(CHUNK_DIR, f"pi_part_{i+1:03}.txt"), "w") as f:
        f.write(chunk)

# === COMPILE TO PDF ===
def compile_to_pdf(input_dir, output_pdf):
    c = canvas.Canvas(output_pdf, pagesize=LETTER)
    width, height = LETTER
    usable_height = height - MARGIN_TOP - MARGIN_BOTTOM
    lines_per_page = int(usable_height // LINE_SPACING)

    c.setFont(FONT_NAME, FONT_SIZE)

    for i in range(100):
        with open(os.path.join(input_dir, f"pi_part_{i+1:03}.txt"), "r") as f:
            digits = f.read()
            lines = [digits[j:j+CHARS_PER_LINE] for j in range(0, len(digits), CHARS_PER_LINE)]

            line_count = 0
            for line in lines:
                if line_count >= lines_per_page:
                    c.showPage()
                    c.setFont(FONT_NAME, FONT_SIZE)
                    line_count = 0

                y = height - MARGIN_TOP - line_count * LINE_SPACING
                x = MARGIN_LEFT

                textobject = c.beginText()
                textobject.setTextOrigin(x, y)
                textobject.setFont(FONT_NAME, FONT_SIZE)
                textobject.setCharSpace(CHAR_SPACING)  # Add character spacing

                textobject.textLine(line)  # Use textLine to write the whole line

                c.drawText(textobject)

                line_count += 1

    c.save()

compile_to_pdf(CHUNK_DIR, PDF_PATH)
print("✅ Clean PDF generated with Helvetica at:", PDF_PATH)