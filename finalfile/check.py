root.title('Parking Management System') #title of window
root.geometry("600x300")  #size of window
root.configure(background="#f9d5d5")
root.wm_iconbitmap('iconn.ico')
root.propagate()
root.resizable(0,0)



#Label
fnt=('Times', 20, 'bold italic')
Mylabel= Label(root, text="Welcome to Parking Management System", bg="#f9d5d5", fg="black", font=fnt) #simply shows the text
Mylabel.grid(row=1, columnspan=5, padx=60, pady=40) #making text stable
#button
logbutton= Button(root, text="Click here to login", relief=FLAT, bg="orange",fg="white", font= "none 11 bold",command=Login)
regbutton= Button(root, text="New ? Register Here.", relief=FLAT, bg="green",fg="white", font= "none 11 bold",command=onRegister)
chkbutton= Button(root, text="Check Availability for parking", relief=FLAT, bg="blue",fg="white", font= "none 11 bold",command=lambda:availability(0))
qutbutton= Button(root, text="Quit", relief=GROOVE, bg="red",fg="white", font= "none 11 bold", command=quit)

#making button stable
logbutton.grid(row=2, column=1, padx=5, pady=20)
regbutton.grid(row=2, column=2, padx=5, pady=20)
chkbutton.grid(row=2, column=3, padx=2, pady=20)
qutbutton.grid(row=3, column=2)

#making window stable
root.mainloop()