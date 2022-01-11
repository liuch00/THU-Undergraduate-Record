    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -40
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t1, -12(fp)
    sw t2, -16(fp)
_L1:
    li t0, 2
    lw t1, -16(fp)
    slt t2, t1, t0
    sw t1, -16(fp)
    beq x0, t2, _L3
    li t0, 0
    mv t1, t0
    sw t1, -20(fp)
_L4:
    li t0, 2
    lw t1, -20(fp)
    slt t2, t1, t0
    sw t1, -20(fp)
    beq x0, t2, _L6
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    addi t0, fp, -36
    mv t3, t0
    li t4, 8
    lw t5, -16(fp)
    mul t4, t4, t5
    add t3, t3, t4
    li t4, 4
    lw t6, -20(fp)
    mul t4, t4, t6
    add t3, t3, t4
    sw t2, 0(t3)
    sw t1, -12(fp)
    sw t5, -16(fp)
    sw t6, -20(fp)
    sw t0, -40(fp)
_L5:
    li t0, 1
    lw t1, -20(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -20(fp)
    j _L4
_L6:
_L2:
    li t0, 1
    lw t1, -16(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -16(fp)
    j _L1
_L3:
    lw t0, -40(fp)
    mv t1, t0
    li t2, 0
    li t3, 8
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 40
    mul t3, t2, t1
    mv t1, t0
    li t2, 0
    li t4, 8
    mul t4, t4, t2
    add t1, t1, t4
    li t2, 1
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 20
    mul t4, t2, t1
    add t1, t3, t4
    mv t2, t0
    li t3, 1
    li t4, 8
    mul t4, t4, t3
    add t2, t2, t4
    li t3, 0
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    lw t3, 0(t2)
    li t2, 10
    mul t4, t3, t2
    add t2, t1, t4
    mv t1, t0
    li t0, 1
    li t3, 8
    mul t3, t3, t0
    add t1, t1, t3
    li t0, 1
    li t3, 4
    mul t3, t3, t0
    add t1, t1, t3
    lw t0, 0(t1)
    add t1, t2, t0
    mv a0, t1
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 40
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

