import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import face_recognition
import cv2
import numpy as np
import os
from tkinter.messagebox import showinfo, showwarning, showerror
import shutil
import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askinteger, askfloat, askstring
import tkinter.ttk as ttk

global known_face_names
global dist
known_face_names = []
dist = {}

filename = open('name.txt', 'r')
filenae_a = filename.read()
filename_b = filenae_a.split('\n')
print(filename_b)

for i in filename_b:#防止数据中的空格成为人名，产生找不到“ ”人名找不到的错误
    if len(i) <=2:
        break
    else:
        filename_c = i.split(':')
        print(filename_c)
        dist[filename_c[0]] = filename_c[1]
        known_face_names.append(str(filename_c[0]))

print(dist)
print(known_face_names)
def known_Preservation():#把dist字典的数据写进name.txt
    filename = open('name.txt', 'w')
    for k, v in dist.items():
        filename.write(k + ':' + str(v))
        filename.write('\n')
    filename.close()

def face_data_base():#建立人脸和人脸识别，图片读取工作
    global known_face_encodings
    global face_locations
    global face_encodings
    global face_names
    known_face_encodings = []
    for name in known_face_names:
        filename = name + ".jpg"
        image = name + "_image"
        face_encoding = name + "_face_encoding"
        image = face_recognition.load_image_file(filename)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
    face_locations = []
    face_encodings = []
    face_names = []


# 主页面按键1的响应事件，，，打开摄像头进行视频人脸识别
def butter_1_program():
    face_data_base()

    showinfo(title="提示", message="此程序按q结束!")

    root.withdraw()


    video_capture = cv2.VideoCapture(0)
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    root.wm_deiconify()


# 主页面按键2的响应事件
def butter_2_program():
    showinfo(title="提示", message="按q保存图片!")
    root.withdraw()
    print('进入人脸图像识别')
    cap = cv2.VideoCapture(0)
    face_data_base()
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.imshow("Photo", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                file_name = "temporary.jpg"
                root.wm_deiconify()
                cv2.imwrite(file_name, frame)
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

    unknown_image = face_recognition.load_image_file(file_name)
    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print('没有看到人脸')
        root.wm_deiconify()
        showerror(title="错误", message="未找到人脸!")
        video_capture.release()
        cv2.destroyAllWindows()
    results = face_recognition.compare_faces(known_face_encodings, unknown_face_encoding, tolerance=0.3)
    print(results)

    for result in range(len(results)):

        if results[result] == True:
            print(known_face_names[result])
            message_add_name = "这个人是" + known_face_names[result]
            Deduction_name=known_face_names[result]
            showinfo(title="提示", message=str(message_add_name))
            account_money_change = askinteger(title="扣款", prompt="请输入消费金额：")
            account_money_change = -account_money_change
            print(account_money_change)
            money_change(Deduction_name, account_money_change)
            known_Preservation()
            print(dist)
            print('准备删除')
            showinfo(title="提示", message=str("账户余额为" + str(dist[Deduction_name])))


    if len(set(results))==1:

        showinfo(title="提示", message='不存在该账户')
        os.remove(file_name)
    root.wm_deiconify()





# 按键3带图片按键，添加人脸图片
def butter_3_program():
    root.withdraw()
    def caps(ev=None):
        face_existence = 1
        window_sign_up.withdraw()
        showinfo(title="提示", message="此程序q识别图片!")
        add_name = entry_1.get()
        if add_name in known_face_names:
            print('已经存在')
            showinfo(title="提示", message="已有此人名")
            root.wm_deiconify()
        else:
            print("正在添加文件")
            cap = cv2.VideoCapture(0)
            face_data_base()
            print(add_name)
            new_add_name = str(add_name + ".jpg")
            while True:
                ret, frame = cap.read()
                if ret:
                    cv2.imshow("Photo", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        root.wm_deiconify()
                        cv2.imwrite(new_add_name, frame)
                        break
                else:
                    break
            unknown_image = face_recognition.load_image_file(new_add_name)
            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            except IndexError:
                print('没有看到人脸')
                os.remove(new_add_name)
                showerror(title="错误", message="未找到人脸!")
                root.wm_deiconify()
                face_existence = 0

            if face_existence == 1:
                known_face_names.append(str(add_name))
                dist[str(add_name)] = str(0)
                print(dist)
                known_Preservation()
                print("保存完成")

            print(known_face_names)
            cap.release()
            cv2.destroyAllWindows()
            root.wm_deiconify()

    window_sign_up = tk.Toplevel(root)
    window_sign_up.geometry('300x200')
    window_sign_up.title('添加人脸图片')

    tk.Label(window_sign_up, text='添加的姓名：').place(x=10, y=50)
    entry_1 = tk.Entry(window_sign_up)
    entry_1.place(x=80, y=50)
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='添加', command=caps)
    window_sign_up.bind("<Return>", caps)
    btn_comfirm_sign_up.place(x=145, y=120)



def butter_4_program():#通过本地文件添加图片
    root.withdraw()
    def caps(ev=None):

        window_sign_up.withdraw()
        add_name = entry_1.get()
        if add_name in known_face_names:
            print('已经存在')
        else:
            filenames = tkinter.filedialog.askopenfilenames()
            print(filenames)
            src = str(filenames[0])
            dst = str(add_name + ".jpg")
            shutil.copyfile(src, dst)
            print('ok')
            known_face_names.append(str(add_name))
            dist[str(add_name)] = str(0)
            print(dist)
            known_Preservation()
        root.wm_deiconify()

    window_sign_up = tk.Toplevel(root)
    window_sign_up.geometry('300x200')
    window_sign_up.title('添加人脸图片')

    tk.Label(window_sign_up, text='添加的姓名：').place(x=10, y=50)
    entry_1 = tk.Entry(window_sign_up)
    entry_1.place(x=80, y=50)
    btn_comfirm_sign_up = tk.Button(window_sign_up, text='添加', command=caps)

    window_sign_up.bind("<Return>", caps)
    btn_comfirm_sign_up.place(x=145, y=120)


def butter_5_program():#添加账户金额
    root.withdraw()
    account_name = askstring(title="请输入一个姓名",prompt="充值账户：")
    if account_name in known_face_names:
        account_money_change = askinteger(title="充值",
                                          prompt="请输入充值金额：")

        money_change(account_name,account_money_change)

        print(dist[account_name])#显示充值账户还有多少余额

        showinfo(title="提示", message=str("账户余额为"+dist[account_name]))
        known_Preservation()
    else:
        showerror(title = "错误", message = "充值账户不存在!")

    root.wm_deiconify()


def form_account():#作一个账户可视化的的表格，可供用户进行查看。
    root.withdraw()

    window_form = tk.Toplevel(root)
    root.withdraw()
    window_form.geometry("500x200")
    window_form.title("人脸识别账户信息")
    tree = ttk.Treeview(window_form, columns=['余额'], selectmode="extended")
    tree.heading('余额', text='余额')
    tree.column('余额', width=100, anchor='center')# 指定第一列的宽度和名称， 如果show = "headings", 这一列就被隐藏.

    # 用递归法遍历带子字典或列表的数据
    def process_dict(d, tree, tr):
        for k, v in d.items():
            if type(v) != dict:
                if type(v[0]) == dict:
                    trr = tree.insert(tr, 'end', text=k, open=True)
                    for ls in v:
                        process_dict(ls, tree, trr)
                else:
                    tree.insert(tr, 'end', text=k, values=v)
            else:
                trr = tree.insert(tr, 'end', text=k, open=True)
                process_dict(v, tree, trr)

    process_dict(dist, tree, "")
    root.wm_deiconify()
    # y滚动条
    yscrollbar = Scrollbar(window_form, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.pack(side=RIGHT, fill=Y)
    # x滚动条
    xscroll = Scrollbar(window_form, orient=HORIZONTAL, command=tree.xview)
    tree.configure(xscrollcommand=xscroll.set)
    xscroll.pack(side=BOTTOM, fill=X)

    tree.pack(side=TOP, expand=1, fill=BOTH)

    window_form.mainloop()
    root.wm_deiconify()



def money_change(name,money):#金钱的加减name为名字，money为改变的钱数有正负之分
    s = dist[name]
    if money>0 :
        dist[name]=str(int(s)+int(money))
    else:
        negative_numbe=int(s) + int(money)
        if negative_numbe>=0:
            dist[name] = negative_numbe
        else:showerror(title = "错误", message = "账户余额不足!")

def gui_face():
    # gui框架
    global root
    root = tk.Tk()
    root.title('人脸识别')
    # gui主页面 用画布来实现
    canvas = tk.Canvas(root, width=600, height=420, bd=0, highlightthickness=0)
    imgpath_1 = "beijing.jpg"
    img_1 = Image.open(imgpath_1)
    photo_1 = ImageTk.PhotoImage(img_1)
    canvas.create_image(300, 200, image=photo_1)
    canvas.pack()
    # gui主页面中的按键

    butter_1 = tk.Button(root, text='账户充值', command=butter_5_program)
    canvas.create_window(150, 350, width=100, height=20, window=butter_1)
    butter_2 = tk.Button(root, text='图片识别', command=butter_2_program)
    canvas.create_window(450, 350, width=100, height=20, window=butter_2)

    imgpath_2 = "add.jpg"
    img_2 = Image.open(imgpath_2).resize((40, 40))
    photo_2 = ImageTk.PhotoImage(img_2)
    butter_3 = tk.Button(root, command=butter_3_program, image=photo_2)
    canvas.create_window(290, 350, width=40, height=40, window=butter_3)

    # gui主页面的顶层页面
    menubar = tk.Menu(root)

    filemenu_1 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='识别', menu=filemenu_1)
    filemenu_1.add_command(label='视频识别', command=butter_1_program)
    filemenu_1.add_command(label='图像识别', command=butter_2_program)

    filemenu_2 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='添加图片', menu=filemenu_2)
    filemenu_2.add_command(label='通过摄像头添加', command=butter_3_program)
    filemenu_2.add_command(label='本地文件添加', command=butter_4_program)

    filemenu_3 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='账户', menu=filemenu_3)
    filemenu_3.add_command(label='账户充值', command=butter_5_program)

    filemenu_4 = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='查看', menu=filemenu_4)
    filemenu_4.add_command(label='账户查看', command=form_account)

    root.config(menu=menubar)
    root.mainloop()


gui_face()
face_data_base()

