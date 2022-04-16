extern printf
SECTION .data
fmt: db "%s = %lld", 10, 0
Label_id1 : dq 0
Label_idOrigin1 : dq "X0"
Label_id2 : dq 0
Label_idOrigin2 : dq "Y"
SECTION .text
global main 
 main: 
 push rbp 
mov rcx, [Label_id1] 
 add rcx, 1 
 mov [Label_id1], rcx 
mov rcx, [Label_id1] 
 add rcx, 1 
 mov [Label_id1], rcx 
mov rcx, [Label_id2] 
 add rcx, 1 
 mov [Label_id2], rcx 
mov rdi, fmt 
 mov rsi, Label_idOrigin1 
 mov rdx, [Label_id1] 
 mov rax, 0 
 call printf 
mov rdi, fmt 
 mov rsi, Label_idOrigin2 
 mov rdx, [Label_id2] 
 mov rax, 0 
 call printf 
pop rbp 
 mov rax, 0 
 ret