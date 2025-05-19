<CsoundSynthesizer>
<CsOptions>
-odac                ; Вывод звука в динамики (audio output)
-d                   ; Без графики, чище лог
</CsOptions>

<CsInstruments>
sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    aL, aR diskin2 "myfile.wav", 1, 0, 1
    outs aL, aR
endin
</CsInstruments>

<CsScore>
i1 0 10
</CsScore>
</CsoundSynthesizer>