import firebase
from firebase import firebase
import tkinter as tk
from tkinter import *
import arrow
import pyqrcode
from pyfpdf.fpdf import FPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
import subprocess


class Application(tk.Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.btn_clicks = 1999
        self.create_widget()

    def create_widget(self):
        self.button1 = tk.Button(self, text="Personal/Private Banking", bg="blue", fg="white", command=self.buttonpersonal)
        self.button1.pack(padx=85, pady=80)

        self.button2 = tk.Button(self, text="Business Banking", bg="red", fg="white", command=self.buttonbusiness)
        self.button2.pack(padx=85, pady=0)

    def buttonpersonal(self):
        self.btn_clicks += 1
        fb = firebase.FirebaseApplication('https://rasppiqueuems.firebaseio.com/')

        varDate = arrow.now('Asia/Kuala_Lumpur').format('YYYY-MM-DD')

        date = '/' + varDate
        qnum = str(self.btn_clicks)
        queue = '/' + qnum
        utc = arrow.utcnow()

        # QR Code Content
        qrcontent = varDate + '|' + qnum
        qc = pyqrcode.create(qrcontent)
        qc.png('toPrint/qc.png', scale=8)
        # print(qc.terminal(quiet_zone=1))

        pdf = FPDF(orientation='P', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=20)

        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        path = 'toPrint/qc.png'
        imgDoc.drawImage(path, 150, 490)
        imgDoc.save()

        pdf.cell(200, 10, txt="Queue Ticket", ln=1, align="C")
        pdf.image('toPrint/qc.png', 93, 20, 33)
        pdf.cell(198, 80, qnum, 0, 1, 'C')
        pdf.cell(198, -50, txt="Counter 3", ln=1, align="C")
        pdf.output("toPrint/ticketPrint.pdf")

        fb.put('', '/queues' + date + queue, {
            "QNum": qnum,
            "Status": "Pending",
            "Service": "Personal/Private",
            "Time": utc.to('Asia/Kuala_Lumpur').format('HH:mm:ss'),
            "TDate": utc.to('Asia/Kuala_Lumpur').format('YYYY-MM-DD'),
        })
        # subprocess.Popen("/home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf", stdin=subprocess.PIPE)
        # for windows #
        # os.startfile("/home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf", "print")
        # for pi #
        os.system("lpr -P Printer_Name /home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf")

    def buttonbusiness(self):
        self.btn_clicks += 1
        fb = firebase.FirebaseApplication('https://rasppiqueuems.firebaseio.com/')

        varDate = arrow.now('Asia/Kuala_Lumpur').format('YYYY-MM-DD')

        date = '/' + varDate
        qnum = str(self.btn_clicks)
        queue = '/' + qnum
        utc = arrow.utcnow()

        # QR Code Content
        qrcontent = varDate + '|' + qnum
        qc = pyqrcode.create(qrcontent)
        qc.png('toPrint/qc.png', scale=8)
        # print(qc.terminal(quiet_zone=1))

        pdf = FPDF(orientation='P', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=20)

        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        path = 'toPrint/qc.png'
        imgDoc.drawImage(path, 150, 490)
        imgDoc.save()

        pdf.cell(200, 10, txt="Queue Ticket", ln=1, align="C")
        pdf.image('toPrint/qc.png', 93, 20, 33)
        pdf.cell(198, 80, qnum, 0, 1, 'C')
        pdf.cell(198, -50, txt="Counter 8", ln=1, align="C")
        pdf.output("toPrint/ticketPrint.pdf")

        fb.put('', '/queues' + date + queue, {
            "QNum": qnum,
            "Status": "Pending",
            "Service": "Business",
            "Time": utc.to('Asia/Kuala_Lumpur').format('HH:mm:ss'),
            "TDate": utc.to('Asia/Kuala_Lumpur').format('YYYY-MM-DD'),
        })
        # subprocess.Popen("/home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf", stdin=subprocess.PIPE)
        # for windows #
        # os.startfile("/home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf", "print")
        # for pi #
        os.system("lpr -P Printer_Name /home/pi/PycharmProjects/piQueue/toPrint/ticketPrint.pdf")

top = Tk()
top.title("Queue World!")
top.geometry("350x310")

app = Application(top)
app.mainloop()
