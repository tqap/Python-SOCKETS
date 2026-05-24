import platform

system = platform.system()

if system == "Windows":
    param = "-n"
else:
    param = "-c"