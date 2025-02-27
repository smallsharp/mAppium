import os
import subprocess


def getPhoneInfo(deviceName):
    """
    :param deviceName: 设备名称
    :return: 手机基本信息
    """
    cmd = "adb -s " + deviceName + " shell cat /system/build.prop "
    print('cmd:',cmd)
    # content = os.popen(cmd).readlines()
    content = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result = {"release": "5.0", "model": "model", "brand": "brand", "device": "device"}
    release = "ro.build.version.release="  # 版本
    model = "ro.product.model="  # 型号
    brand = "ro.product.brand="  # 品牌
    device = "ro.product.device="  # 设备代号
    for con in content:
        for i in con.split():
            temp = i.decode()
            if temp.find(release) >= 0:
                result["release"] = temp[len(release):]
                break
            if temp.find(model) >= 0:
                result["model"] = temp[len(model):]
                break
            if temp.find(brand) >= 0:
                result["brand"] = temp[len(brand):]
                break
            if temp.find(device) >= 0:
                result["device"] = temp[len(device):]
                break
    return result


# 得到最大运行内存
def get_men_total(devices):
    cmd = "adb -s " + devices + " shell cat /proc/meminfo"
    get_cmd = os.popen(cmd).readlines()
    men_total = 0
    men_total_str = "MemTotal"
    for line in get_cmd:
        if line.find(men_total_str) >= 0:
            men_total = line[len(men_total_str) + 1:].replace("kB", "").strip()
            break
    return int(men_total)

# cpu核心数量
def get_cpu_kel(devices):
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    get_cmd = os.popen(cmd).readlines()
    find_str = "processor"
    int_cpu = 0
    for line in get_cmd:
        if line.find(find_str) >= 0:
            int_cpu += 1
    return str(int_cpu) + "核"


# 手机分辨率
def get_app_pix(devices):
    result = os.popen("adb -s " + devices + " shell wm size", "r")
    return result.readline().split("Physical size:")[1]
