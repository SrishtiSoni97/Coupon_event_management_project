import qrcode
from io import BytesIO
from django.core.files import File

def generate_qr_code(ticket):
    qr = qrcode.make(ticket.ticket_code)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    ticket.qr_code.save(
        f"{ticket.ticket_code}.png",
        File(buffer),
        save=True
    )
