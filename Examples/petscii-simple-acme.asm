;; using the ca65 assembler (part of the cc65 toolchain,
;;; see https://github.com/cc65/cc65 for downloads).
;;;
;;; target platform: Commander X16, Sept 2019 design
;;; test platform: cx16emu r.32
;;; dev host platform: Ryzen 3 2200g PC running Manjaro Linux
;;;
;;;
;;; Uses the Kernal print-character routine to print all of the
;;; characters of the first character set (40 hex to 7F hex).
;;;
;;; Since this was just a quick demo, I kept it simple,
;;; with all of the constants as local equates rather than
;;; using a separate header (as I plan to do with future programs).
;;;
;;; to assemble:
;;;    ca65 petscii-simple.asm -o petscii-simple.o -l petscii-simple.lst
;;; 
;;;   acme -f cbm -DMACHINE_C64=0 -o petscii-simple-acme.prg petscii-simple-acme.asm
;;; 
;;; link:
;;;    cl65 petscii-simple.o -C cx16-asm.cfg -o petscii-simple.prg
;;; run:
;;; /Applications/x16emu_mac-r33/x16emu -prg petscii-simple.prg -run
;;;    x16emu -prg petscii-simple.prg -run

;;; constants
Kernal_bank   = $07
ROM_bank_ctrl = $9F61
BSOUT         = $FFD2

;; ca65
;; .org  $0801

; acme
*=  $0801

; acme
;; common header for binary executable PRGs
!byte $0b,$08,$01,$00,$9e,$32,$30,$36,$31,$00,$00,$00

;; ca65
;; common header for binary executable PRGs
;; .byte $0b,$08,$01,$00,$9e,$32,$30,$36,$31,$00,$00,$00

start:
      ; initialize the ROM Bank to 'kernal'
      ; while this is not strictly necessary since
      ; the BASIC ROM also includes the Kernal ROM,
      ; I wanted to make sure I had the procedure correct
      lda #Kernal_bank       ; get the bank ID #
      sta ROM_bank_ctrl      ; set the bank control

      ; print out all of the characts of the primary code set
      lda #$40               ; load the character '@'
loop:
      jsr BSOUT              ; print the current char
      adc #1                 ; increment the accumulator
      cmp #$7F               ; are we at the end of the codeset?
      bne loop               ; if not, loop
exit:
      rts