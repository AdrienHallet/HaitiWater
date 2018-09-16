FILES=$(wildcard *.tex)

all: pdf

%.pdf: %.tex
	latexmk -pdf $<
	latexmk -c $<

pdf: $(FILES)
	make $(FILES:tex=pdf)

clean:
	latexmk -CA
