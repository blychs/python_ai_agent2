from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def tests():
    # result = get_files_info("calculator", ".")
    # print("Result for current directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "pkg")
    # print("Result for 'pkg' directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "/bin")
    # print("Result for '/bin' directory:")
    # print(result)
    # print("")

    # result = get_files_info("calculator", "../")
    # print("Result for '../' directory:")
    # print(result)
    # print("")

    # result = get_file_content("calculator", "lorem.txt")
    # print("Result for contents, with truncation:")
    # print(result)

    # result = get_file_content("calculator", "main.py")
    # print("main calculator:")
    # print(result)

    # result = get_file_content("calculator", "pkg/calculator.py")
    # print("calculator.py:")
    # print(result)

    # result = get_file_content("calculator", "/bin/cat")
    # print("error1:")
    # print(result)

    # result = get_file_content("calculator", "pkg/does_not_exist.py")
    # print("error2:")
    # print(result)

    # result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    # print(result)

    # result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    # print(result)

    # result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    # print(result)

    result = run_python_file("calculator", "main.py")
    print(result)

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)

    result = run_python_file("calculator", "../main.py")
    print(result)

    result = run_python_file("calculator", "nonexistent.py")
    print(result)


if __name__ == "__main__":
    tests()
