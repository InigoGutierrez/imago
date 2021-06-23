.SUFFIXES: .puml .png

docName = tfg
outputFolder = out

texFiles = tex/tfg.tex tex/introduction.tex tex/planification.tex tex/interface.tex tex/implementation.tex tex/systemAnalysis.tex tex/biber.bib
diagramImgs = diagrams/gameRepresentation.png diagrams/gtpEngine.png diagrams/modules.png diagrams/planificationWorkPlanEngine.png diagrams/planificationWorkPlanGame.png diagrams/sgfModule.png diagrams/useCases.png diagrams/analysisClasses.png

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
