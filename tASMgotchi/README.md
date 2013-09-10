tASMgotchi

tASMgotchi.py <infile> <images> <outfile>

Convenience functions:

Display an image

LDA #0
JSR display_image

Displays image from your <images> file at the index in a

clear LCD

JSR clear_lcd

Read port A (buttons) into A, debounced

JSR read_a