    .data
    .globl sorted_after
    sorted_after:
        .word 500
    .bss
    .globl a
    a:
        .space 2000
    .data
    .globl state
    state:
        .word 0
    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -36
    # end of prologue
    
    # start of body
    li t0, 218397121
    mv t1, t0
    li t0, 0
    mv t1, t0
    sw t1, -12(fp)
_L1:
    la t0, sorted_after
    lw t1, 0(t0)
    lw t2, -12(fp)
    slt t3, t2, t1
    sw t2, -12(fp)
    sw t0, -16(fp)
    beq x0, t3, _L3
    addi sp, sp, 0
    call rand
    addi sp, sp, 0
    mv t0, a0
    la t1, a
    mv t2, t1
    li t3, 4
    lw t4, -12(fp)
    mul t3, t3, t4
    add t2, t2, t3
    sw t0, 0(t2)
    sw t4, -12(fp)
    sw t1, -20(fp)
_L2:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
    j _L1
_L3:
    li t0, 1
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t1, -24(fp)
    sw t2, -28(fp)
_L4:
    lw t0, -16(fp)
    lw t1, 0(t0)
    li t2, 1
    sub t3, t1, t2
    lw t1, -28(fp)
    slt t2, t1, t3
    sw t0, -16(fp)
    sw t1, -28(fp)
    beq x0, t2, _L6
    lw t0, -20(fp)
    mv t1, t0
    li t2, 4
    lw t3, -28(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t4, 1
    add t5, t3, t4
    li t4, 4
    mul t4, t4, t5
    add t1, t1, t4
    lw t4, 0(t1)
    sgt t1, t2, t4
    sw t0, -20(fp)
    sw t3, -28(fp)
    beq x0, t1, _L7
    li t0, 0
    mv t1, t0
    sw t1, -24(fp)
_L7:
_L5:
    li t0, 1
    lw t1, -28(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -28(fp)
    j _L4
_L6:
    lw t0, -16(fp)
    lw t1, 0(t0)
    sw t1, -4(sp)
    addi sp, sp, -4
    call bubblesort
    addi sp, sp, 4
    mv t0, a0
    li t0, 1
    mv t1, t0
    li t0, 0
    mv t2, t0
    sw t1, -32(fp)
    sw t2, -36(fp)
_L8:
    li t0, 1
    lw t1, -32(fp)
    sub t2, t1, t0
    lw t0, -36(fp)
    slt t3, t0, t2
    sw t1, -32(fp)
    sw t0, -36(fp)
    beq x0, t3, _L10
    lw t0, -20(fp)
    mv t1, t0
    li t2, 4
    lw t3, -36(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t4, 1
    add t5, t3, t4
    li t4, 4
    mul t4, t4, t5
    add t1, t1, t4
    lw t4, 0(t1)
    sgt t1, t2, t4
    sw t3, -36(fp)
    sw t0, -20(fp)
    beq x0, t1, _L11
    li t0, 0
    mv t1, t0
    sw t1, -32(fp)
_L11:
_L9:
    li t0, 1
    lw t1, -36(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -36(fp)
    j _L8
_L10:
    li t0, 200
    li t1, 10
    lw t2, -24(fp)
    mul t3, t2, t1
    add t1, t0, t3
    lw t0, -32(fp)
    add t2, t1, t0
    mv a0, t2
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 36
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
rand:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    la t0, state
    lw t1, 0(t0)
    li t2, 64013
    mul t3, t1, t2
    li t1, 1531011
    add t2, t3, t1
    li t1, 32768
    rem t3, t2, t1
    sw t3, 0(t0)
    mv t0, t3
    mv a0, t3
    j rand_exit
    # end of body
    
rand_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
swap:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -8
    # end of prologue
    
    # start of body
    la t0, a
    mv t1, t0
    li t2, 4
    lw t3, 0(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t2
    mv t2, t0
    li t4, 4
    lw t5, 4(fp)
    mul t4, t4, t5
    add t2, t2, t4
    lw t4, 0(t2)
    mv t2, t0
    li t6, 4
    mul t6, t6, t3
    add t2, t2, t6
    sw t4, 0(t2)
    mv t2, t0
    li t0, 4
    mul t0, t0, t5
    add t2, t2, t0
    sw t1, 0(t2)
    li a0, 0
    j swap_exit
    # end of body
    
swap_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
bubblesort:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -20
    # end of prologue
    
    # start of body
    li t0, 0
    mv t1, t0
    sw t1, -12(fp)
_L12:
    lw t0, -12(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -12(fp)
    beq x0, t2, _L14
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t0, t2
    sw t1, -12(fp)
    sw t0, -20(fp)
_L15:
    lw t0, -20(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -20(fp)
    beq x0, t2, _L17
    la t0, a
    mv t1, t0
    li t2, 4
    lw t3, -12(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t0, 4
    lw t4, -20(fp)
    mul t0, t0, t4
    add t1, t1, t0
    lw t0, 0(t1)
    sgt t1, t2, t0
    sw t3, -12(fp)
    sw t4, -20(fp)
    beq x0, t1, _L18
    lw t0, -12(fp)
    sw t0, -8(sp)
    lw t1, -20(fp)
    sw t1, -4(sp)
    sw t0, -12(fp)
    sw t1, -20(fp)
    addi sp, sp, -8
    call swap
    addi sp, sp, 8
    mv t0, a0
_L18:
_L16:
    li t0, 1
    lw t1, -20(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -20(fp)
    j _L15
_L17:
_L13:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
    j _L12
_L14:
    li a0, 0
    j bubblesort_exit
    # end of body
    
bubblesort_exit:
    # start of epilogue
    addi sp, sp, 20
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

