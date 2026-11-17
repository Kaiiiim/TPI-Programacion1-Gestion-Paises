import os
from fpdf import FPDF

ROOT = r"C:\Users\kevin\Documents\Proyecto predeterminado"
MD_PATH = os.path.join(ROOT, "docs", "informe.md")
OUT_PATH = os.path.join(ROOT, "informe.pdf")
DOCS_PDF = os.path.join(ROOT, "docs", "informe.pdf")

with open(MD_PATH, encoding="utf-8") as f:
    md_lines = f.read().splitlines()

cleaned = []
for line in md_lines:
    line = line.replace("**", "").replace("`", "")
    cleaned.append(line)
md_lines = cleaned

DARK_BLUE = (15, 40, 90)
GRAY = (110, 110, 110)

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 20, 20)

    def footer(self):
        if self.page_no() > 2:
            self.set_y(-12)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(*GRAY)
            self.cell(0, 10, f"Pagina {self.page_no()}", align="C")
            self.set_text_color(0, 0, 0)

def add_cover(pdf):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*DARK_BLUE)
    pdf.ln(25)
    pdf.cell(0, 8, "Universidad Tecnologica Nacional (UTN)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, "Facultad Regional Mendoza", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Tecnicatura Universitaria en Programacion a Distancia", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Materia: Programacion 1", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(18)
    pdf.set_font("Helvetica", "B", 17)
    pdf.set_text_color(*DARK_BLUE)
    pdf.multi_cell(0, 9, "Gestion de Datos de Paises en Python:\nfiltros, ordenamientos y estadisticas", align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Trabajo Practico Integrador (TPI)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Integrantes:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Kevin Ibanez - Selene Carrascosa", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, "Fecha de entrega:", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "17 de noviembre de 2026", align="C", new_x="LMARGIN", new_y="NEXT")

def find_diagram():
    for ext in (".png", ".jpeg", ".jpg"):
        p = os.path.join(ROOT, "diagrama_flujo" + ext)
        if os.path.exists(p):
            return p
    return None

def render_content(pdf, register=None):
    in_list = False
    for line in md_lines:
        stripped = line.strip()
        if stripped == "":
            pdf.ln(3)
            in_list = False
            continue
        if stripped == "---":
            pdf.ln(2)
            y = pdf.get_y()
            pdf.set_draw_color(180, 180, 180)
            pdf.line(20, y, 190, y)
            pdf.ln(4)
            in_list = False
            continue
        if stripped.startswith("# "):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(*DARK_BLUE)
            pdf.multi_cell(0, 8, stripped[2:].strip())
            pdf.set_text_color(0, 0, 0)
            pdf.ln(2)
            in_list = False
            continue
        if stripped.startswith("## "):
            title = stripped[3:].strip()
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(*DARK_BLUE)
            if register is not None:
                register[title] = pdf.page_no()
            pdf.multi_cell(0, 7, title)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
            in_list = False
            continue
        if stripped.startswith("### "):
            pdf.set_font("Helvetica", "B", 11.5)
            pdf.set_text_color(*DARK_BLUE)
            pdf.multi_cell(0, 6.5, stripped[4:].strip())
            pdf.set_text_color(0, 0, 0)
            pdf.ln(1)
            in_list = False
            continue
        if stripped.startswith("- "):
            text = stripped[2:].strip()
            pdf.set_font("Helvetica", "", 10.5)
            pdf.set_x(24)
            pdf.multi_cell(0, 6, "-  " + text, new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(20)
            in_list = True
            continue
        if stripped.startswith("[INSERTAR IMAGEN:") or stripped.startswith("[INSERTAR CAPTURAS"):
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(*GRAY)
            pdf.multi_cell(0, 6, stripped, align="C")
            pdf.set_text_color(0, 0, 0)
            if "diagrama_flujo" in stripped.lower() or "imagen" in stripped.lower():
                img_path = find_diagram()
                if img_path:
                    pdf.ln(2)
                    pdf.image(img_path, x=25, w=160)
                    pdf.set_font("Helvetica", "I", 9)
                    pdf.set_text_color(*GRAY)
                    pdf.multi_cell(0, 5, "Figura 1: Diagrama de flujo de las operaciones principales.", align="C")
                    pdf.set_text_color(0, 0, 0)
                    pdf.ln(2)
            if "CAPTURAS" in stripped:
                capt_dir = os.path.join(ROOT, "capturas")
                if os.path.isdir(capt_dir):
                    imgs = sorted([f for f in os.listdir(capt_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
                    for idx, img in enumerate(imgs, start=1):
                        pdf.ln(2)
                        pdf.image(os.path.join(capt_dir, img), x=25, w=160)
                        pdf.set_font("Helvetica", "I", 9)
                        pdf.set_text_color(*GRAY)
                        pdf.multi_cell(0, 5, f"Figura {idx + 1}: Captura de ejecucion en consola.", align="C")
                        pdf.set_text_color(0, 0, 0)
                        pdf.ln(2)
            in_list = False
            continue
        pdf.set_font("Helvetica", "", 10.5)
        pdf.multi_cell(0, 6, stripped)
        pdf.ln(1)
        in_list = False

# Pasada 1: medir
dummy = PDF()
dummy.add_page()
register = {}
render_content(dummy, register=register)
section_pages = {title: (pg + 2) for title, pg in register.items()}

index_items = []
for title in md_lines:
    t = title.strip().replace("**", "").replace("`", "")
    if t.startswith("## ") and (len(t) > 3 and t[3:4].isdigit()):
        index_items.append(t[3:].strip())

# Pasada 2: PDF final
pdf = PDF()
add_cover(pdf)

pdf.add_page()
pdf.set_font("Helvetica", "B", 14)
pdf.set_text_color(*DARK_BLUE)
pdf.cell(0, 9, "Indice", new_x="LMARGIN", new_y="NEXT")
pdf.set_text_color(0, 0, 0)
pdf.ln(2)
for item in index_items:
    pg = section_pages.get(item, "")
    pdf.set_font("Helvetica", "", 10.5)
    pdf.cell(150, 7, item, new_x="RIGHT", new_y="TOP")
    pdf.cell(0, 7, str(pg), align="R", new_x="LMARGIN", new_y="NEXT")

pdf.add_page()
render_content(pdf, register=None)

pdf.output(OUT_PATH)
pdf.output(DOCS_PDF)
print("PDF generado:", OUT_PATH)
print("Paginas:", pdf.page_no())
print("Diagrama encontrado:", find_diagram() is not None)
