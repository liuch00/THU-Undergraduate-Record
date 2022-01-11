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
    sw t2, -12(fp)
    beq x0, t1, _L1
    li t0, 2
    mv t1, t0
    sw t1, -16(fp)
    j _L2
_L1:
    li t0, 3
    mv t1, t0
    sw t1, -16(fp)
_L2:
    lw t0, -12(fp)
    beq x0, t0, _L3
    li t0, 4
    mv t1, t0
    sw t1, -12(fp)
    j _L4
_L3:
    li t0, 5
    mv t1, t0
    sw t1, -12(fp)
_L4:
    lw t0, -16(fp)
    lw t1, -12(fp)
    add t2, t0, t1
    mv a0, t2
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

