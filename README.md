# nonmodel_genome

Basic data processing of a new non-model genome.
This repo will download genomes and assemblies, extract gene/protein sequences and run orthofinder.

--input example (species_name COMMA Refseq ID):
```
A_mellifera,GCF_003254395.2
D_melanogaster,GCA_000001215.4
P_exclamans,GCA_023678865.1
P_fuscatus,GCF_010416935.1
```

Make sure all your input files are in RefSeq ID format "GCF........", and these point to the expected genome assembly formats (though some GCA version will work too).

You can also input your own local GFF and genome files like so:

--input example (species_name COMMA path_to_genome COMMA path_to_gff3_file)
```
B_impatiens,/workspace/nonmodel_genome/B_impatiensGenome.FINAL.fasta.gz,/workspace/nonmodel_genome/B_impatiens.gff.gz
```

*Choose a profile, either docker (if local), myriad (on ucl cluster), or gitpod (if using the gitpod env)

# Run with nextflow *test* data:
```
nextflow run chriswyatt1/nonmodel_genome -profile docker/myriad/gitpod,test -bg -resume 
```

OR clone the repo (git clone https://github.com/chriswyatt1/nonmodel_genome.git) 
and run:
```
./nextflow run main.nf -profile docker/myriad/gitpod,test -bg -resume --input Example.csv
```

# Run with your own data:

```
nextflow run chriswyatt1/nonmodel_genome -profile docker/myriad/gitpod -bg -resume --input /path/to/Example.csv
```

See Example.csv for expected input format.


# Results

Then in Results, you should have all the gffread outputs, plus orthofinder.


# Testing

To run an individual module on Gitpod use the following:

`docker run --volume $PWD:$PWD -it chriswyatt/bioseqio workspace/nonmodel_genome/bin/ncbi_gffread_to_gene.pl`