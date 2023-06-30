import chardet





def removePageNumber(file_path, start_counter):
    with open(file_path, "r+", encoding=f"{result['encoding']}") as file:
        lines = file.readlines()

        count = start_counter
        for i, line in enumerate(lines):
            line = line.replace("\n", "")
            line = line.replace("\t", "")
            if (line.isdecimal() and int(line) == count):
                modified_line = ""
                lines[i] = modified_line
                count += 1

        file.seek(0)
        file.writelines(lines)
        file.truncate()

# 读取文件内容
with open('D:\learn\project\llm\\Data\\MTDS.pdf', 'rb') as f:
    content = f.read()
# 检测文件的编码格式
result = chardet.detect(content)

removePageNumber("D:\learn\project\llm\\Data\\MTDS.pdf",429)