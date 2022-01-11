    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -104
    # end of prologue
    
    # start of body
    li t0, 5
    addi t1, fp, -104
    mv t2, t1
    li t3, 1
    li t4, 48
    mul t4, t4, t3
    add t2, t2, t4
    li t3, 2
    li t4, 16
    mul t4, t4, t3
    add t2, t2, t4
    li t3, 3
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t0, 0(t2)
    mv t0, t1
    li t2, 1
    li t3, 48
    mul t3, t3, t2
    add t0, t0, t3
    li t2, 2
    li t3, 16
    mul t3, t3, t2
    add t0, t0, t3
    li t2, 3
    li t3, 4
    mul t3, t3, t2
    add t0, t0, t3
    lw t2, 0(t0)
    mv t0, t1
    li t3, 0
    li t4, 48
    mul t4, t4, t3
    add t0, t0, t4
    li t3, 0
    li t4, 16
    mul t4, t4, t3
    add t0, t0, t4
    li t3, 2
    li t4, 4
    mul t4, t4, t3
    add t0, t0, t4
    sw t2, 0(t0)
    mv t0, t1
    li t2, 1
    li t3, 48
    mul t3, t3, t2
    add t0, t0, t3
    li t2, 2
    li t3, 16
    mul t3, t3, t2
    add t0, t0, t3
    li t2, 3
    li t3, 4
    mul t3, t3, t2
    add t0, t0, t3
    lw t2, 0(t0)
    mv t0, t1
    li t1, 0
    li t3, 48
    mul t3, t3, t1
    add t0, t0, t3
    li t1, 0
    li t3, 16
    mul t3, t3, t1
    add t0, t0, t3
    li t1, 2
    li t3, 4
    mul t3, t3, t1
    add t0, t0, t3
    lw t1, 0(t0)
    add t0, t2, t1
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 104
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

