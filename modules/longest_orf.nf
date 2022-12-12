process LONGEST {
    label 'longest'
    tag "$fasta"
    container = 'chriswyatt/bioseqio'
    publishDir "$params.outdir/" , mode: "copy"
             
    input:

        path(fasta)

    output:

        path( "${fasta}.largestIsoform.fa" )

    script:
    """
        ncbi_gffread_to_gene_universal.pl ${fasta}
    """
}