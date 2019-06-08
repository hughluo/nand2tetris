// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(LOOP)

    // init addr point to the first chunk
    @SCREEN
    D=A
    @addr
    M=D
    
    // if key pressed goto BLACKOUT
    @24576
    D=M
    @BLACKOUT
    D;JNE

    // else goto WHITEOUT

(WHITEOUT)
    // if loop through the screen, goto LOOP
    @addr
    D=M
    @24576
    D=D-A
    @LOOP
    D;JEQ

    // set that 16bit chunck of screen to white
    @addr
    A=M
    M=0
    
    // set addr pointer to the next chunck
    @addr
    M=M+1

    @WHITEOUT
    0;JMP


(BLACKOUT)
    // if loop through the screen, goto LOOP
    @addr
    D=M
    @24576
    D=D-A
    @LOOP
    D;JEQ

    // set that 16bit chunck of screen to black
    @addr
    A=M
    M=-1
    
    // set addr pointer to the next chunck
    @addr
    M=M+1

    @BLACKOUT
    0;JMP
