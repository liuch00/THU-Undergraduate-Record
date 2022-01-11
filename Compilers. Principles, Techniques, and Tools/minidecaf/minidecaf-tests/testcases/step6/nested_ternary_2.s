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
    li t0, 1
    beq x0, t0, _L2
    li t0, 2
    beq x0, t0, _L4
    li t0, 3
    mv t1, t0
    sw t1, -12(fp)
    j _L3
_L4:
    li t0, 4
    mv t1, t0
    sw t1, -12(fp)
_L3:
    lw t0, -12(fp)
    mv t1, t0
    sw t1, -16(fp)
    j _L1
_L2:
    li t0, 5
    mv t1, t0
    sw t1, -16(fp)
_L1:
    lw t0, -16(fp)
    mv t1, t0
    li t0, 0
    sw t1, -20(fp)
    beq x0, t0, _L6
    li t0, 2
    beq x0, t0, _L8
    li t0, 3
    mv t1, t0
    sw t1, -24(fp)
    j _L7
_L8:
    li t0, 4
    mv t1, t0
    sw t1, -24(fp)
_L7:
    lw t0, -24(fp)
    mv t1, t0
    sw t1, -28(fp)
    j _L5
_L6:
    li t0, 5
    mv t1, t0
    sw t1, -28(fp)
_L5:
    lw t0, -28(fp)
    mv t1, t0
    lw t0, -20(fp)
    mul t2, t0, t1
    mv a0, t2
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 28
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

