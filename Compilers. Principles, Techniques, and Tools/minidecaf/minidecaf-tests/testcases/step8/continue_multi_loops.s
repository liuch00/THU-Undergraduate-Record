    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -20
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t1, -12(fp)
    sw t2, -16(fp)
_L1:
    li t0, 10
    lw t1, -16(fp)
    slt t2, t1, t0
    sw t1, -16(fp)
    beq x0, t2, _L3
    li t0, 0
    mv t1, t0
    sw t1, -20(fp)
_L4:
    li t0, 10
    lw t1, -20(fp)
    slt t2, t1, t0
    sw t1, -20(fp)
    beq x0, t2, _L6
    j _L5
_L5:
    li t0, 1
    lw t1, -20(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -20(fp)
    j _L4
_L6:
    lw t0, -12(fp)
    lw t1, -16(fp)
    add t2, t0, t1
    mv t0, t2
    sw t0, -12(fp)
    sw t1, -16(fp)
_L2:
    li t0, 1
    lw t1, -16(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -16(fp)
    j _L1
_L3:
    lw t0, -12(fp)
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 20
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

