
PLUGINNAME = zoomrc

VERSION=$(shell cat src/metadata.txt | awk -F '=' '/^version/{print $$NF}')

package:
	rm -f build/$(PLUGINNAME)*.zip
	mkdir -p build
	cp -r src build/$(PLUGINNAME)
	cp LICENSE README.md build/$(PLUGINNAME)/
	cd build && zip -9r $(PLUGINNAME)-$(VERSION).zip $(PLUGINNAME) && rm -rf $(PLUGINNAME)
	echo "Created package: $(PLUGINNAME)-$(VERSION).zip"
