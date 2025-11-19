import functions.get_file_content
import functions.get_files_info

# print(functions.get_file_content.get_file_content("calculator", "lorem.txt"))
print(functions.get_file_content.get_file_content("calculator", "main.py"))
print(functions.get_file_content.get_file_content("calculator", "pkg/calculator.py"))
print(functions.get_file_content.get_file_content("calculator", "bin/cat"))
print(
    functions.get_file_content.get_file_content("calculator", "pkg/does_not_exist.py")
)
# print(functions.get_files_info.get_files_info("calculator", "."))
# print(functions.get_files_info.get_files_info("calculator", "pkg"))
# print(functions.get_files_info.get_files_info("calculator", "/bin"))
# print(functions.get_files_info.get_files_info("calculator", "../"))
