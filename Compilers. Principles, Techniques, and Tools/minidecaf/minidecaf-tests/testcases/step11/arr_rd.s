    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -28
    # end of prologue
    
    # start of body
    addi t0, fp, -16
    mv t1, t0
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    mv t1, t0
    li t3, 1
    li t4, 4
    mul t4, t4, t3
    add t1, t1, t4
    lw t3, 0(t1)
    add t1, t2, t3
    mv t1, t0
    li t0, 1
    li t2, 4
    mul t2, t2, t0
    add t1, t1, t2
    lw t0, 0(t1)
    addi t0, fp, -24
    mv t1, t0
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    mv t1, t0
    li t3, 0
    li t4, 4
    mul t4, t4, t3
    add t1, t1, t4
    lw t3, 0(t1)
    sub t1, t2, t3
    snez t1, t1
    sw t0, -28(fp)
    beq x0, t1, _L1
    li t0, 1
    mv a0, t0
    j main_exit
_L1:
    lw t0, -28(fp)
    mv t1, t0
    li t2, 1
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    mv t1, t0
    li t0, 1
    li t3, 4
    mul t3, t3, t0
    add t1, t1, t3
    lw t0, 0(t1)
    sub t1, t2, t0
    snez t1, t1
    beq x0, t1, _L2
    li t0, 1
    mv a0, t0
    j main_exit
_L2:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 28
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

