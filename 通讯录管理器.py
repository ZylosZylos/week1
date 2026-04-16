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
                          
#include <stdio.h>
#include <string.h>
#include <time.h>    // 核心头文件
#include <stdlib.h>

void func_A();
void func_B();
void func_C(int internal, int duration);

int main(int argc, char *argv[])
{
    char c1, c2;
    int internal, duration;

    if(argc == 1)
    {
        func_A();
        return 0;
    }

    if(argc > 1)
    {
        sscanf(argv[1], "%c%c", &c1, &c2);
        if(c1 != '-') return 0;
        
        if(c2 == 's')
        {
            func_B();
            return 0;
        }

        if(c2 == 'l')
        {
            if(argc < 4) return 0;
            internal = atoi(argv[2]);
            duration = atoi(argv[3]);
            // 将参数传入 func_C
            func_C(internal, duration);
            return 0;
        }
    }
    return 0;
}

void func_A() {
    printf("\n1. CPU类型及型号、Linux内核版本号\n");
    system("printf \"CPU类型及型号: \"; cat /proc/cpuinfo | grep 'model name' | head -n 1 | cut -d ':' -f 2");
    system("printf \"内核版本: \"; cat /proc/version");
}

void func_B() {
    printf("\n2. 系统启动时间、进程数等\n");
    system("printf \"系统最后启动时间为: \"; uptime -s");
    system("printf \"系统运行时间: \"; uptime -p");
    system("grep 'processes' /proc/stat | awk '{print \"从系统启动开始创建的进程数: \"$2}'");
}

void func_C(int internal, int duration) {
    printf("\n3. 内存及平均负载监控\n");
    system("grep 'MemTotal' /proc/meminfo | awk '{print \"计算机配置的内存数量: \"$2}'");
    system("grep 'MemAvailable' /proc/meminfo | awk '{print \"当前可用的内存数量: \"$2}'");
    printf("平均负载列表 (每 %d 秒采样一次，总计 %d 秒):\n", internal, duration);

    time_t start_time = time(NULL); // 记录整个监控开始的时间
    time_t last_sample_time = 0;    // 记录上一次打印的时间

    // 循环：只要当前时间 - 开始时间 < 总持续时间，就继续
    while (time(NULL) - start_time < duration) {
        time_t current_time = time(NULL);

        // 如果当前时间 - 上次采样时间 >= 我们设置的间隔（internal）
        // 或者这是第一次采样（last_sample_time == 0）
        if (current_time - last_sample_time >= internal) {
            system("cat /proc/loadavg | cut -d ' ' -f 1"); // 打印负载
            last_sample_time = current_time;               // 更新采样时间
        }
        
        // 注意：这里没有 sleep，CPU 会在这里拼命循环检查时间
    }
    printf("监控结束。\n");
}

             
              
        

           
           

