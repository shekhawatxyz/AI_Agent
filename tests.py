import functions.get_file_content
import functions.get_files_info
import functions.write_file


print(
    functions.write_file.write_file(
        "calculator", "lorem.txt", "wait, this isn't lorem ipsum"
    )
)
print(
    functions.write_file.write_file(
        "calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"
    )
)
print(
    functions.write_file.write_file(
        "calculator", "/tmp/temp.txt", "this should not be allowed"
    )
)
# print(functions.get_file_content.get_file_content("calculator", "lorem.txt"))
# print(functions.get_file_content.get_file_content("calculator", "main.py"))
# print(functions.get_file_content.get_file_content("calculator", "pkg/calculator.py"))
# print(functions.get_file_content.get_file_content("calculator", "bin/cat"))
# print(
# functions.get_file_content.get_file_content("calculator", "pkg/does_not_exist.py")
# )
# print(functions.get_files_info.get_files_info("calculator", "."))
# print(functions.get_files_info.get_files_info("calculator", "pkg"))
# print(functions.get_files_info.get_files_info("calculator", "/bin"))
# print(functions.get_files_info.get_files_info("calculator", "../"))
