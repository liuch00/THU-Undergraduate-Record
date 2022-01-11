    .text
    .global main
    
main:
    # start of prologue
    sw ra, -4(sp)
    sw fp, -8(sp)
    mv fp, sp
    addi sp, sp, -136
    # end of prologue
    
    # start of body
    li t0, 0
    addi t1, fp, -128
    mv t2, t1
    li t3, 0
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t0, 0(t2)
    li t0, 1
    mv t2, t1
    li t3, 1
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t0, 0(t2)
    li t0, 2
    mv t2, t0
    sw t2, -132(fp)
    sw t1, -136(fp)
_L1:
    li t0, 30
    lw t1, -132(fp)
    slt t2, t1, t0
    sw t1, -132(fp)
    beq x0, t2, _L3
    lw t0, -136(fp)
    mv t1, t0
    li t2, 2
    lw t3, -132(fp)
    sub t4, t3, t2
    li t2, 4
    mul t2, t2, t4
    add t1, t1, t2
    lw t2, 0(t1)
    mv t1, t0
    li t4, 1
    sub t5, t3, t4
    li t4, 4
    mul t4, t4, t5
    add t1, t1, t4
    lw t4, 0(t1)
    add t1, t2, t4
    mv t2, t0
    li t4, 4
    mul t4, t4, t3
    add t2, t2, t4
    sw t1, 0(t2)
    sw t3, -132(fp)
    sw t0, -136(fp)
_L2:
    li t0, 1
    lw t1, -132(fp)
    add t2, t1, t0
    mv t1, t2
    sw t1, -132(fp)
    j _L1
_L3:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 2
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 1
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L4
    li t0, 2
    mv a0, t0
    j main_exit
_L4:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 3
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 2
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L5
    li t0, 3
    mv a0, t0
    j main_exit
_L5:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 4
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 3
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L6
    li t0, 4
    mv a0, t0
    j main_exit
_L6:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 5
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 5
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L7
    li t0, 5
    mv a0, t0
    j main_exit
_L7:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 6
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 8
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L8
    li t0, 6
    mv a0, t0
    j main_exit
_L8:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 7
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 13
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L9
    li t0, 7
    mv a0, t0
    j main_exit
_L9:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 8
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 21
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L10
    li t0, 8
    mv a0, t0
    j main_exit
_L10:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 9
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 34
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L11
    li t0, 9
    mv a0, t0
    j main_exit
_L11:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 10
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 55
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L12
    li t0, 10
    mv a0, t0
    j main_exit
_L12:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 11
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 89
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L13
    li t0, 11
    mv a0, t0
    j main_exit
_L13:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 12
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 144
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L14
    li t0, 12
    mv a0, t0
    j main_exit
_L14:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 13
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 233
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L15
    li t0, 13
    mv a0, t0
    j main_exit
_L15:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 14
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 377
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L16
    li t0, 14
    mv a0, t0
    j main_exit
_L16:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 15
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 610
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L17
    li t0, 15
    mv a0, t0
    j main_exit
_L17:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 16
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 987
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L18
    li t0, 16
    mv a0, t0
    j main_exit
_L18:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 17
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 1597
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L19
    li t0, 17
    mv a0, t0
    j main_exit
_L19:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 18
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 2584
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L20
    li t0, 18
    mv a0, t0
    j main_exit
_L20:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 19
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 4181
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L21
    li t0, 19
    mv a0, t0
    j main_exit
_L21:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 20
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 6765
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L22
    li t0, 20
    mv a0, t0
    j main_exit
_L22:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 21
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 10946
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L23
    li t0, 21
    mv a0, t0
    j main_exit
_L23:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 22
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 17711
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L24
    li t0, 22
    mv a0, t0
    j main_exit
_L24:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 23
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 28657
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L25
    li t0, 23
    mv a0, t0
    j main_exit
_L25:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 24
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 46368
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L26
    li t0, 24
    mv a0, t0
    j main_exit
_L26:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 25
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 75025
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L27
    li t0, 25
    mv a0, t0
    j main_exit
_L27:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 26
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 121393
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L28
    li t0, 26
    mv a0, t0
    j main_exit
_L28:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 27
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 196418
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L29
    li t0, 27
    mv a0, t0
    j main_exit
_L29:
    lw t0, -136(fp)
    mv t1, t0
    li t2, 28
    li t3, 4
    mul t3, t3, t2
    add t1, t1, t3
    lw t2, 0(t1)
    li t1, 317811
    sub t3, t2, t1
    snez t3, t3
    sw t0, -136(fp)
    beq x0, t3, _L30
    li t0, 28
    mv a0, t0
    j main_exit
_L30:
    lw t0, -136(fp)
    mv t1, t0
    li t0, 29
    li t2, 4
    mul t2, t2, t0
    add t1, t1, t2
    lw t0, 0(t1)
    li t1, 514229
    sub t2, t0, t1
    snez t2, t2
    beq x0, t2, _L31
    li t0, 29
    mv a0, t0
    j main_exit
_L31:
    li t0, 0
    mv a0, t0
    j main_exit
    # end of body
    
main_exit:
    # start of epilogue
    addi sp, sp, 136
    lw ra, -4(sp)
    lw fp, -8(sp)
    # end of epilogue
    
    ret
    

