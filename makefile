# Directories
SRC			= src/

# Files
latexfile	= report
figures		=
files		=

$(latexfile).pdf: $(SRC)$(latexfile).tex $(figures) $(files)
	rubber --pdf $(SRC)$(latexfile)


.PHONY: clean clean-full

clean:
	rubber --clean $(SRC)$(latexfile)


clean-full: clean
	rm -f $(latexfile).pdf
