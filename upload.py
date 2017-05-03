from firebase import firebase
import tkinter
import arrow


firebaseURL = ""  # "your firebase url"

if __name__ == '__main__':

    def buttons():
        fb = firebase.FirebaseApplication(firebaseURL, None)

        varDate = arrow.now('Asia/Kuala_Lumpur').format('YYYY-MM-DD')
        varUnix = arrow.now('Asia/Kuala_Lumpur').format('X')

        date = '/' + varDate
        unix = '/' + varUnix
        utc = arrow.utcnow()
        fb.post('/queuetest' + date + unix, {
            "Time": utc.to('Asia/Kuala_Lumpur').format('HH:mm:ss'),
            "Queue Number": '1234'
        })

top = tkinter.Tk()
top.title("Queue World!")
top.geometry("300x190")

button1 = tkinter.Button(top, text="Normal Transaction", command=buttons)
button1.place(x=90, y=40)

button2 = tkinter.Button(top, text="Special Transaction", command=buttons)
button2.place(x=90, y=110)
top.mainloop()
