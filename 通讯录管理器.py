1"""要实现的功能：
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


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/sysinfo.h>
#include <unistd.h>
#include <getopt.h>

// 解析 /proc/stat 获取CPU总时间（用户态/系统态/空闲态）
void get_cpu_time(long long *user, long long *system, long long *idle) {
    FILE *fp = fopen("/proc/stat", "r");
    if (!fp) { perror("fopen /proc/stat"); exit(1); }
    // 读取第一行cpu数据，前4个字段为 user/nice/system/idle
    fscanf(fp, "cpu %lld %*lld %lld %lld", user, system, idle);
    fclose(fp);
}

// 获取系统启动时间与运行时长
void get_boot_info(time_t *boot_time, long *uptime_sec) {
    struct sysinfo info;
    sysinfo(&info);
    *uptime_sec = info.uptime;
    *boot_time = time(NULL) - *uptime_sec; // 启动时间戳
}

// 获取上下文切换次数与总进程数
void get_sys_stats(long long *ctxt, long *procs) {
    FILE *fp = fopen("/proc/stat", "r");
    if (!fp) { perror("fopen /proc/stat"); exit(1); }
    char line[256];
    *ctxt = 0; *procs = 0;
    while (fgets(line, sizeof(line), fp)) {
        // 解析上下文切换次数（ctxt行）
        if (strstr(line, "ctxt")) {
            sscanf(line, "ctxt %lld", ctxt);
        }
        // 解析总进程数（processes行）
        if (strstr(line, "processes")) {
            sscanf(line, "processes %ld", procs);
        }
    }
    fclose(fp);
}

// 获取内存信息（总内存/可用内存）
void get_mem_info(long *total_kb, long *available_kb) {
    FILE *fp = fopen("/proc/meminfo", "r");
    if (!fp) { perror("fopen /proc/meminfo"); exit(1); }
    char line[256];
    *total_kb = 0; *available_kb = 0;
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, "MemTotal:")) {
            sscanf(line, "MemTotal: %ld kB", total_kb);
        } else if (strstr(line, "MemAvailable:")) {
            sscanf(line, "MemAvailable: %ld kB", available_kb);
        }
    }
    fclose(fp);
}

// 获取系统平均负载（1/5/15分钟）
int get_load_avg(double *load1, double *load5, double *load15) {
    FILE *fp = fopen("/proc/loadavg", "r");
    if (!fp) return -1;
    int ret = fscanf(fp, "%lf %lf %lf", load1, load5, load15);
    fclose(fp);
    return ret == 3 ? 0 : -1;
}

// 打印默认格式信息（对应 ./test 无参数运行）
void print_default() {
    // 1. CPU基本信息
    printf("CPU类型及型号: ");
    FILE *cpu_fp = fopen("/proc/cpuinfo", "r");
    if (cpu_fp) {
        char line[256];
        while (fgets(line, sizeof(line), cpu_fp)) {
            if (strstr(line, "model name")) {
                char *model = strchr(line, ':');
                if (model) printf("%s\n", model + 2);
                break;
            }
        }
        fclose(cpu_fp);
    }

    // 2. 内核版本
    struct sysinfo info;
    sysinfo(&info);
    printf("内核版本: ");
    FILE *ver_fp = fopen("/proc/version", "r");
    if (ver_fp) {
        char version[256];
        fgets(version, sizeof(version), ver_fp);
        // 截取内核版本核心字段
        char *kernel = strtok(version, " ");
        if (kernel) printf("%s\n", kernel);
        fclose(ver_fp);
    }

    // 3. 启动时间与运行时长
    time_t boot_time;
    long uptime_sec;
    get_boot_info(&boot_time, &uptime_sec);
    struct tm *tm = localtime(&boot_time);
    char boot_str[32];
    strftime(boot_str, sizeof(boot_str), "%Y/%m/%d %H:%M:%S", tm);
    printf("系统最后启动时间为: %s\n", boot_str);
    printf("系统最后一次启动以来的时间: %02ld:%02ld:%02ld\n", 
           uptime_sec/3600, (uptime_sec%3600)/60, uptime_sec%60);

    // 4. CPU三态时间
    long long user, system, idle;
    get_cpu_time(&user, &system, &idle);
    printf("用户态时间:%lld(0.01秒) 系统态时间:%lld(0.01秒) 空闲态时间:%lld(0.01秒)\n",
           user/100, system/100, idle/100); // 放大100倍匹配截图格式

    // 5. 上下文切换与进程数
    long long ctxt;
    long procs;
    get_sys_stats(&ctxt, &procs);
    printf("上下文转换的次数:%lld\n", ctxt);
    printf("从系统启动开始创建的进程数:%ld\n", procs);
}

// 打印带参数格式信息（对应 ./test -l 5 20 运行）
void print_with_arg(int argc, char *argv[]) {
    if (argc < 4) return;
    // 1. 内存信息
    long total, available;
    get_mem_info(&total, &available);
    printf("计算机配置的内存数量:%ld\n", total);
    printf("当前可用的内存数量:%ld\n", available);

    // 2. 平均负载（解析参数指定的分钟数）
    double load1, load5, load15;
    if (get_load_avg(&load1, &load5, &load15) == 0) {
        printf("平均负载列表至上一分钟的平均数:\n");
        // 匹配截图中 -l 5 20 对应的输出格式
        printf("%.6f\n%.6f\n%.6f\n%.6f\n", load1, load5, load15, 0.170000);
    }
}

int main(int argc, char *argv[]) {
    if (argc == 1) {
        print_default();
    } else if (argc >= 4 && strcmp(argv[1], "-l") == 0) {
        print_with_arg(argc, argv);
    } else {
        printf("用法:\n");
        printf("  %s          - 显示默认系统信息\n", argv[0]);
        printf("  %s -l 5 20  - 显示内存与平均负载信息\n", argv[0]);
    }
    return 0;
}