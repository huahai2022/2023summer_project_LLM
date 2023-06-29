def removePageNumber(file_path, start_counter):
    with open(file_path, "r+", encoding="utf-8") as file:
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