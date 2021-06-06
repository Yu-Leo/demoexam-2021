N = int(input())
sum = 0
while N > 0:
   digit = N % 10
   if digit < 7:
         sum = sum + 1
   N = N // 10
print(digit)
