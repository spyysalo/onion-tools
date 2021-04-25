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
make && make install
cd -
```

Add to path (you may want to add this to e.g. `$HOME/.bash_profile`)

```
export PATH=$PATH:$HOME/local/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/local/lib
```

Run on example data

```
git clone https://github.com/spyysalo/onion-tools.git
cd onion-tools
python3 tsv_to_vert.py example-data/fi.tsv > fi.vert
onion fi.vert > fi.vert.onion
```

Get IDs and separate fully duplicated documents

```
python3 doc_duprate.py fi.vert.onion | egrep '^1\.0' | cut -f 2 > fi-dup-ids.txt
fgrep -f fi-dup-ids.txt example-data/fi.tsv > fi-dup.tsv
fgrep -v -f fi-dup-ids.txt example-data/fi.tsv > fi-dedup.tsv
```

This should result in the following:

```
wc -l fi-{dup,dedup}.tsv
    248 fi-dup.tsv
    752 fi-dedup.tsv
   1000 total
```
