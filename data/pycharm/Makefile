# Adopted for PyCharm by Andreas Bader <Development@Geekparadise.de>
# Originally written by Trygve Laugstøl <trygvis@inamo.no>
# TODO: Support publishing the packages and run dpkg-scanpackages
# TODO: Write notes on how to use
# TODO: Support for signing the packages

REPO ?= pycharm

ifeq ($(FLAVOR),community)
FLAVOR_LOWER=community
OTHER_FLAVOR=professional
OTHER_FLAVOR_LOWER=professional
else
FLAVOR_LOWER=professional
OTHER_FLAVOR=community
OTHER_FLAVOR_LOWER=community
endif

COUNT=$(words $(wildcard $(REPO)/pycharm-$(FLAVOR_LOWER)-$(VERSION)-*.deb))
REVISION=$(shell perl -e "print $(COUNT)+1")
V=$(VERSION)-$(REVISION)

PWD=$(shell pwd)
FAKEROOT=fakeroot -i fakeroot.save -s fakeroot.save

.PHONY: check-settings clean download $(REPO)/Packages.gz

all: check-settings $(REPO)/pycharm-$(FLAVOR_LOWER)-$(V).deb $(REPO)/Packages.gz

check-settings:
	@if [ -z "$(FLAVOR)" ]; then echo "Make sure FLAVOR is set when running make; for example: make FLAVOR=professional VERSION=4.5.3"; exit 1; fi
	@if [ "$(FLAVOR)" != "professional" -a "$(FLAVOR)" != "community" ]; then echo "Make sure FLAVOR is set to either 'professional' or 'community'."; exit 1; fi
	@if [ -z "$(VERSION)" ]; then echo "Make sure VERSION is set when running make; for example: make FLAVOR=community VERSION=4.5.3"; exit 1; fi
	@echo Parameters: version=$(VERSION), flavor=$(FLAVOR), revision=$(REVISION)

clean:
	@echo Cleaning
	@rm -rf root *.save

%.gz:%
	@echo GZ $<
	@gzip -c $< > $@

######################################################################
# Package Creation

download: download/pycharm-$(FLAVOR)-$(VERSION).tar.gz

download/pycharm-$(FLAVOR)-$(VERSION).tar.gz:
	@mkdir -p $(shell dirname $@)
	wget -O $@ http://download.jetbrains.com/python/pycharm-$(FLAVOR)-$(VERSION).tar.gz

root/usr/share/jetbrains/intellij-idea: download/pycharm-$(FLAVOR)-$(VERSION).tar.gz
	@echo Unpacking $?
	@mkdir -p $@
	@(cd $@; tar --strip-components 1 -zxf $(PWD)/$<)

root/usr/bin/idea: pycharm.in
	@echo Creating $@
	@mkdir -p $(shell dirname $@)
	@sed \
		-e "s,FLAVOR,$(FLAVOR)," \
		-e "s,VERSION,$(VERSION)," \
		$< > $@
	@chmod +x $@

root/DEBIAN/control: control.in
	@echo Creating $@
	@mkdir -p $(shell dirname $@)
	@sed \
		-e "s,OTHER_FLAVOR_LOWER,$(OTHER_FLAVOR_LOWER)," \
		-e "s,OTHER_FLAVOR,$(OTHER_FLAVOR)," \
		-e "s,FLAVOR_LOWER,$(FLAVOR_LOWER)," \
		-e "s,FLAVOR,$(FLAVOR)," \
		-e "s,VERSION,$(V)," \
		$< > $@

root/usr/share/applications/pycharm.desktop:
	@echo Installing $@
	@mkdir -p $(shell dirname $@)
	@cp pycharm.desktop $@

$(REPO)/pycharm-$(FLAVOR_LOWER)-$(V).deb: \
        clean \
        root/DEBIAN/control \
        root/usr/bin/pycharm \
        root/usr/share/applications/pycharm.desktop \
        root/usr/share/jetbrains/pycharm
	@mkdir -p $(REPO)
	@touch fakeroot.save
	@$(FAKEROOT) -- chown -R root:root root/
	@$(FAKEROOT) -- dpkg-deb -b root $@

######################################################################
# Package Repository

#	(cd $(REPO) && dpkg-scanpackages -m $(dir $@) /dev/null) > $@.new
$(REPO)/Packages:
	(cd $(REPO)/.. && dpkg-scanpackages -m $(shell basename $(abspath $(REPO))) /dev/null) > $@.new
	mv $@.new $@

$(REPO)/Packages.gz: $(REPO)/Packages
