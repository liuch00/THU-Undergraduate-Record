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
    li t1, 2
    sgt t2, t0, t1
    beq x0, t2, _L2
    li t0, 3
    mv t1, t0
    sw t1, -12(fp)
    j _L1
_L2:
    li t0, 4
    mv t1, t0
    sw t1, -12(fp)
_L1:
    lw t0, -12(fp)
    mv t1, t0
    li t0, 1
    li t2, 2
    sgt t3, t0, t2
    sw t1, -16(fp)
    beq x0, t3, _L4
    li t0, 5
    mv t1, t0
    sw t1, -20(fp)
    j _L3
_L4:
    li t0, 6
    mv t1, t0
    sw t1, -20(fp)
_L3:
    lw t0, -20(fp)
    mv t1, t0
    lw t0, -16(fp)
    add t2, t0, t1
    mv a0, t2
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 20
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

