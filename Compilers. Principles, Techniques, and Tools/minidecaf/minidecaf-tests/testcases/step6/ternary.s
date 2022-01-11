    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -12
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    li t0, 1
    neg t2, t0
    sgt t0, t1, t2
    beq x0, t0, _L2
    li t0, 4
    mv t1, t0
    sw t1, -12(fp)
    j _L1
_L2:
    li t0, 5
    mv t1, t0
    sw t1, -12(fp)
_L1:
    lw t0, -12(fp)
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 12
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

