import sys
import subprocess


def vpy_converter(vpy, tab=4):
    brace_counter = 0
    result = []
    res = list(map(str.strip, vpy.split('\n')))
    passer = False
    for i in res:
        if len(i) == 0:
            result.append(i)
            continue
        if '{' == i[len(i) - 1]:
            brace_counter += 1
            passer = 1
        elif '}' == i:
            brace_counter -= 1
            result.append((brace_counter + 1) * tab * " " + "pass")
            continue
        if not passer:
            result.append(brace_counter * tab * " " + i)
        else:
            result.append((brace_counter - 1) * tab * " " + i[0:len(i) - 1] + ":")
        passer = 0

    result = "\n".join(result)
    return result + "\n"


def vpy_converter_online(tab=4):
    brace_counter = 0
    result = []
    passer = False
    while True:
        i = input().strip()
        if len(i) == 0:
            result.append(i)
            if brace_counter == 0:
                break
            print("...", end=' ')
        if '{' == i[len(i) - 1]:
            brace_counter += 1
            passer = 1
        elif '}' == i:
            brace_counter -= 1
            result.append((brace_counter + 1) * tab * " " + "pass")
            print("...", end=' ')
            continue
        if not passer:
            result.append(brace_counter * tab * " " + i)
        else:
            result.append((brace_counter - 1) * tab * " " + i[0:len(i) - 1] + ":")
        passer = 0
        if brace_counter == 0:
            break
        print("...", end=' ')
    result = "\n".join(result)
    return result + "\n"


builder_code = """\
def exit():
    sys.exit()

"""

if __name__ == '__main__':
    try:
        compile_file = sys.argv[1]
        try:
            if compile_file.split('.')[1] == "vpy":
                vpy_file = open(compile_file, "r")
                py_filename = compile_file.split('.')[0] + ".py"
                py_file = open(py_filename, "w")
                vpy_file_string = vpy_file.read()
                py_file_string = vpy_converter(vpy_file_string)
                py_file.write(py_file_string)
                py_file.close()
                vpy_file.close()
                output = subprocess.Popen(["python", py_filename], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          shell=True)
                out, error = output.communicate()
                print(out.decode())
        except IOError as e:
            print(e)
    except IndexError:
        print("vpy interpreter is online (Created by Vishal)", end='\n\n')
        while True:
            try:
                print(">>>", end=' ')
                exec(builder_code)
                exec(vpy_converter_online())
                print()
            except Exception as e:
                print(e)
