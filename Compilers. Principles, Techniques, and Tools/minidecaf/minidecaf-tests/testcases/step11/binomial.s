    .bss
    .globl C
    C:
        .space 80000
    .data
    .globl P
    P:
        .word 10000007
    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -32
    # end of prologue
    
    # start of body
    li t0, 5996
    mv t1, t0
    li t0, 1
    la t2, C
    mv t3, t2
    li t4, 0
    li t5, 40000
    mul t5, t5, t4
    add t3, t3, t5
    li t4, 0
    li t5, 4
    mul t5, t5, t4
    add t3, t3, t5
    sw t0, 0(t3)
    li t0, 0
    mv t3, t0
    li t0, 1
    mv t4, t0
    sw t1, -12(fp)
    sw t2, -16(fp)
    sw t3, -20(fp)
    sw t4, -24(fp)
_L1:
    lw t0, -24(fp)
    lw t1, -12(fp)
    sgt t2, t0, t1
    seqz t2, t2
    sw t1, -12(fp)
    sw t0, -24(fp)
    beq x0, t2, _L3
    li t0, 0
    mv t1, t0
    sw t1, -28(fp)
_L4:
    lw t0, -28(fp)
    lw t1, -24(fp)
    sgt t2, t0, t1
    seqz t2, t2
    sw t1, -24(fp)
    sw t0, -28(fp)
    beq x0, t2, _L6
    lw t0, -28(fp)
    seqz t1, t0
    sw t0, -28(fp)
    beq x0, t1, _L8
    li t0, 1
    mv t1, t0
    sw t1, -32(fp)
    j _L7
_L8:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 4
    lw t4, -28(fp)
    mul t2, t2, t4
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t5, 40000
    mul t5, t5, t3
    add t1, t1, t5
    li t5, 1
    sub t6, t4, t5
    li t5, 4
    mul t5, t5, t6
    add t1, t1, t5
    lw t5, 0(t1)
    add t1, t2, t5
    la t2, P
    lw t5, 0(t2)
    rem t2, t1, t5
    mv t1, t2
    sw t0, -16(fp)
    sw t3, -20(fp)
    sw t4, -28(fp)
    sw t1, -32(fp)
_L7:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 1
    lw t3, -20(fp)
    sub t4, t2, t3
    li t2, 40000
    mul t2, t2, t4
    add t1, t1, t2
    li t2, 4
    lw t4, -28(fp)
    mul t2, t2, t4
    add t1, t1, t2
    lw t2, -32(fp)
    sw t2, 0(t1)
    sw t0, -16(fp)
    sw t3, -20(fp)
    sw t4, -28(fp)
_L5:
    li t0, 1
    lw t1, -28(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -28(fp)
    j _L4
_L6:
    li t0, 1
    lw t1, -20(fp)
    sub t2, t0, t1
    mv t1, t2
    sw t1, -20(fp)
_L2:
    li t0, 1
    lw t1, -24(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -24(fp)
    j _L1
_L3:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 0
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 1
    sub t4, t2, t1
    snez t4, t4
    mv t1, t0
    li t2, 40000
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 4
    lw t5, -12(fp)
    mul t2, t2, t5
    add t1, t1, t2
    lw t2, 0(t1)
    li t1, 1
    sub t6, t2, t1
    snez t6, t6
    or t1, t4, t6
    mv t2, t0
    li t4, 1
    sub t6, t4, t3
    li t4, 40000
    mul t4, t4, t6
    add t2, t2, t4
    li t4, 1
    li t6, 4
    mul t6, t6, t4
    add t2, t2, t6
    lw t4, 0(t2)
    li t2, 1
    sub t6, t5, t2
    sub t2, t4, t6
    snez t2, t2
    or t4, t1, t2
    sw t5, -12(fp)
    sw t0, -16(fp)
    sw t3, -20(fp)
    beq x0, t4, _L9
    li t0, 1
    mv a0, t0
    j main_exit
_L9:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 1234
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 6188476
    sub t4, t2, t1
    snez t4, t4
    sw t0, -16(fp)
    sw t3, -20(fp)
    beq x0, t4, _L10
    li t0, 2
    mv a0, t0
    j main_exit
_L10:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 2333
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 9957662
    sub t4, t2, t1
    snez t4, t4
    sw t0, -16(fp)
    sw t3, -20(fp)
    beq x0, t4, _L11
    li t0, 3
    mv a0, t0
    j main_exit
_L11:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 3456
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 9832509
    sub t4, t2, t1
    snez t4, t4
    sw t0, -16(fp)
    sw t3, -20(fp)
    beq x0, t4, _L12
    li t0, 4
    mv a0, t0
    j main_exit
_L12:
    lw t0, -16(fp)
    mv t1, t0
    li t2, 40000
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 5678
    li t4, 4
    mul t4, t4, t2
    add t1, t1, t4
    lw t2, 0(t1)
    li t1, 2436480
    sub t4, t2, t1
    snez t4, t4
    sw t0, -16(fp)
    sw t3, -20(fp)
    beq x0, t4, _L13
    li t0, 5
    mv a0, t0
    j main_exit
_L13:
    lw t0, -16(fp)
    mv t1, t0
    li t0, 40000
    lw t2, -20(fp)
    mul t0, t0, t2
    add t1, t1, t0
    li t0, 2
    lw t2, -12(fp)
    div t3, t2, t0
    li t0, 4
    mul t0, t0, t3
    add t1, t1, t0
    lw t0, 0(t1)
    li t1, 7609783
    sub t2, t0, t1
    snez t2, t2
    beq x0, t2, _L14
    li t0, 6
    mv a0, t0
    j main_exit
_L14:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 32
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

