import os
import subprocess
import tkinter as tk
from tkinter import filedialog, simpledialog

def read_binary_file(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data

def generate_cpp_code(files, title, after_command):
    includes = '#include <iostream>\n#include <fstream>\n#include <cstdlib>\n\n'
    arrays = ''
    extract_function = 'void extract_files() {\n'
    after_command_code = f'system("{after_command}");\n' if after_command else ''
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        array_name = file_name.replace('.', '_').replace('-', '_').replace('/', '_').replace('\\', '_')
        data = read_binary_file(file_path)
        arrays += f'const unsigned char {array_name}[] = {{\n    '
        arrays += ', '.join(hex(b) for b in data) + '\n};\n'
        arrays += f'const unsigned int {array_name}_len = {len(data)};\n\n'
        extract_function += f'    std::ofstream out("{file_name}", std::ios::binary);\n'
        extract_function += f'    out.write(reinterpret_cast<const char*>({array_name}), {array_name}_len);\n'
        extract_function += '    out.close();\n'

    extract_function += f'    {after_command_code}'
    extract_function += '}\n\n'

    main_function = f'int main() {{\n    std::cout << "-- {title} installer ---" << std::endl;\n'
    main_function += f'    std::cout << "Made with ElliNet13\'s archive executable generator" << std::endl;\n'
    main_function += f'    std::cout << "https://github.com/ElliNet13/earchivexe" << std::endl;\n'
    for file_path in files:
        file_name = os.path.basename(file_path)
        main_function += f'    std::cout << "Files made: {file_name}" << std::endl;\n'
    if after_command:
        main_function += f'    std::cout << "> {after_command}" << std::endl;\n'
    
    main_function += f'    extract_files();\n'
    main_function += f'    return 0;\n}}\n'

    cpp_code = includes + arrays + extract_function + main_function
    return cpp_code

def compile_cpp_code(cpp_code, output_file):
    with open(output_file + '.cpp', 'w') as f:
        f.write(cpp_code)

    # Compile the C++ code to an executable using g++
    subprocess.run(['g++', '-std=c++11', '-o', output_file, output_file + '.cpp'])
    os.remove(output_file + '.cpp')  # Remove the temporary .cpp file

def select_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Select files to include in the archive")
    return root.tk.splitlist(file_paths)

def get_user_input(prompt):
    root = tk.Tk()
    root.withdraw()
    return simpledialog.askstring("Input", prompt)

def main():
    title = get_user_input("Enter the title for the self-extracting archive:")
    files = select_files()
    after_command = get_user_input("Enter the command to run after extraction (leave blank for none):")
    output_file = get_user_input("Enter the name for the output executable (e.g., output):")

    if not title or not files or not output_file:
        print("All fields are required.")
        return

    cpp_code = generate_cpp_code(files, title, after_command)
    compile_cpp_code(cpp_code, output_file)
    print(f"Self-extracting archive script created successfully: {output_file}")

if __name__ == "__main__":
    print("Welcome to the ElliNet13's Archive Executeable Generator!")
    print("Warning: G++ is required for this to work.")
    main()
