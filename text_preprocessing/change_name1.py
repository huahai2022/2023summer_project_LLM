import os

def batch_rename_files(folder_path):
    # 获取文件夹中的所有文件名
    files = os.listdir(folder_path)

    for filename in files:
        if "chapter" in filename.lower():
            # 构建新的文件名
            new_filename = filename.replace("chapter", "Chapter")

            # 构建文件的完整路径
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)

            # 重命名文件
            os.rename(old_path, new_path)
            print(f"文件已重命名：{filename} -> {new_filename}")

    print("批量文件重命名完成！")

# 指定文件夹路径
folder_path = "C:/Users/85283/Desktop/chapter5.2"

# 执行批量改名操作
batch_rename_files(folder_path)
