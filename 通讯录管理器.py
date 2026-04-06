"""要实现的功能：
1.添加通讯录，并且可以添加通讯录联系人的姓名、年龄、性别、电话号码等信息。
2.删除通讯录中的联系人。
3.修改通讯录中联系人的信息。
4.查询通讯录中的联系人信息。
5.按姓名查找联系人。
6.按姓名排序通讯录中的联系人。
7.保存通讯录信息到文件中。
8.从文件中加载通讯录信息。
9.退出通讯录管理器。
"""
import json
contacts = []
def sort_contacts():
    if not contacts:
        return
    else:
        contacts.sort(key = lambda contact:contact['name'])
def add_contact():
    name=input("请输入联系人的姓名：")
    number=input("请输入联系人的电话号码：")
    contacts.append({"name":name,"number":number})
    sort_contacts()
def delete_contact():
    name=input("请输入要删除联系人的姓名：")
    for contact in contacts:
        if contact["name"]==name:
            contacts.remove(contact)
            print("联系人已删除")
            return
    print("查无此人")    
def show_contacts():
    if not contacts:
        return
    for contact in contacts:
        print("姓名:"+contact['name']+"  "+"number:"+contact["number"])
        print("------------------------------")

def search_contact():
    name=input("请输入查找的联系人：")
    for contact in contacts:
        if(contact['name']==name):
          print("查找成功")
          print("姓名:"+contact['name']+"  " +"number:"+contact["number"])
          return
    print("查无此人")

def save_contacts():
    with open("contacts.json","w",encoding="utf-8") as f:
        json.dump(contacts,f,ensure_ascii=False,indent=2)

def load_contacts():
    global contacts
    with open("contacts.json",'r',encoding='utf-8') as f:
       contacts =json.load(f)
    sort_contacts()
    print("通讯录加载成功")
def main():
    while True:
        print("1.添加联系人  2.删除联系人  3.查看所有联系人  4.按姓名查找联系人  5.退出系统 6.修改联系人 7.保存联系人到文件夹 8.从文件夹里面加载联系人")
        choice = input("请选择功能对应编号：")
        if (choice == "1"):
            add_contact()
        elif (choice=='2'):
            delete_contact()
        elif (choice=='3'):
            show_contacts()
        elif (choice=='4'):
            search_contact()
        elif (choice=='5'):
            print("已退出")
            break
        elif (choice=='6'):
            edit_contact()
        elif (choice=='7'):
            save_contacts()
        elif (choice=='8'):
            load_contacts()
        else :
            print("输入无效，请重新输入")

def edit_contact():
    name=input("请输入要修改的联系人：")
    for contact in contacts:
        if(contact['name']==name):
          print("修改姓名请选：1，修改number请选：2，都要修改请选：3")
          choice=input("请选择功能编号：")
          if(choice=='1'):
            name=input("请修改姓名为：")
            contact['name']=name
            sort_contacts()
            return
          elif(choice=='2'):
              number=input("请修改number为:")
              contact['number']=number
              return
          elif (choice=='3'):
               name=input("请修改姓名为：")
               contact['name']=name
               number=input("请修改number为:")
               contact['number']=number
               sort_contacts()
               return
          else:
              print("无效输入")
              return
    print("查无此人，无法修改")
    
    
if __name__=='__main__':
   main()
                          
             
              
        

           
           

