"""Escritor minimo de archivos .docx (solo biblioteca estandar + Pillow para medir imagenes)."""
import zipfile
from xml.sax.saxutils import escape

from PIL import Image

EMU = 914400


def Inches(x):
    return int(x * EMU)


class Document:
    def __init__(self):
        self.body = []
        self.imgs = []

    def _run(self, text, code=False, bold=False, size=None):
        props = ""
        if code:
            props += '<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>'
        if bold:
            props += "<w:b/>"
        if size:
            props += f'<w:sz w:val="{size}"/>'
        lines = text.replace("\r", "").split("\n")
        out = ""
        for i, l in enumerate(lines):
            if i:
                out += "<w:br/>"
            out += f'<w:t xml:space="preserve">{escape(l)}</w:t>'
        return f"<w:r><w:rPr>{props}</w:rPr>{out}</w:r>"

    def add_heading(self, text, level=1):
        size = {0: 44, 1: 32, 2: 26}[level]
        self.body.append(f"<w:p><w:pPr><w:spacing w:before=\"240\" w:after=\"120\"/></w:pPr>"
                         f"{self._run(text, bold=True, size=size)}</w:p>")

    def add_paragraph(self, text):
        self.body.append(f"<w:p>{self._run(text)}</w:p>")

    def add_code(self, text):
        self.body.append(f"<w:p>{self._run(text, code=True, size=18)}</w:p>")

    def add_bullet(self, text):
        self.body.append(f'<w:p><w:pPr><w:ind w:left="540" w:hanging="270"/></w:pPr>{self._run("• " + text)}</w:p>')

    def add_page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def add_caption(self, text):
        self.body.append(f'<w:p><w:pPr><w:jc w:val="center"/></w:pPr>{self._run(text, size=18)}</w:p>')

    def add_table(self, filas):
        b = "".join(f'<w:{s} w:val="single" w:sz="4" w:color="808080"/>' for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        x = f"<w:tbl><w:tblPr><w:tblW w:w=\"5000\" w:type=\"pct\"/><w:tblBorders>{b}</w:tblBorders></w:tblPr>"
        for i, fila in enumerate(filas):
            x += "<w:tr>"
            for c in fila:
                sh = '<w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/>' if i == 0 else ""
                x += f"<w:tc><w:tcPr>{sh}</w:tcPr><w:p>{self._run(c, bold=(i == 0), size=20)}</w:p></w:tc>"
            x += "</w:tr>"
        self.body.append(x + "</w:tbl><w:p/>")

    def add_picture(self, path, width, max_height=None):
        idx = len(self.imgs) + 1
        self.imgs.append(path)
        w, h = Image.open(path).size
        if max_height and width * h / w > max_height:
            width = int(max_height * w / h)
        cy = int(width * h / w)
        self.body.append(
            '<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{width}" cy="{cy}"/><wp:docPr id="{idx}" name="img{idx}"/>'
            '<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{idx}" name="img{idx}"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="rId{idx}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')

    def save(self, path):
        ns = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
              'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
              'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
              'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
              'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"')
        doc = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document {ns}><w:body>'
               + "".join(self.body) + "</w:body></w:document>")
        rels = "".join(
            f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/img{i}.png"/>'
            for i in range(1, len(self.imgs) + 1))
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml",
                       '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
                       '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
                       '<Default Extension="xml" ContentType="application/xml"/>'
                       '<Default Extension="png" ContentType="image/png"/>'
                       '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
            z.writestr("_rels/.rels",
                       '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
            z.writestr("word/_rels/document.xml.rels",
                       '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       + rels + "</Relationships>")
            z.writestr("word/document.xml", doc)
            for i, p in enumerate(self.imgs, 1):
                z.write(p, f"word/media/img{i}.png")
