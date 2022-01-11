    .bss
    .globl a
    a:
        .space 4194304
    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -16
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, -12(fp)
_L1:
    li t0, 1048576
    lw t1, -12(fp)
    slt t2, t1, t0
    sw t1, -12(fp)
    beq x0, t2, _L3
    li t0, 1048576
    lw t1, -12(fp)
    sub t2, t0, t1
    la t0, a
    mv t3, t0
    li t4, 4
    mul t4, t4, t1
    add t3, t3, t4
    sw t2, 0(t3)
    sw t1, -12(fp)
    sw t0, -16(fp)
_L2:
    li t0, 1
    lw t1, -12(fp)
    add t2, t0, t1
    mv t1, t2
    sw t1, -12(fp)
    j _L1
_L3:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 142123
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    mv t1, t0
    li t0, 564432
    li t3, 4
    mul t3, t3, t0
    add t1, t1, t3
    lw t0, 0(t1)
    add t1, t2, t0
    mv a0, t1
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

