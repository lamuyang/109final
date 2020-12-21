import tkinter as tk
def start():
    def get_ac_pa():
        global ac, pa
        ac = ac_entry.get()
        pa = pa_entry.get()
        ac_entry.delete(0, "end")
        pa_entry.delete(0, "end")
        win.destroy()

    win = tk.Tk()
    win.title('BMI App')
    win.geometry('640x480')

    header_label = tk.Label(win, text='請輸入LDAP帳號密碼')
    header_label.pack()


    ac_frame = tk.Frame(win)
    ac_frame.pack(side=tk.TOP)
    ac_label = tk.Label(ac_frame, text='帳號')
    ac_label.pack(side=tk.LEFT)
    ac_entry = tk.Entry(ac_frame)
    ac_entry.pack(side=tk.LEFT)

    pa_frame = tk.Frame(win)
    pa_frame.pack(side=tk.TOP)
    pa_label = tk.Label(pa_frame, text='密碼')
    pa_label.pack(side=tk.LEFT)
    pa_entry = tk.Entry(pa_frame, show="*")
    pa_entry.pack(side=tk.LEFT)

    result_label = tk.Label(win)
    result_label.pack()

    send_btn = tk.Button(win, text='送出', command=get_ac_pa)
    send_btn.pack()
    win.mainloop()  
    return ac, pa