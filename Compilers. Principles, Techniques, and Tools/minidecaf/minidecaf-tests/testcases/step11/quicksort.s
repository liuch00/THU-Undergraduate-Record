    .data
    .globl n
    n:
        .word 1000000
    .bss
    .globl a
    a:
        .space 4000000
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
    addi sp, sp, -16
    # end of prologue
    
    # start of body
    la t0, n
    lw t1, 0(t0)
    sw t1, -4(sp)
    sw t0, -12(fp)
    addi sp, sp, -4
    call initArr
    addi sp, sp, 4
    mv t0, a0
    lw t0, -12(fp)
    lw t1, 0(t0)
    sw t1, -4(sp)
    sw t0, -12(fp)
    addi sp, sp, -4
    call isSorted
    addi sp, sp, 4
    mv t0, a0
    mv t1, t0
    li t0, 0
    lw t2, -12(fp)
    lw t3, 0(t2)
    li t4, 1
    sub t5, t3, t4
    sw t0, -8(sp)
    sw t5, -4(sp)
    sw t1, -16(fp)
    sw t2, -12(fp)
    addi sp, sp, -8
    call qsort
    addi sp, sp, 8
    mv t0, a0
    lw t0, -12(fp)
    lw t3, 0(t0)
    sw t3, -4(sp)
    addi sp, sp, -4
    call isSorted
    addi sp, sp, 4
    mv t0, a0
    mv t1, t0
    li t0, 0
    lw t2, -16(fp)
    sub t3, t2, t0
    seqz t3, t3
    li t0, 1
    sub t2, t1, t0
    seqz t2, t2
    and t0, t3, t2
    seqz t1, t0
    beq x0, t1, _L1
    li t0, 1
    mv a0, t0
    j main_exit
_L1:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
qsort:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -32
    # end of prologue
    
    # start of body
    lw t0, 0(fp)
    mv t1, t0
    lw t2, 4(fp)
    mv t3, t2
    la t4, a
    mv t5, t4
    add t6, t0, t2
    li a0, 2
    div a1, t6, a0
    li t6, 4
    mul t6, t6, a1
    add t5, t5, t6
    lw t6, 0(t5)
    mv t5, t6
    li t6, 1
    mv a0, t6
    sw t0, -12(fp)
    sw t2, -16(fp)
    sw t1, -20(fp)
    sw t3, -24(fp)
    sw t5, -28(fp)
    sw t4, -32(fp)
_L2:
    lw t0, -20(fp)
    lw t1, -24(fp)
    sgt t2, t0, t1
    seqz t2, t2
    sw t0, -20(fp)
    sw t1, -24(fp)
    beq x0, t2, _L4
_L5:
    lw t0, -32(fp)
    mv t1, t0
    li t2, 4
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    lw t1, -28(fp)
    slt t4, t2, t1
    sw t3, -20(fp)
    sw t1, -28(fp)
    sw t0, -32(fp)
    beq x0, t4, _L7
    li t0, 1
    lw t1, -20(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -20(fp)
_L6:
    j _L5
_L7:
_L8:
    lw t0, -32(fp)
    mv t1, t0
    li t2, 4
    lw t3, -24(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    lw t1, -28(fp)
    sgt t4, t2, t1
    sw t3, -24(fp)
    sw t1, -28(fp)
    sw t0, -32(fp)
    beq x0, t4, _L10
    li t0, 1
    lw t1, -24(fp)
    sub t2, t1, t0
    mv t1, t2
    sw t1, -24(fp)
_L9:
    j _L8
_L10:
    lw t0, -20(fp)
    lw t1, -24(fp)
    sgt t2, t0, t1
    sw t0, -20(fp)
    sw t1, -24(fp)
    beq x0, t2, _L11
    j _L4
_L11:
    lw t0, -32(fp)
    mv t1, t0
    li t2, 4
    lw t3, -20(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t2
    mv t2, t0
    li t4, 4
    lw t5, -24(fp)
    mul t4, t4, t5
    add t2, t2, t4
    lw t4, 0(t2)
    mv t2, t0
    li t6, 4
    mul t6, t6, t3
    add t2, t2, t6
    sw t4, 0(t2)
    mv t2, t0
    li t4, 4
    mul t4, t4, t5
    add t2, t2, t4
    sw t1, 0(t2)
    li t1, 1
    add t2, t3, t1
    mv t3, t2
    li t1, 1
    sub t2, t5, t1
    mv t5, t2
    sw t3, -20(fp)
    sw t5, -24(fp)
    sw t0, -32(fp)
_L3:
    j _L2
_L4:
    lw t0, -20(fp)
    lw t1, 4(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -20(fp)
    beq x0, t2, _L12
    lw t0, -20(fp)
    sw t0, -8(sp)
    lw t0, 4(fp)
    sw t0, -4(sp)
    addi sp, sp, -8
    call qsort
    addi sp, sp, 8
    mv t0, a0
_L12:
    lw t0, -24(fp)
    lw t1, 0(fp)
    sgt t2, t0, t1
    sw t1, -12(fp)
    sw t0, -24(fp)
    beq x0, t2, _L13
    lw t0, 0(fp)
    sw t0, -8(sp)
    lw t0, -24(fp)
    sw t0, -4(sp)
    addi sp, sp, -8
    call qsort
    addi sp, sp, 8
    mv t0, a0
_L13:
    li a0, 0
    j qsort_exit
    # end of body
    
qsort_exit:
    # start of epilogue
    addi sp, sp, 32
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
    mv t1, t3
    lw t1, 0(t0)
    li t0, 1000
    rem t2, t1, t0
    mv a0, t2
    j rand_exit
    # end of body
    
rand_exit:
    # start of epilogue
    addi sp, sp, 8
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
initArr:
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
_L14:
    lw t0, -12(fp)
    lw t1, 0(fp)
    slt t2, t0, t1
    sw t1, -16(fp)
    sw t0, -12(fp)
    beq x0, t2, _L16
    addi sp, sp, 0
    call rand
    addi sp, sp, 0
    mv t0, a0
    la t1, a
    mv t2, t1
    li t1, 4
    lw t3, -12(fp)
    mul t1, t1, t3
    add t2, t2, t1
    sw t0, 0(t2)
    li t0, 1
    add t1, t3, t0
    mv t3, t1
    sw t3, -12(fp)
_L15:
    j _L14
_L16:
    li a0, 0
    j initArr_exit
    # end of body
    
initArr_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    
isSorted:
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
_L17:
    li t0, 1
    lw t1, 0(fp)
    sub t2, t1, t0
    lw t0, -12(fp)
    slt t3, t0, t2
    sw t1, -16(fp)
    sw t0, -12(fp)
    beq x0, t3, _L19
    la t0, a
    mv t1, t0
    li t2, 4
    lw t3, -12(fp)
    mul t2, t2, t3
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t0, 1
    add t4, t3, t0
    li t0, 4
    mul t0, t0, t4
    add t1, t1, t0
    lw t0, 0(t1)
    sgt t1, t2, t0
    sw t3, -12(fp)
    beq x0, t1, _L20
    li t0, 0
    mv a0, t0
    j isSorted_exit
_L20:
    li t0, 1
    lw t1, -12(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -12(fp)
_L18:
    j _L17
_L19:
    li t0, 1
    mv a0, t0
    j isSorted_exit
    # end of body
    
isSorted_exit:
    # start of epilogue
    addi sp, sp, 16
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

