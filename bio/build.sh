rm *.acn
rm *.alg
rm *.bbl
rm *.glg
rm *.gls
rm *.log
rm *.pdf
rm *.toc
rm *.acr
rm *.aux
rm *.blg
rm *.glo
rm *.idx
rm *.out
rm *.xdy

xelatex 00_summary
xelatex 00_summary
bibtex 00_summary
xelatex 00_summary
xelatex 00_summary
makeglossaries 00_summary
xelatex 00_summary

xelatex 01_bio
xelatex 01_bio
bibtex 01_bio
xelatex 01_bio
xelatex 01_bio
makeglossaries 01_bio
xelatex 01_bio

xelatex 02_education
xelatex 02_education
bibtex 02_education
xelatex 02_education
xelatex 02_education
makeglossaries 02_education
xelatex 02_education

xelatex 03_progress
xelatex 03_progress
bibtex 03_progress
xelatex 03_progress
xelatex 03_progress
makeglossaries 03_progress
xelatex 03_progress

xelatex 04_lplan
xelatex 04_lplan
bibtex 04_lplan
xelatex 04_lplan
xelatex 04_lplan
makeglossaries 04_lplan
xelatex 04_lplan

xelatex 05_rplan
xelatex 05_rplan
bibtex 05_rplan
xelatex 05_rplan
xelatex 05_rplan
makeglossaries 05_rplan
xelatex 05_rplan

mkdir -p dist
mv *.pdf dist
cp ../journey/journey.pdf dist/06_journey.pdf
cp ../epanl/epanlz.pdf dist/07_epanlz.pdf
