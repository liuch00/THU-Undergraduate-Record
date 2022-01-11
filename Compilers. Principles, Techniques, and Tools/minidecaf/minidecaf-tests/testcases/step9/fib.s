    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    li t0, 5
    mv t1, t0
    sw t1, -4(sp)
    addi sp, sp, -4
    call fib
    addi sp, sp, 4
    mv t0, a0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
fib:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -16
    # end of prologue
    
    # start of body
    li t0, 0
    lw t1, 0(fp)
    sub t2, t1, t0
    seqz t2, t2
    li t0, 1
    sub t3, t1, t0
    seqz t3, t3
    or t0, t2, t3
    sw t1, -12(fp)
    beq x0, t0, _L1
    lw t0, 0(fp)
    mv a0, t0
    j fib_exit
_L1:
    li t0, 1
    lw t1, 0(fp)
    sub t2, t1, t0
    sw t2, -4(sp)
    sw t1, -12(fp)
    addi sp, sp, -4
    call fib
    addi sp, sp, 4
    mv t0, a0
    li t1, 2
    lw t2, 0(fp)
    sub t3, t2, t1
    sw t3, -4(sp)
    sw t0, -16(fp)
    addi sp, sp, -4
    call fib
    addi sp, sp, 4
    mv t0, a0
    lw t1, -16(fp)
    add t2, t1, t0
    mv a0, t2
    j fib_exit
    # end of body
    
fib_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

