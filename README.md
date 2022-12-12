# nonmodel_genome
Basic data processing of a new non-model genome

Make sure all your input files are in RefSeq ID format "GCF........", and these point to genome assemblies, that are stored in 
`Example.csv`. There is an example in the repo.


Run with:
```
./nextflow run main.nf -profile docker/myriad -bg -resume --input Example.csv
```

Then in Results, you should have all the gffread outputs, plus orthofinder.


# Testing

To run an individual module on Gitpod use the following:

`docker run --volume $PWD:$PWD -it chriswyatt/bioseqio workspace/nonmodel_genome/bin/ncbi_gffread_to_gene.pl`