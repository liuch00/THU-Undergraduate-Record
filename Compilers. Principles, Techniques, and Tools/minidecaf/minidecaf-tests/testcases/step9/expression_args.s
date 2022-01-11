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
    li t0, 1
    li t1, 2
    add t2, t0, t1
    li t0, 4
    sw t2, -8(sp)
    sw t0, -4(sp)
    addi sp, sp, -8
    call add
    addi sp, sp, 8
    mv t0, a0
    mv t1, t0
    add t0, t1, t1
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
    
add:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    lw t0, 0(fp)
    lw t1, 4(fp)
    add t2, t0, t1
    mv a0, t2
    j add_exit
    # end of body
    
add_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

