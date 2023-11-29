import subprocess
import sys
import time
import os
from parse import parse_files

# Create a file containing only local ips.
print("Creating ip files...")
prefix = "127.0.0.1:"
filename = "ips.txt"
f = open(filename, "w")
ips = []

for i in range(int(sys.argv[1])):
    port = 9000 + i
    f.write(prefix + str(port) + '\n')
    ips.append(prefix + str(port) + '\n')

f.close()

print("Deleting old logs...")
for file in os.scandir("logs"):
    if file.name.endswith(".log"):
        os.unlink(file.path)

# compile in release mode
print("Compiling...")
subprocess.run("cargo build --bin app --release", shell=True)

# start all nodes
subprocess.run("killall -9 app", shell=True)

print("Starting nodes...")
processes = []
for i, ip in enumerate(ips):
    cmd = "./target/release/app {} {} &> logs/{}.log".format(i, filename, i)
    p = subprocess.Popen(cmd, shell=True)
    processes.append(p)

# wait and kill nodes
time.sleep(10)
print("Shutting down nodes...")
for p in processes:
    p.kill()

# just to be sure
subprocess.run("killall -9 app", shell=True)

print("Parsing logs...")
print(f'Average time between two beacon values: {parse_files("logs/")}s')
