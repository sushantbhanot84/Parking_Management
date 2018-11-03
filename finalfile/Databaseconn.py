import sqlite3
conn=sqlite3.connect('test.db')

l1=["drop table User_details","drop table Check_avail"]

print('opened database successfully')

print('done')
class A:

    def __init__(self):
        conn = sqlite3.connect('test.db')

    def establish(self):

        conn.execute('''create table User_detail(Name varchar(20),Password varchar(10),Reg_No int PRIMARY key , Hostel_No int,Mobile_no int(20),Emailid varchar(30),Parking_Alloted int )''')
        # conn.execute("insert into db values ('rajan',64,11807118)");
        # conn.execute("insert into db values ('manhart',12,11803425)");
        # conn.execute("insert into db values ('Akhil',63,11806970)");
        conn.execute('''create table Check_avail(Block varchar(20),car_avail int,Cycle_avail int, Bike int)''')
        conn.commit()
    def drop(self,x):
        conn.execute(l1[x])
        print(l1[x],' query executed')
        conn.commit()
    def look_for_data(self,var):
        db1 = conn.execute("Select * from "+var)        #var1 is the table name
        for data in db1:
            print(data)
        conn.commit()
    def insert(self):
        pass
        # conn.execute('''create table Check_avail(Block varchar(20),car_avail int,Cycle_avail int, Bike int)''')
        # conn.execute("insert into Check_avail values('block57',40,27,15)")
        # conn.execute("insert into Check_avail values('block30',50,18,21)")
        # conn.execute("insert into Check_avail values('Hospital',15,12,7)")4
        #conn.execute("insert into User_detail values('rajan','Male',11807118,4,9888249609,'rajan@gmail.com','block30')")

        #conn.execute('''create table parking_confirm(Reg_No int,Confirmation varchar(10),block_name varchar (20))''')
        #conn.commit()
    # def check_parking(self,dbname,vehicle):
    #     num=conn.execute("select parking_left from "+dbname+" where vehicle_type=?",(vehicle,))
    #     for a in num:
    #         print()
    #     a=int(a[0])
    #     print(a)
    #     if a>0:
    #         print(a," parkings available")
    #
    #
    #     else:
    #         print('sorry no parking available')

c=A()

#c.establish()
#c.insert()
#conn.execute("Alter table User_details add column Confirmation varchar(5)")
c.look_for_data('User_detail')
#c.drop(1)      #DROP 0 for db, 1 for block30 and 2 for block57
conn.close()
