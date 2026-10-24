SHELL := /usr/bin/env bash

.PHONY: help doctor fetch customize test build package clean

help:
	@printf '%s
' 	  'make doctor     Check Fedora/toolchain prerequisites' 	  'make fetch      Fetch the pinned Euro-Office Lite source' 	  'make customize  Apply OsiX branding and Fedora bundle config' 	  'make test       Run OsiX bootstrap and OOXML tests' 	  'make build      Build OsiX Office RPM + AppImage' 	  'make package    Copy built artifacts into dist/' 	  'make clean      Remove generated work and artifacts'

doctor:
	./scripts/00-doctor.sh

fetch:
	./scripts/02-fetch-base.sh

customize:
	./scripts/03-customize.sh

test:
	python3 -m unittest discover -s tests -p 'test_*.py' -v

build:
	./scripts/04-build.sh

package:
	./scripts/06-collect-artifacts.sh

clean:
	rm -rf work
	find dist -mindepth 1 ! -name .gitkeep -delete
