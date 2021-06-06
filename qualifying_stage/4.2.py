N = int(input())
sum = 0
while N > 0:
   digit = N % 10
   if digit < 7:
         sum = sum + digit
   N = N // 10
print(sum)
