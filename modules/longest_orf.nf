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
        head -n 1 ${fasta} > tbd
        if grep -q ; tbd; then
            ncbi_gffread_to_gene.pl ${fasta}
        else
            ncbi_gffread_to_gene_augustus.pl ${fasta}
        fi
        
    """
}