from firebase import firebase
import tkinter as tk
from tkinter import *
import arrow
import pyqrcode
from pyfpdf.fpdf import FPDF
from PDF import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os
from io import StringIO

# from pyPdf import PdfFileWriter, PdfFileReader
import png
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import pyfpdf
import fpdf
from collections import deque
import requests
import json

#
#
# def buttons(i):
#     i += 1
#     fb = firebase.FirebaseApplication('https://firebaseio.com/')
#
#     varDate = arrow.now('Asia/Kuala_Lumpur').format('YYYY-MM-DD')
#
#     date = '/' + varDate
#     utc = arrow.utcnow()
#     fb.put('', '/queuetest' + date, {
#         "Time": utc.to('Asia/Kuala_Lumpur').format('HH:mm:ss'),
#         "Queue Number": i
#     })
#
# i = 2000
# top = tkinter.Tk()
# top.title("Queue World!")
# top.geometry("300x190")
#
# button1 = tkinter.Button(top, text="Normal Transaction", command=lambda: buttons(i))
# button1.place(x=90, y=40)
#
# button2 = tkinter.Button(top, text="Special Transaction", command=lambda: buttons(i))
# button2.place(x=90, y=110)
# top.mainloop()
# tk widget placement


class Application(tk.Frame):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.btn_clicks = 1999
        self.create_widget()

    def create_widget(self):
        self.button1 = tk.Button(self, text="Normal Transaction", bg="blue", fg="white", command=self.buttons)
        # self.button1.grid(row=1, column=1)
        # self.button1.place(x=0, y=0)
        self.button1.pack(padx=100, pady=80)

        self.button2 = tk.Button(self, text="Special Transaction", bg="red", fg="white", command=self.buttons)
        # self.button1.grid(row=3, column=3)
        # self.button2.place(x=0, y=0)
        self.button2.pack(padx=100, pady=0)

    def buttons(self):
        self.btn_clicks += 1
        fb = firebase.FirebaseApplication('https://.firebaseio.com/')

        varDate = arrow.now('Asia/Kuala_Lumpur').format('YYYY-MM-DD')
        # varTime = arrow.now('Asia/Kuala_Lumpur').format('HH:mm:ss')

        date = '/' + varDate
        qnum = str(self.btn_clicks)
        queue = '/' + qnum
        utc = arrow.utcnow()

        # QR Code Content
        qrcontent = varDate + '|' + qnum
        qc = pyqrcode.create(qrcontent)
        # qc.svg('toPrint/qc.svg', scale=10)
        # qc.eps('toPrint/qc.eps', scale=10)
        qc.png('toPrint/qc.png', scale=8)
        # print(qc.terminal(quiet_zone=1))

        pdf = FPDF(orientation='P', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=20)
        # pdf.cell(200, 10, txt=qnum + "\n\n" + qc.png, align="C")
        pdf.cell(190, 10, txt="Queue Ticket", ln=1, align="C")
        pdf.cell(190, 220, qnum, 0, 1, 'C')
        pdf.output("toPrint/ticketPrint.pdf")

        path = 'toPrint/qc.png'
        pdf2 = PdfFileWriter()
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=A4)
        # imgPath = "toPrint/qc.png"
        imgDoc.drawImage(path, 150, 490)
        imgDoc.save()

        page = PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0)
        pdf2.addPage(page)
        pdf2.write(open("toPrint/ticketPrint2.pdf", "wb"))

        fb.put('', '/queues' + date + queue, {
            "Time": utc.to('Asia/Kuala_Lumpur').format('HH:mm:ss'),
            # "Queue Number": self.btn_clicks
        })

        os.startfile("C://", "print")


top = Tk()
top.title("Queue World!")
top.geometry("310x310")

app = Application(top)
app.mainloop()
