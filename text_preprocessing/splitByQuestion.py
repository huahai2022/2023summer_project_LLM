def splitByQuestion(folder_path, file_name_without_suffix):
    with open(folder_path+file_name_without_suffix+".md", "r+", encoding="utf-8") as file:
        
        lines = file.readlines()
        
        count = 1
        new_file_lines = []
        for i, line in enumerate(lines):
            # write to new file if encouter delimiter
            if (f"{count+1}、" in line):
                if (len(new_file_lines) != 0):
                    with open(folder_path+f"{file_name_without_suffix}_{count}.md", "w", encoding="utf-8") as newfile:
                        newfile.writelines(new_file_lines)
                        count += 1
                        new_file_lines.clear()
            new_file_lines.append(line)
        with open(folder_path+f"{file_name_without_suffix}_{count}.md", "w", encoding="utf-8") as newfile:
            newfile.writelines(new_file_lines)