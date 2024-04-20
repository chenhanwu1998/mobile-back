from src.constant import mobile_data_path, evaluate_data_path, param_data_path

if __name__ == '__main__':
    import os

    mobile_file_list = os.listdir(mobile_data_path)
    mobile_eva_list = os.listdir(evaluate_data_path)
    param_data_list = os.listdir(param_data_path)
    for i, temp in enumerate(mobile_eva_list):
        mobile_eva_list[i] = temp.replace("evaluate_", "")
    for i, temp in enumerate(param_data_list):
        param_data_list[i] = temp.replace("param_", "")
    print("mobile_fil_list:", mobile_file_list)
    print('mobile_eva_list:', mobile_eva_list)
    print("param_data_list:", param_data_list)
