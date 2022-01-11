    .bss
    .globl a
    a:
        .space 4
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
    li t0, 24
    la t1, a
    mv t2, t1
    li t3, 0
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t0, 0(t2)
    mv t0, t1
    li t1, 0
    li t2, 4
    mul t2, t2, t1
    add t0, t0, t2
    lw t1, 0(t0)
    mv a0, t1
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

