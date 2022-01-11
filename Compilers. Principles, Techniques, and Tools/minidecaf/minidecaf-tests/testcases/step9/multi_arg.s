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
    li t0, 10
    li t1, 4
    li t2, 2
    sw t0, -12(sp)
    sw t1, -8(sp)
    sw t2, -4(sp)
    addi sp, sp, -12
    call sub_3
    addi sp, sp, 12
    mv t0, a0
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
    
sub_3:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    lw t0, 0(fp)
    lw t1, 4(fp)
    sub t2, t0, t1
    lw t0, 8(fp)
    sub t1, t2, t0
    mv a0, t1
    j sub_3_exit
    # end of body
    
sub_3_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

