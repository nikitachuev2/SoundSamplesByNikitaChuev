<CsoundSynthesizer>
<CsOptions>
-odac
</CsOptions>

<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    aSig diskin2 "myfile.wav", 1, 0, 1

    kX chnget "posx"
    ; Простое панорамирование: -1 = влево, 1 = вправо, 0 = центр
    kpan = tanh(kX / 5)  ; нормализация для плавного панорамирования

    aL, aR pan2 aSig, kpan
    outs aL, aR
endin
</CsInstruments>

<CsScore>
i 1 0 60
</CsScore>
</CsoundSynthesizer>
