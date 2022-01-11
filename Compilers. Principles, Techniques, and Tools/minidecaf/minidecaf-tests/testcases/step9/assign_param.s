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
    li t0, 5
    sw t0, -4(sp)
    sw t1, -12(fp)
    addi sp, sp, -4
    call fun
    addi sp, sp, 4
    mv t0, a0
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
    
fun:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    li t0, 5
    mv t1, t0
    mv a0, t0
    j fun_exit
    # end of body
    
fun_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

