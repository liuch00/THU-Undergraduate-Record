    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    li t0, 6
    sw t0, -4(sp)
    addi sp, sp, -4
    call f
    addi sp, sp, 4
    mv t0, a0
    li t1, 6
    sub t2, t0, t1
    snez t2, t2
    beq x0, t2, _L1
    li t0, 1
    mv a0, t0
    j main_exit
_L1:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
f:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    lw t0, 0(fp)
    mv a0, t0
    j f_exit
    # end of body
    
f_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

