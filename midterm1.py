name = []
math = []
eng = []


for i in range (1, 6):
    name.append(input("\nno.%s student name: "%i))
    math.append(int(input("no.%s math score: "%i)))
    eng.append(int(input("no.%s english score: "%i)))

mathSum = 0
engSum = 0

for i in range (0, 5):
    mathSum += math[i]
    engSum += eng[i]

mathMean = mathSum/5
engMean = engSum/5

print("\nmath mean: %s"%mathMean)
print("english mean: %s"%engMean)
print("name list:")
for i in range (0, 5):
   print("    %s" %name[i])
