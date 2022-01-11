    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -24
    # end of prologue
    
    # start of body
    li t0, 1
    li t1, 2
    sw t0, -8(sp)
    sw t1, -4(sp)
    addi sp, sp, -8
    call sum
    addi sp, sp, 8
    mv t0, a0
    li t1, 1
    li t2, 2
    sw t1, -8(sp)
    sw t2, -4(sp)
    sw t0, -12(fp)
    addi sp, sp, -8
    call sum
    addi sp, sp, 8
    mv t0, a0
    li t1, 2
    div t2, t0, t1
    li t0, 2
    mul t1, t2, t0
    lw t0, -12(fp)
    sub t2, t0, t1
    mv t0, t2
    li t1, 2
    li t2, 3
    li t3, 4
    sw t2, -8(sp)
    sw t3, -4(sp)
    sw t0, -16(fp)
    sw t1, -20(fp)
    addi sp, sp, -8
    call sum
    addi sp, sp, 8
    mv t0, a0
    lw t1, -20(fp)
    mul t2, t1, t0
    li t0, 1
    li t1, 2
    sw t0, -8(sp)
    sw t1, -4(sp)
    sw t2, -24(fp)
    addi sp, sp, -8
    call sum
    addi sp, sp, 8
    mv t0, a0
    lw t1, -24(fp)
    add t2, t1, t0
    mv t0, t2
    lw t1, -16(fp)
    sub t2, t0, t1
    mv a0, t2
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 24
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
sum:
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
    j sum_exit
    # end of body
    
sum_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

