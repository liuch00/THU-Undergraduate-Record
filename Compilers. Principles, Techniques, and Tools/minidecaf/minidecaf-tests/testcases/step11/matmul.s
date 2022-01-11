    .bss
    .globl a
    a:
        .space 16
    .bss
    .globl b
    b:
        .space 16
    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -20
    # end of prologue
    
    # start of body
    li t0, 2
    sw t0, -4(sp)
    addi sp, sp, -4
    call initMatrix
    addi sp, sp, 4
    mv t0, a0
    li t0, 2
    sw t0, -4(sp)
    addi sp, sp, -4
    call mulMatrix
    addi sp, sp, 4
    mv t0, a0
    li t0, 0
    mv t1, t0
    sw t1, -12(fp)
_L1:
    li t0, 2
    lw t1, -12(fp)
    slt t2, t1, t0
    sw t1, -12(fp)
    beq x0, t2, _L3
    li t0, 0
    mv t1, t0
    sw t1, -16(fp)
_L4:
    li t0, 2
    lw t1, -16(fp)
    slt t2, t1, t0
    sw t1, -16(fp)
    beq x0, t2, _L6
    la t0, b
    mv t1, t0
    li t2, 8
    lw t3, -12(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 4
    lw t4, -16(fp)
    mul t2, t2, t4
    add t1, t1, t2
    lw t2, 0(t1)
    la t1, a
    mv t5, t1
    li t1, 8
    mul t1, t1, t3
    add t5, t5, t1
    li t1, 4
    mul t1, t1, t4
    add t5, t5, t1
    sw t2, 0(t5)
    li t1, 0
    mv t2, t0
    li t5, 8
    mul t5, t5, t3
    add t2, t2, t5
    li t5, 4
    mul t5, t5, t4
    add t2, t2, t5
    sw t1, 0(t2)
    sw t3, -12(fp)
    sw t4, -16(fp)
    sw t0, -20(fp)
_L5:
    li t0, 1
    lw t1, -16(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -16(fp)
    j _L4
_L6:
_L2:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
    j _L1
_L3:
    li t0, 2
    sw t0, -4(sp)
    addi sp, sp, -4
    call mulMatrix
    addi sp, sp, 4
    mv t0, a0
    lw t0, -20(fp)
    mv t1, t0
    li t2, 0
    li t3, 8
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 199
    sub t3, t2, t1
    snez t3, t3
    sw t0, -20(fp)
    beq x0, t3, _L7
    li t0, 1
    mv a0, t0
    j main_exit
_L7:
    lw t0, -20(fp)
    mv t1, t0
    li t2, 0
    li t3, 8
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 1
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 290
    sub t3, t2, t1
    snez t3, t3
    sw t0, -20(fp)
    beq x0, t3, _L8
    li t0, 2
    mv a0, t0
    j main_exit
_L8:
    lw t0, -20(fp)
    mv t1, t0
    li t2, 1
    li t3, 8
    mul t3, t3, t2
    add t1, t1, t3
    li t2, 0
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 435
    sub t3, t2, t1
    snez t3, t3
    sw t0, -20(fp)
    beq x0, t3, _L9
    li t0, 3
    mv a0, t0
    j main_exit
_L9:
    lw t0, -20(fp)
    mv t1, t0
    li t0, 1
    li t2, 8
    mul t2, t2, t0
    add t1, t1, t2
    li t0, 1
    li t2, 4
    mul t2, t2, t0
    add t1, t1, t2
    lw t0, 0(t1)
    li t1, 634
    sub t2, t0, t1
    snez t2, t2
    beq x0, t2, _L10
    li t0, 4
    mv a0, t0
    j main_exit
_L10:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 20
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
mulMatrix:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -28
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, -12(fp)
_L11:
    lw t0, -12(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -12(fp)
    beq x0, t2, _L13
    li t0, 0
    mv t1, t0
    sw t1, -20(fp)
_L14:
    lw t0, -20(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -20(fp)
    beq x0, t2, _L16
    li t0, 0
    la t1, b
    mv t2, t1
    li t3, 8
    lw t4, -12(fp)
    mul t3, t3, t4
    add t2, t2, t3
    li t3, 4
    lw t5, -20(fp)
    mul t3, t3, t5
    add t2, t2, t3
    sw t0, 0(t2)
    li t0, 0
    mv t2, t0
    sw t4, -12(fp)
    sw t5, -20(fp)
    sw t2, -24(fp)
    sw t1, -28(fp)
_L17:
    lw t0, -24(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -24(fp)
    beq x0, t2, _L19
    lw t0, -28(fp)
    mv t1, t0
    li t2, 8
    lw t3, -12(fp)
    mul t2, t2, t3
    add t1, t1, t2
    li t2, 4
    lw t4, -20(fp)
    mul t2, t2, t4
    add t1, t1, t2
    lw t2, 0(t1)
    la t1, a
    mv t5, t1
    li t6, 8
    mul t6, t6, t3
    add t5, t5, t6
    li t6, 4
    lw a0, -24(fp)
    mul t6, t6, a0
    add t5, t5, t6
    lw t6, 0(t5)
    mv t5, t1
    li t1, 8
    mul t1, t1, a0
    add t5, t5, t1
    li t1, 4
    mul t1, t1, t4
    add t5, t5, t1
    lw t1, 0(t5)
    mul t5, t6, t1
    add t1, t2, t5
    mv t2, t0
    li t5, 8
    mul t5, t5, t3
    add t2, t2, t5
    li t5, 4
    mul t5, t5, t4
    add t2, t2, t5
    sw t1, 0(t2)
    li t1, 1
    add t2, a0, t1
    mv a0, t2
    sw t3, -12(fp)
    sw t4, -20(fp)
    sw a0, -24(fp)
    sw t0, -28(fp)
_L18:
    j _L17
_L19:
    li t0, 1
    lw t1, -20(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -20(fp)
_L15:
    j _L14
_L16:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
_L12:
    j _L11
_L13:
    li a0, 0
    j mulMatrix_exit
    # end of body
    
mulMatrix_exit:
    # start of epilogue
    addi sp, sp, 28
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
initMatrix:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -20
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t2, -12(fp)
    sw t1, -16(fp)
_L20:
    li t0, 2
    lw t1, -12(fp)
    slt t2, t1, t0
    sw t1, -12(fp)
    beq x0, t2, _L22
    li t0, 0
    mv t1, t0
    sw t1, -20(fp)
_L23:
    li t0, 2
    lw t1, -20(fp)
    slt t2, t1, t0
    sw t1, -20(fp)
    beq x0, t2, _L25
    li t0, 1
    lw t1, -16(fp)
    add t2, t1, t0
    mv t1, t2
    la t0, a
    mv t2, t0
    li t0, 8
    lw t3, -12(fp)
    mul t0, t0, t3
    add t2, t2, t0
    li t0, 4
    lw t4, -20(fp)
    mul t0, t0, t4
    add t2, t2, t0
    sw t1, 0(t2)
    li t0, 1
    add t2, t4, t0
    mv t4, t2
    sw t3, -12(fp)
    sw t4, -20(fp)
    sw t1, -16(fp)
_L24:
    j _L23
_L25:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
_L21:
    j _L20
_L22:
    li a0, 0
    j initMatrix_exit
    # end of body
    
initMatrix_exit:
    # start of epilogue
    addi sp, sp, 20
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

