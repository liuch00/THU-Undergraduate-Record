    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -124
    # end of prologue
    
    # start of body
    li t0, 1
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
    li t0, 3
    lw t1, -20(fp)
    slt t2, t1, t0
    sw t1, -20(fp)
    beq x0, t2, _L6
    li t0, 6
    lw t1, -16(fp)
    mul t2, t1, t0
    li t0, 3
    lw t3, -20(fp)
    mul t4, t3, t0
    sub t0, t2, t4
    addi t2, fp, -116
    mv t4, t2
    li t5, 48
    mul t5, t5, t1
    add t4, t4, t5
    li t5, 16
    mul t5, t5, t3
    add t4, t4, t5
    li t5, 0
    li t6, 4
    mul t6, t6, t5
    add t4, t4, t6
    sw t0, 0(t4)
    li t0, 1
    mv t4, t0
    sw t1, -16(fp)
    sw t3, -20(fp)
    sw t2, -120(fp)
    sw t4, -124(fp)
_L7:
    li t0, 4
    lw t1, -124(fp)
    slt t2, t1, t0
    sw t1, -124(fp)
    beq x0, t2, _L9
    li t0, 2
    lw t1, -12(fp)
    mul t2, t1, t0
    li t0, 1
    add t1, t2, t0
    mv t0, t1
    lw t1, -120(fp)
    mv t2, t1
    li t3, 48
    lw t4, -16(fp)
    mul t3, t3, t4
    add t2, t2, t3
    li t3, 16
    lw t5, -20(fp)
    mul t3, t3, t5
    add t2, t2, t3
    li t3, 1
    lw t6, -124(fp)
    sub a0, t6, t3
    li t3, 4
    mul t3, t3, a0
    add t2, t2, t3
    lw t3, 0(t2)
    add t2, t3, t0
    mv t3, t1
    li a0, 48
    mul a0, a0, t4
    add t3, t3, a0
    li a0, 16
    mul a0, a0, t5
    add t3, t3, a0
    li a0, 4
    mul a0, a0, t6
    add t3, t3, a0
    sw t2, 0(t3)
    sw t0, -12(fp)
    sw t4, -16(fp)
    sw t5, -20(fp)
    sw t1, -120(fp)
    sw t6, -124(fp)
_L8:
    li t0, 1
    lw t1, -124(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -124(fp)
    j _L7
_L9:
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
    lw t0, -120(fp)
    mv t1, t0
    li t2, 1
    li t3, 48
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 2
    li t3, 16
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 3
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    mv t1, t0
    li t0, 0
    li t3, 48
    mul t3, t3, t0
    add t1, t1, t3
    li t0, 0
    li t3, 16
    mul t3, t3, t0
    add t1, t1, t3
    li t0, 2
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
    addi sp, sp, 124
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

