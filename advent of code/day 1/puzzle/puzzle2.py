import time

start_time = time.perf_counter()  # Start the high-resolution timer

# Your code goes here
with open(r"day 1\puzzle 1\input.txt") as f:
    calibrationlines = f.read().splitlines() 

calibrationlines=["twonethree","twoone1zero4","eightone1three","84","1wofkok4fofr","threetwo1zero","dcjsdcknsjn","eightyonetwo"]
calibrationvalues = []
numbers = {"one": "1", "two": "2", "three": "3", "four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","zero":"0"}
calibrationlines_new = []
for i,line in enumerate(calibrationlines):
    for key in numbers.keys():
        line = line.replace(key,numbers[key])
    calibrationlines_new.append(line)
    value = ""
    for i,elem in enumerate(line):
        index=-1
        if elem.isdigit():
            index = i
            value += elem
            break
    for i,elem in enumerate(reversed(line)):
        if elem.isdigit():
            if (len(line)-1)-i!=index:
                value+=elem
                break
    if value!="":
        calibrationvalues.append(int(value))

print(calibrationlines)
print(calibrationlines_new)
print(calibrationvalues)
# print(sum(calibrationvalues))

end_time = time.perf_counter()  # End the high-resolution timer

print(f"Execution time: {end_time - start_time} seconds")
