import io
import hashlib
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from django.conf import settings
from django.utils import timezone


def generate_certificate(student, course):
    buffer = io.BytesIO()
    w, h = landscape(A4)

    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    c.setTitle(f"Certificado - {course.title}")

    # ── border ──
    border_color = HexColor('#4f46e5')
    c.setStrokeColor(border_color)
    c.setLineWidth(2.5)
    margin = 20
    c.roundRect(margin, margin, w - 2 * margin, h - 2 * margin, 12)
    c.setLineWidth(1)
    c.setStrokeColor(HexColor('#7c3aed'))
    margin2 = 26
    c.roundRect(margin2, margin2, w - 2 * margin2, h - 2 * margin2, 8)

    # ── top decorative line ──
    c.setStrokeColor(HexColor('#4f46e5'))
    c.setLineWidth(4)
    line_y = h - 110
    c.line(80, line_y, w - 80, line_y)

    # ── header ──
    c.setFont('Helvetica-Bold', 14)
    c.setFillColor(HexColor('#4f46e5'))
    c.drawCentredString(w / 2, h - 70, 'LearnHub')

    c.setFont('Helvetica', 10)
    c.setFillColor(HexColor('#6b7280'))
    c.drawCentredString(w / 2, h - 88, 'Plataforma de Aprendizaje Online')

    # ── title ──
    c.setFont('Helvetica-Bold', 28)
    c.setFillColor(HexColor('#1e293b'))
    c.drawCentredString(w / 2, h - 158, 'CERTIFICADO DE FINALIZACION')

    c.setFont('Helvetica', 12)
    c.setFillColor(HexColor('#475569'))
    c.drawCentredString(w / 2, h - 182, 'Otorgado a')

    # ── student name ──
    c.setFont('Helvetica-Bold', 24)
    c.setFillColor(HexColor('#4f46e5'))
    c.drawCentredString(w / 2, h - 218, student.name)

    # ── body ──
    c.setFont('Helvetica', 12)
    c.setFillColor(HexColor('#475569'))
    body_text = f"Por haber completado satisfactoriamente el curso"
    c.drawCentredString(w / 2, h - 246, body_text)

    # ── course name ──
    c.setFont('Helvetica-Bold', 18)
    c.setFillColor(HexColor('#7c3aed'))
    c.drawCentredString(w / 2, h - 275, course.title)

    c.setFont('Helvetica', 11)
    c.setFillColor(HexColor('#64748b'))
    c.drawCentredString(w / 2, h - 298, f"Duracion: {course.duration}  |  Nivel: {course.get_level_display()}")

    # ── line above signature ──
    c.setStrokeColor(HexColor('#cbd5e1'))
    c.setLineWidth(1)
    sig_y = 120
    c.line(w / 2 - 90, sig_y + 15, w / 2 + 90, sig_y + 15)

    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(HexColor('#1e293b'))
    c.drawCentredString(w / 2, sig_y - 2, course.instructor_name)

    c.setFont('Helvetica', 8)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(w / 2, sig_y - 18, 'Instructor del curso')

    # ── date ──
    today = timezone.now().strftime('%d de %B de %Y')
    c.setFont('Helvetica', 9)
    c.setFillColor(HexColor('#94a3b8'))
    c.drawCentredString(w / 2, sig_y - 42, f'Emitido el {today}')

    # ── verification code ──
    unique_str = f"{student.id}-{course.id}-{student.email}-{today}"
    code = hashlib.sha256(unique_str.encode()).hexdigest()[:12].upper()
    c.setFont('Helvetica', 7)
    c.setFillColor(HexColor('#b0b7c3'))
    c.drawCentredString(w / 2, sig_y - 60, f'Codigo de verificacion: {code}')

    # ── footer ──
    c.setFont('Helvetica', 7)
    c.setFillColor(HexColor('#cbd5e1'))
    c.drawCentredString(w / 2, 30, 'LearnHub  -  Transformando el aprendizaje digital')

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer
