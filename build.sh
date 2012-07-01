#!/usr/bin/zsh

function build() {
  input=$1
  mkdir -p .$input.tex_files
  cd .$input.tex_files
  TEXINPUTS=.:..:../images/:../figures/: xelatex $input
  BSTINPUTS=:..: BIBINPUTS=:..:.: biber $input
  cp $input.pdf ..
  cd ..
}
build paper
