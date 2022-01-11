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
    li t0, 1
    mv t1, t0
    li t0, 2
    mv t2, t0
    li t0, 0
    mv t3, t0
    sgt t0, t1, t2
    sw t3, -12(fp)
    beq x0, t0, _L2
    li t0, 5
    mv t1, t0
    sw t1, -16(fp)
    j _L1
_L2:
    lw t0, -12(fp)
    beq x0, t0, _L4
    li t0, 6
    mv t1, t0
    sw t1, -20(fp)
    j _L3
_L4:
    li t0, 7
    mv t1, t0
    sw t1, -20(fp)
_L3:
    lw t0, -20(fp)
    mv t1, t0
    sw t1, -16(fp)
_L1:
    lw t0, -16(fp)
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
    

