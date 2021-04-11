# onion-tools

Tools for text deduplication using the onion (ONe Instance ONly) tool (<http://corpus.tools/wiki/Onion>)

## Quickstart

Install libjudy locally (<http://judy.sourceforge.net/>)

```
git clone https://github.com/spyysalo/libjudy.git
cd libjudy
./configure --prefix=${HOME}/local
make && make check
make install
cd -
```

Install onion following instructions from <http://corpus.tools/wiki/Onion>

```
wget -O onion-1.2.tar.gz 'http://corpus.tools/raw-attachment/wiki/Downloads/onion-1.2.tar.gz'
tar xvzf onion-1.2.tar.gz 
cd onion-1.2
perl -p -i -e 's|^(PREFIX=).*|${1}'"$HOME"'/local|' Makefile.config 
perl -p -i -e 's|^#?(JUDY_INC=).*|${1}-I'"$HOME"'/local/include|' Makefile.config
perl -p -i -e 's|^#?(JUDY_LIB=).*|${1}-L'"$HOME"'/local/lib|' Makefile.config 
```

Add `onion` to path (you may want to add this line to e.g. `$HOME/.bash_profile`)

```
PATH=$PATH:$HOME/local/bin
```
