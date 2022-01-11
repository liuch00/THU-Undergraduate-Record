    .data
    .globl a
    a:
        .word 3
    .data
    .globl b
    b:
        .word 4
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
    la t0, a
    lw t1, 0(t0)
    la t0, b
    lw t2, 0(t0)
    mul t0, t1, t2
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
    

