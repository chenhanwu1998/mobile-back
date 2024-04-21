import threading
import time


def worker():
    """线程执行的函数"""
    print("线程启动")
    time.sleep(2)  # 模拟I/O操作
    print("线程结束")


if __name__ == '__main__':
    # 创建线程对象
    t = threading.Thread(target=worker)
    # 启动线程
    t.start()
    # 等待线程完成（可选）
    # t.join()
    print("主线程继续执行")

    # mobile_file_list = os.listdir(mobile_data_path)
    # mobile_eva_list = os.listdir(evaluate_data_path)
    # param_data_list = os.listdir(param_data_path)
    # for i, temp in enumerate(mobile_eva_list):
    #     mobile_eva_list[i] = temp.replace("evaluate_", "")
    # for i, temp in enumerate(param_data_list):
    #     param_data_list[i] = temp.replace("param_", "")
    # print("mobile_fil_list:", mobile_file_list)
    # print('mobile_eva_list:', mobile_eva_list)
    # print("param_data_list:", param_data_list)
