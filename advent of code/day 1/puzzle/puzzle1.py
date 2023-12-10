import time

start_time = time.perf_counter()  # Start the high-resolution timer

# Your code goes here
with open(r"day 1\puzzle 1\input.txt") as f:
    calibrationlines = f.read().splitlines() 
calibrationvalues = []
for line in calibrationlines:
    value = ""
    for elem in line:
        if elem.isdigit():
            value += elem
            break
    for elem in reversed(line):
        if elem.isdigit():
            value+=elem
            break
    calibrationvalues.append(int(value))

print(sum(calibrationvalues))

end_time = time.perf_counter()  # End the high-resolution timer

print(f"Execution time: {end_time - start_time} seconds")
