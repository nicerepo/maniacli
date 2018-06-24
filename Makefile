SCRIPTS    = $(wildcard src/*.py)
CACHEDIR   = __pycache__
BUILDDIR   = build
DISTDIR    = dist
EXECUTABLE = maniacli

all:
	pyinstaller -n $(EXECUTABLE) --onefile --hidden-import=_cffi_backend $(SCRIPTS)

clean:
	-rm -rf $(CACHEDIR) $(BUILDDIR) $(DISTDIR)
	-rm -f $(EXECUTABLE).spec

install:
	install --strip $(DISTDIR)/$(EXECUTABLE) /usr/local/bin/
