.SUFFIXES: .puml .png

docName = tfg
outputFolder = out

texFiles = tex/tfg.tex tex/introduction.tex tex/previousWorks.tex tex/interface.tex tex/implementation.tex
diagramImgs = diagrams/gameRepresentation.png diagrams/modules.png diagrams/sgfModule.png diagrams/gtpEngine.png

all: $(docName).pdf

$(docName).pdf: $(texFiles) $(diagramImgs)
	[ -d $(outputFolder) ] || mkdir $(outputFolder)
	xelatex -output-directory $(outputFolder) tex/$(docName).tex
	biber $(outputFolder)/$(docName)
	xelatex -output-directory $(outputFolder) tex/$(docName).tex
	mv $(outputFolder)/$(docName).pdf .

.puml.png:
	plantuml $<

clean:
	rm -r $(outputFolder)
	rm diagrams/*.png
