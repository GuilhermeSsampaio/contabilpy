from tools.convert_files import convert_csv_to_excel


def chose_operation(option, input_file):
    match(option):
        case "CSV para Excel":
            return convert_csv_to_excel(input_file, "converted_file.xlsx")
    
    