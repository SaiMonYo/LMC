
# first input starting fibbonacci number
# second input second fibbonacci number
# third input how many fibbonacci numbers to print
fibonacci_code = '''INP
STA x
INP
STA y
INP
STA lmt
LDA x
OUT
LDA y
OUT
loop    LDA lmt
BRZ end
SUB one
STA lmt
LDA x
ADD y
STA z
OUT
LDA y
STA x
LDA z
STA y
BRA loop
end   LDA z
SUB z
HLT
x    DAT
y    DAT
z    DAT
lmt   DAT
one   DAT 1'''


# prints max of two numbers
max_code = '''	INP
	STA x
	INP
	STA y
	SUB x
	BRP outit
	LDA x
	OUT
	HLT
	
outit	LDA y
	OUT
	HLT
x	DAT
y	DAT   
'''


# counts down from input
counter_code = '''        INP
loop    OUT   
        STA count
        SUB one
        STA count
        BRP loop
        HLT
		
one     DAT 1
count   DAT   '''