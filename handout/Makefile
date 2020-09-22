.PHONY: default dvi clean

default: INF_3200_F2020_Assignment1.pdf

dvi: default

clean:
	git clean -fX .

INF_3200_F2020_Assignment1.pdf: handout.pdf
	mv $< $@

.INTERMEDIATE: handout.pdf
handout.pdf: handout.tex general.bib
	pdflatex handout.tex
	biber handout
	pdflatex handout.tex
	pdflatex handout.tex
