    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -16
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t1, -12(fp)
    sw t2, -16(fp)
_L1:
    li t0, 3
    lw t1, -16(fp)
    slt t2, t1, t0
    sw t1, -16(fp)
    beq x0, t2, _L3
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
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
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

