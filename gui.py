import tkinter as tk
from tkinter.constants import YES
def start():
    def get_ac_pa():
        global ac, pa
        ac = ac_entry.get()
        pa = pa_entry.get()
        ac_entry.delete(0, "end")
        pa_entry.delete(0, "end")
        win.destroy()

    win = tk.Tk()
    win.title('抓取tronclass公告')
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

def save_page(info_dic):
    def yes():
        global check
        check = True
        win.destroy()
    def no():
        global check
        check = False
        win.destroy()

    win = tk.Tk()
    win.title('儲存tronclass公告')
    win.geometry('980x480')


    header_label = tk.Label(win, text='公告抓取完成\n「請選擇是否儲存成CSV檔？」')
    header_label.pack()

    listbox = tk.Listbox(win, width=100)
    for i in range(10):
        a = str(i+1) + "：" + info_dic["title"][i] + ", " + info_dic["class"][i] + ", " + info_dic["content"][i]
        listbox.insert('end', a)
    listbox.pack()

    yes_btn = tk.Button(win, text='YES', command=yes)
    yes_btn.pack(side=tk.LEFT, padx = 300)
    no_btn = tk.Button(win, text='NO', command=no)
    no_btn.pack(side = tk.LEFT, )


    win.mainloop() 
    return check