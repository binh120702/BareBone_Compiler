extern printf
SECTION .data
fmt: db "%s = %lld", 10, 0
Label_id1 : dq 0
Label_idOrigin1 : dq "X0"
SECTION .text
global main 
 main: 
 push rbp 
mov rcx, [Label_id1] 
 add rcx, 1 
 mov [Label_id1], rcx 
mov rdi, fmt 
 mov rsi, Label_idOrigin1 
 mov rdx, [Label_id1] 
 mov rax, 0 
 call printf 
pop rbp 
 mov rax, 0 
 ret