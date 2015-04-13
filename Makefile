GEN_CHANNELS := "channels-list.md"

MMD_SOURCE := $(wildcard *.md) $(GEN_CHANNELS)
HTML_OUTPUT := $(MMD_SOURCE:.md=.html)

.PHONY: all clean

all: $(HTML_OUTPUT)

%.html: %.md
	awk 'BEGIN{print "CSS: res/api-doc.css"}{print}' $< | sed 's/\.md/.html/g' | multimarkdown 2>/dev/null | xsltproc --encoding utf-8 res/toc.xslt - > $@

$(GEN_CHANNELS):
	./scripts/gen-channels.py $@

clean:
	-rm *.html
