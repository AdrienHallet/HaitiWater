TARGET=thesis.tex

all: pdf

pdf: $(TARGET)
	latexmk -pdf $<
	latexmk -c $<

clean:
	latexmk -CA
