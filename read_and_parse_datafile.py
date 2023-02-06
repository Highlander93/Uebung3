def parse_data(path_to_data):
    file = open(path_to_data)
    nonempty_lines = [line.strip("\n") for line in file if line != "\n"]
    parsed_lines = []
    for each_line in nonempty_lines:
        parsed_lines.append(parsing_lines(each_line))
    file.close()
    return parsed_lines

def parsing_lines(each_line):
    parsed_line = []
    parsed_between_space = each_line.split(" ")
    parsed_result = parsed_between_space[1].split(":")
    parsed_line.append(parsed_between_space[0])
    parsed_line.append(parsed_result[0])
    parsed_line.append(parsed_result[1])
    return parsed_line