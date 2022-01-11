    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -52
    # end of prologue
    
    # start of body
    li t0, 0
    addi t1, fp, -48
    mv t2, t1
    li t3, 0
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t0, 0(t2)
    sw t1, -52(fp)
_L1:
    lw t0, -52(fp)
    mv t1, t0
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 1
    add t3, t2, t1
    mv t1, t0
    li t2, 0
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    sw t3, 0(t1)
    mv t1, t0
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 1
    add t3, t2, t1
    mv t1, t0
    mv t2, t0
    li t4, 0
    li t5, 4
    mul t5, t5, t4
    add t2, t2, t5
    lw t4, 0(t2)
    li t2, 4
    mul t2, t2, t4
    add t1, t1, t2
    sw t3, 0(t1)
    sw t0, -52(fp)
_L2:
    lw t0, -52(fp)
    mv t1, t0
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 10
    li t3, 1
    sub t4, t1, t3
    sub t1, t2, t4
    snez t1, t1
    sw t0, -52(fp)
    bne x0, t1, _L1
_L3:
    li t0, 0
    lw t1, -52(fp)
    mv t2, t1
    li t3, 10
    li t4, 1
    sub t5, t3, t4
    li t3, 4
    mul t3, t3, t5
    add t2, t2, t3
    sw t0, 0(t2)
    mv t0, t1
    mv t2, t1
    mv t3, t1
    mv t4, t1
    mv t5, t1
    mv t6, t1
    mv a0, t1
    mv a1, t1
    mv a2, t1
    li t1, 1
    li a3, 4
    mul a3, a3, t1
    add a2, a2, a3
    lw t1, 0(a2)
    li a2, 4
    mul a2, a2, t1
    add a1, a1, a2
    lw t1, 0(a1)
    li a1, 4
    mul a1, a1, t1
    add a0, a0, a1
    lw t1, 0(a0)
    li a0, 4
    mul a0, a0, t1
    add t6, t6, a0
    lw t1, 0(t6)
    li t6, 4
    mul t6, t6, t1
    add t5, t5, t6
    lw t1, 0(t5)
    li t5, 4
    mul t5, t5, t1
    add t4, t4, t5
    lw t1, 0(t4)
    li t4, 4
    mul t4, t4, t1
    add t3, t3, t4
    lw t1, 0(t3)
    li t3, 4
    mul t3, t3, t1
    add t2, t2, t3
    lw t1, 0(t2)
    li t2, 4
    mul t2, t2, t1
    add t0, t0, t2
    lw t1, 0(t0)
    mv a0, t1
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 52
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

