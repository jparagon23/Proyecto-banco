from sqlite3.dbapi2 import IntegrityError
from tkinter import ttk
from tkinter import *
import sqlite3
import os
from tkinter import font
import tkinter
from PIL import ImageTk,Image
from datetime import datetime

class Bank:
    def __init__(self,window):
        self.window=window
        #import the image

        self.img=Image.open('descarga.jpg')
        self.img=self.img.resize((180,180)) #we change the size of the image 
        self.img=ImageTk.PhotoImage(self.img)
        self.date=datetime.now()

        #Create labels
        Label(self.window,text='Custom Banking Beta',font=('Calibri',14)).grid(row=0,sticky=N,pady=10) #sticky means in the middle
        Label(self.window,text="The most secure bank you've probably used",font=('Calibri',12)).grid(row=1,sticky=N) 
        Label(self.window,image=self.img).grid(row=1,sticky=N,pady=30) #pady is the distance between rows 

        #we need buttons
        Button(self.window,text='Register', font=('calibri',12),command=lambda:self.registro(),width=15).grid(row=3,sticky=N)
        Button(self.window,text='Login', font=('calibri',12),command=lambda:self.login(),width=15).grid(row=4,sticky=N,pady=10)
    
    def run_query(self,query,parameters=()):
        db_name='database.db'
        with sqlite3.connect(db_name) as conn:
            cursor= conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result
   
    def registro(self):

        self.register_screen=Toplevel(self.window)
        self.register_screen.title('Register')

        #we create de labels ( information )

        Label(self.register_screen,text='Please enter your details bellow to register').grid(row=0,sticky=N,columnspan=2,pady=10)
        
        Label(self.register_screen,text='Id',font=('calibri',12)).grid(row=1,sticky=W)
        Label(self.register_screen,text='Name',font=('calibri',12)).grid(row=2,sticky=W)
        Label(self.register_screen,text='Age',font=('calibri',12)).grid(row=3,sticky=W)

        Label(self.register_screen,text='Gender',font=('calibri',12)).grid(row=4,sticky=W)
        
        Label(self.register_screen,text='Username',font=('calibri',12)).grid(row=5,sticky=W) #to the west, meaning left part
        Label(self.register_screen,text='Password',font=('calibri',12)).grid(row=6,sticky=W)
        #notification
        self.reg_notif=Label(self.register_screen,font=('calibri',12),text='',fg='red') # aqui es donde iran las notificaciones 
        self.reg_notif.grid(row=8,sticky=N, columnspan=2)

        #now we are going to configure the entry 
        self.register_id=Entry(self.register_screen)
        self.register_id.focus() 
        self.register_id.grid(row=1,column=1)
        self.register_name=Entry(self.register_screen)
        self.register_name.grid(row=2,column=1)
        self.register_age=Entry(self.register_screen)
        self.register_age.grid(row=3,column=1)
        #with gender we are going to try roundbutton
        self.pre_gender=StringVar()
        var_ger=Radiobutton(self.register_screen,variable=self.pre_gender,text="Male",  value='male')
        var_ger.select()
        var_ger.grid(row=4,column=1,sticky=W)
        var_ger2=Radiobutton(self.register_screen,variable=self.pre_gender,text="Female",  value='female')
        var_ger2.grid(row=4,column=1,sticky=E)
        
        # self.register_gender=Entry(self.register_screen)
        # self.register_gender.grid(row=3,column=1)

        self.register_uname=Entry(self.register_screen)
        self.register_uname.grid(row=5,column=1)
        self.register_password=Entry(self.register_screen,show='*')
        self.register_password.grid(row=6,column=1)

        #here we configure the BOTTOMS
        Button(self.register_screen,text='Register',font='Calibry 12',command=lambda:self.finish_reg()).grid(row=7,columnspan=2,sticky=N)
    
    def finish_reg(self):
        self.register_gender=self.pre_gender
        self.reg_notif['text']=''
        #first we need to validate that there is not n/a spaces 

        if self.register_id.get()=='' or self.register_name.get()=='' or self.register_uname.get()=='' or self.register_gender.get()=='' or self.register_age.get()=='' or self.register_password.get()=='':
            self.notif['text']='Please introduce the required fields'
            return
        #!ojo,verificar lo del id, esta pendinte 
        try:
            query='INSERT INTO user_info VALUES(NULL,?,?,?,?,?,?)'
            parameters=(self.register_id.get(),self.register_uname.get(),self.register_password.get(),self.register_name.get(),self.register_gender.get(),self.register_age.get())
            self.run_query(query,parameters)
            #aqui se va a crear el balance
            query='INSERT INTO balance VALUES(NULL,?,?)'
            parameters=(self.register_id.get(),'0')
            self.run_query(query,parameters)
            self.reg_notif['text']='The user has been created'
        except IntegrityError:
            self.reg_notif['text']='The Id or the user already exist, please try again'
    
    def login(self):

        #login_screen
        self.login_screen=Toplevel(self.window)
        self.login_screen.title('Login')

        Label(self.login_screen,text='Login to your account',font=('calibri',12)).grid(row=0,sticky=N,pady=5)

        Label(self.login_screen,text='Username',font=('calibri',12)).grid(row=1,sticky=W)
        Label(self.login_screen,text='Password',font=('calibri',12)).grid(row=2,sticky=W)
        self.login_notif=Label(self.login_screen,font=('calibri',12),text='',fg='red')
        self.login_notif.grid(row=4,columnspan=2,sticky=N)

        #Entry 
        self.login_uname=Entry(self.login_screen)
        self.login_uname.focus()
        self.login_uname.grid(row=1,column=1,padx=2)
        self.login_password=Entry(self.login_screen,show='*')
        self.login_password.grid(row=2,column=1,padx=2)

        #button

        Button(self.login_screen,text='Login',width=15,font=('Calibri',12),command=lambda:self.login_session()).grid(row=3,sticky=N,columnspan=2)
        
    def login_session(self):
        
        #mirar si el usuario existe 
        query_login='SELECT * FROM user_info where user_uname=?'
        parameters_login=((self.login_uname.get(),))
        self.data_info=self.run_query(query_login,parameters_login)

        for db_info in self.data_info:
            self.info_password=db_info[3]
            self.info_uname=db_info[2]
            self.info_account_id=db_info[1]
            self.info_name=db_info[4]
            self.info_gender=db_info[5]
            self.info_age=db_info[6]
            self.info_account=db_info[0]

            if self.login_uname.get()==self.info_uname and self.login_password.get()==self.info_password:
            
                
                self.login_screen.destroy()
                self.account_dashboard=Toplevel(self.window)
                self.account_dashboard.title ('Dashboard')
                #labels de la pantalla 

                Label(self.account_dashboard,text='Account Dashboard',font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(self.account_dashboard,text='welcome '+ db_info[4],font=('Calibri',12)).grid(row=1,sticky=N,pady=5)

                #buttons
                Button(self.account_dashboard,text='Personal Details',font=('Calibri',12),width=30,command=lambda:self.personal_details()).grid(row=2,sticky=N,padx=10)
                Button(self.account_dashboard,text='Deposit',font=('Calibri',12),width=30,command=lambda:self.deposit()).grid(row=3,sticky=N,padx=10)
                Button(self.account_dashboard,text='Withdraw',font=('Calibri',12),width=30,command=lambda:self.withdraw()).grid(row=4,sticky=N,padx=10)
                Button(self.account_dashboard,text='Transaction',font=('Calibri',12),width=30,command=lambda:self.transaction()).grid(row=5,sticky=N,padx=10)
                
                Label(self.account_dashboard).grid(row=6,sticky=N,pady=10)

                self.inicial_login_balance=self.cal_balance(str(self.info_account_id))

                return
            else:
                self.login_uname.delete(0,END)
                self.login_password.delete(0,END)
                self.login_uname.focus()

                self.login_notif['text']='The user or the password is wrong'

    def personal_details(self):
        self.initial_personal_balance=self.cal_balance(self.info_account_id)

        personal_details_screen=Toplevel(self.window)
        personal_details_screen.title('Personal Details')
        #labels

        Label(personal_details_screen,text='Personal details ', font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
        Label(personal_details_screen,text='Id: '+ str(self.info_account_id), font=('Calibri',12)).grid(row=1,sticky=W)
        Label(personal_details_screen,text='Name: '+ str(self.info_name), font=('Calibri',12)).grid(row=2,sticky=W)
        Label(personal_details_screen,text='Age: '+ str(self.info_age), font=('Calibri',12)).grid(row=3,sticky=W)
        Label(personal_details_screen,text='Gender: '+ str(self.info_gender), font=('Calibri',12)).grid(row=4,sticky=W)
        Label(personal_details_screen,text='Balance: $'+ str(self.initial_personal_balance), font=('Calibri',12)).grid(row=4,sticky=W)

    def deposit (self):
        self.inicial_deposit_balance=self.cal_balance(str(self.info_account_id))
        self.details_balance=0
        self.deposit_screen=Toplevel(self.window)
        self.deposit_screen.title('Deposit')

        Label(self.deposit_screen,text='Deposit',font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
        Label(self.deposit_screen,text='Current balance: ',font=('Calibri',12)).grid(row=1,sticky=N,pady=10)
        Label(self.deposit_screen,text='$' + str(self.inicial_deposit_balance),font=('Calibri',12)).grid(row=1,column=1,sticky=N,pady=10)
        
        Label(self.deposit_screen,text='Amount',font=('Calibri',12)).grid(row=2,sticky=W,pady=10)
        self.deposit_notif=Label(self.deposit_screen, font=('calibri',12),text='',fg='red')
        self.deposit_notif.grid(row=4,sticky=N, columnspan=2)
        # entry
        self.deposit_amount=Entry(self.deposit_screen)
        self.deposit_amount.grid(row=2,column=1)
        # button
        Button(self.deposit_screen,text='Deposit',font=('Calibri',12),command=lambda:self.finish_deposit()).grid(row=3,columnspan=2,sticky=N)

    def finish_deposit(self):

        if self.deposit_amount.get() == '':
            self.deposit_notif['text']="Please introduce the amount"
            return
        
        try:
            #insertar la transaccion en la tabla para registro}
            query='INSERT INTO deposit VALUES(NULL,?,?,?)'
            parameters=(str(self.info_account_id),str(self.deposit_amount.get()),str(self.date),)
            self.run_query(query,parameters)

            # cambiar el balance 
            self.deposit_balance=self.cal_balance(self.info_account_id)
            new_balance=int(self.deposit_balance)+int(self.deposit_amount.get())

            query='UPDATE balance SET balance=? where account=?'
            parameters=(str(new_balance),str(self.info_account_id),)
            self.run_query(query,parameters)

            self.deposit_screen.destroy()
            self.deposit_message=Toplevel(self.window)
            self.deposit_message.title('Deposit')

            Label(self.deposit_message,text='The deposit has been made').grid(row=0,columnspan=2,sticky=N)
            Label(self.deposit_message,text='Your Balance is: ').grid(row=2,sticky=E)
            Label(self.deposit_message,text='$'+str(new_balance)).grid(row=2,column=1,sticky=E)

        except:
            self.deposit_notif['text']="cant make the deposit at this moment"

    def withdraw (self):
        self.details_balance=0
        self.initial_withdraw_balance=self.cal_balance(self.info_account_id)
        self.withdraw_screen=Toplevel(self.window)
        self.withdraw_screen.title('Withdraw')

        Label(self.withdraw_screen,text='Withdraw',font=('Calibri',12)).grid(row=0,columnspan=2,sticky=N,pady=10)
        Label(self.withdraw_screen,text='Current balance: ',font=('Calibri',12)).grid(row=1,sticky=N,pady=10)
        Label(self.withdraw_screen,text=str(self.initial_withdraw_balance),font=('Calibri',12)).grid(row=1,column=1,sticky=N,pady=10)

        Label(self.withdraw_screen,text='Amount',font=('Calibri',12)).grid(row=2,sticky=N,pady=10)
        self.withdraw_notif=Label(self.withdraw_screen, font=('calibri',12),text='',fg='red')
        self.withdraw_notif.grid(row=4,columnspan=2,sticky=N)
        # entry
        self.withdraw_amount=Entry(self.withdraw_screen)
        self.withdraw_amount.grid(row=2,column=1)
        # button
        Button(self.withdraw_screen,text='Withdraw',font=('Calibri',12),command=lambda:self.finish_withdraw()).grid(row=3,columnspan=2,sticky=N,pady=5)
    
    def finish_withdraw(self):

        if self.withdraw_amount.get() == '':

            self.withdraw_notif['text']="Please introduce the amount"
            return
        
        if int(self.withdraw_amount.get())>int(self.initial_withdraw_balance):
            self.withdraw_notif['text']="The amount is not valid"
            return
        
        try:
            #insertar la transaccion en la tabla para registro}
            query='INSERT INTO withdraw VALUES(NULL,?,?,?)'
            parameters=(str(self.info_account_id),str(self.withdraw_amount.get()),str(self.date),)
            self.run_query(query,parameters)

            # cambiar el balance 
            self.withdraw_balance=self.cal_balance(self.info_account_id)
            new_balance=int(self.withdraw_balance)-int(self.withdraw_amount.get())

            query='UPDATE balance SET balance=? where account=?'
            parameters=(str(new_balance),str(self.info_account_id),)
            self.run_query(query,parameters)

            self.withdraw_screen.destroy()
            self.withdraw_message=Toplevel(self.window)
            self.withdraw_message.title('Deposit')

            Label(self.withdraw_message,text='The withdraw has been made').grid(row=0,columnspan=2,sticky=N)
            Label(self.withdraw_message,text='Your Balance is: ').grid(row=2,sticky=E)
            Label(self.withdraw_message,text='$'+str(new_balance)).grid(row=2,column=1,sticky=E)

        except:
            self.deposit_notif['text']="cant make the withdraw at this moment"

    def transaction (self):
        self.transaction_inicial_balance_i=self.cal_balance(str(self.info_account_id),)

        balance_prov=0
        self.transaction_screen=Toplevel(self.window)
        self.transaction_screen.title('Transaction')

        #labels

        Label(self.transaction_screen,text='Your account number: ', font=('Calibri',12)).grid(row=0,sticky=N)
        Label(self.transaction_screen,text='Your Balance is:  ', font=('Calibri',12)).grid(row=1,sticky=N)
        Label(self.transaction_screen,text='$' + str(self.transaction_inicial_balance_i), font=('Calibri',12)).grid(row=1,column=1,sticky=N)
        
        Label(self.transaction_screen,text='Account number to tranfer: ', font=('Calibri',12)).grid(row=2,sticky=W)
        Label(self.transaction_screen,text='Amount to tranfer: ', font=('Calibri',12)).grid(row=3,sticky=W)
        Label(self.transaction_screen,text='Message: ', font=('Calibri',12)).grid(row=4,columnspan= 2)
        
        Label(self.transaction_screen,text=str(self.info_account_id)).grid(row=0,column=1)
        self.transaction_jaccount=Entry(self.transaction_screen)
        self.transaction_jaccount.grid(row=2,column=1)
        self.transaction_amount=Entry(self.transaction_screen)
        self.transaction_amount.grid(row=3,column=1)
        self.transaction_message=Entry(self.transaction_screen)
        self.transaction_message.grid(row=5,columnspan=2, ipadx=10,ipady=10)

        #bottom
        Button(self.transaction_screen,text='Send',font=('Calibri',12),command=lambda:self.transaction_finish()).grid(row=6,columnspan=2)
        #notificacion
        self.reg_notif=Label(self.transaction_screen,font=('calibri',12),text='',fg='red') # aqui es donde iran las notificaciones 
        self.reg_notif.grid(row=7,sticky=N, columnspan=2)
    def transaction_finish(self):
        # Validar que la información de la ventana no este vacia
        if self.transaction_jaccount.get()=='' or self.transaction_amount=='':
            self.reg_notif['text']='Please introduce the require fileds'
            return
        #Validar si la cuenta a depositar existe
        condicional=False
        query_login='SELECT * FROM user_info where user_id=?'
        parameters_login=((self.transaction_jaccount.get(),))
        self.data_info=self.run_query(query_login,parameters_login)

        for db_info in self.data_info:
            condicional=True
            self.transaction_jaccount_query=db_info[0]
        #traigo el balance de la cuenta j
        self.transaction_inicial_balance_j=self.cal_balance(str(self.transaction_jaccount.get()),)

        if int(self.transaction_amount.get())>self.transaction_inicial_balance_i:
            self.reg_notif['text']='The amount is not valid'
            self.transaction_jaccount.delete(0,END)
            self.transaction_amount.delete(0,END)
            self.transaction_jaccount.focus()
            return
        if condicional==True:
            try:
                query='INSERT INTO transactions VALUES(NULL,?,?,?,?,?)'
                parameters=(self.info_account_id,self.transaction_jaccount.get(),self.transaction_amount.get(),self.transaction_message.get(),self.date)
                self.run_query(query,parameters)

                #tenemos que disminuir el balance de la cuenta i 
                #1 tenemos que traer el valor del balance 
                new_balance_i=int(self.transaction_inicial_balance_i) - int(self.transaction_amount.get())
                new_balance_j=int(self.transaction_inicial_balance_j)+ int(self.transaction_amount.get())
                #tenemos que disminuir el balance de la cuenta i 
                query='UPDATE balance SET balance=? where account=?'
                parameters=(str(new_balance_i),str(self.info_account_id),)
                self.run_query(query,parameters)

                #tenemos que aumentar el balance de la cuenta j 
                query='UPDATE balance SET balance=? where account=?'
                parameters=(str(new_balance_j),str(self.transaction_jaccount.get()),)
                self.run_query(query,parameters)


                self.transaction_screen.destroy()
                self.transaccion_finish_screen=Toplevel(self.window)
                self.transaccion_finish_screen.title ('Message')
                Label(self.transaccion_finish_screen,font=('calibri',12),text='The transaction has been made').grid(row=1,column=0,sticky=N) # aqui es donde iran las notificaciones 
                Label(self.transaccion_finish_screen,font=('calibri',12),text='Your balance is: ').grid(row=2,column=0,sticky=N) # aqui es donde iran las notificaciones 
                Label(self.transaccion_finish_screen,font=('calibri',12),text=str(new_balance_i)).grid(row=2,column=1,sticky=N) # aqui es donde iran las notificaciones 

            
            except:
                self.reg_notif['text']="The transaction can't be made in this moment, please try latter"
        else:
            self.reg_notif['text']='the account to transfer, doesnt exist'
            return








    def cal_balance(self,account):
        query_login="SELECT * FROM balance where account=?"
        parameters_login=((account,))
        self.data_info=self.run_query(query_login,parameters_login)
        for db_info in self.data_info:
            balance_=db_info[2]
            return(balance_)
         



if __name__=='__main__':
    window=Tk()
    application=Bank(window)
    window.mainloop()
