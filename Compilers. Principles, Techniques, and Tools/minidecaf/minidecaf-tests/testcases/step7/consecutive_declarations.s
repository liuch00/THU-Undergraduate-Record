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
    li t0, 0
    mv t1, t0
    li t0, 1
    mv t1, t0
    mv t0, t1
    li t1, 2
    mv t2, t1
    add t1, t0, t2
    mv t0, t1
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
    

