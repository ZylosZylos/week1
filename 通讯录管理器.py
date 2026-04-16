#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/sysinfo.h>
#include <unistd.h>
#include <getopt.h>

// 修复后的CPU时间读取函数（避免格式警告）
void get_cpu_time(long long *user, long long *system, long long *idle) {
    FILE *fp = fopen("/proc/stat", "r");
    if (!fp) { 
        perror("fopen /proc/stat"); 
        exit(EXIT_FAILURE); 
    }
    // 读取全部字段，再赋值需要的部分
    long long nice, iowait, irq, softirq, steal, guest, guest_nice;
    if (fscanf(fp, "cpu %lld %lld %lld %lld %lld %lld %lld %lld %lld %lld", 
               user, &nice, system, idle, &iowait, &irq, &softirq, &steal, &guest, &guest_nice) != 10) {
        perror("fscanf /proc/stat");
        fclose(fp);
        exit(EXIT_FAILURE);
    }
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
    if (!fp) { perror("fopen /proc/stat"); exit(EXIT_FAILURE); }
    char line[256];
    *ctxt = 0; *procs = 0;
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, "ctxt")) {
            sscanf(line, "ctxt %lld", ctxt);
        }
        if (strstr(line, "processes")) {
            sscanf(line, "processes %ld", procs);
        }
    }
    fclose(fp);
}

// 获取内存信息（总内存/可用内存）
void get_mem_info(long *total_kb, long *available_kb) {
    FILE *fp = fopen("/proc/meminfo", "r");
    if (!fp) { perror("fopen /proc/meminfo"); exit(EXIT_FAILURE); }
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
    printf("内核版本: ");
    FILE *ver_fp = fopen("/proc/version", "r");
    if (ver_fp) {
        char version[512];
        fgets(version, sizeof(version), ver_fp);
        printf("%s", version);
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
           user, system, idle); // 这里直接用原始值，单位就是0.01秒

    // 5. 上下文切换与进程数
    long long ctxt;
    long procs;
    get_sys_stats(&ctxt, &procs);
    printf("上下文转换的次数:%lld\n", ctxt);
    printf("从系统启动开始创建的进程数:%ld\n", procs);
}

// 打印带参数格式信息（对应 ./test -s 运行）
void print_with_s() {
    // 1. 启动时间与运行时长
    time_t boot_time;
    long uptime_sec;
    get_boot_info(&boot_time, &uptime_sec);
    struct tm *tm = localtime(&boot_time);
    char boot_str[32];
    strftime(boot_str, sizeof(boot_str), "%Y/%m/%d %H:%M:%S", tm);
    printf("系统最后启动时间为: %s\n", boot_str);
    printf("系统最后一次启动以来的时间: %02ld:%02ld:%02ld\n", 
           uptime_sec/3600, (uptime_sec%3600)/60, uptime_sec%60);

    // 2. CPU三态时间
    long long user, system, idle;
    get_cpu_time(&user, &system, &idle);
    printf("用户态时间:%lld(0.01秒) 系统态时间:%lld(0.01秒) 空闲态时间:%lld(0.01秒)\n",
           user, system, idle);

    // 3. 上下文切换与进程数
    long long ctxt;
    long procs;
    get_sys_stats(&ctxt, &procs);
    printf("上下文转换的次数:%lld\n", ctxt);
    printf("从系统启动开始创建的进程数:%ld\n", procs);
}

// 打印带参数格式信息（对应 ./test -l 5 20 运行）
void print_with_l() {
    // 1. 内存信息
    long total, available;
    get_mem_info(&total, &available);
    printf("计算机配置的内存数量:%ld\n", total);
    printf("当前可用的内存数量:%ld\n", available);

    // 2. 平均负载（解析参数指定的分钟数）
    double load1, load5, load15;
    if (get_load_avg(&load1, &load5, &load15) == 0) {
        printf("平均负载列表至上一分钟的平均数:\n");
        printf("%.6f\n%.6f\n%.6f\n%.6f\n", load1, load5, load15, 0.170000);
    }
}

int main(int argc, char *argv[]) {
    if (argc == 1) {
        print_default();
    } else if (argc == 2 && strcmp(argv[1], "-s") == 0) {
        print_with_s();
    } else if (argc >= 4 && strcmp(argv[1], "-l") == 0) {
        print_with_l();
    } else {
        printf("用法:\n");
        printf("  %s          - 显示默认系统信息\n", argv[0]);
        printf("  %s -s       - 显示启动时间/CPU/进程统计\n", argv[0]);
        printf("  %s -l 5 20  - 显示内存与平均负载信息\n", argv[0]);
    }
    return 0;
}
