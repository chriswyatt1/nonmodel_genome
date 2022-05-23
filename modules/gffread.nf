process GFFREAD {
    label 'gffread'
    tag "$sample_id"
    container = 'chriswyatt/gffread_python3'
    publishDir "$params.outdir/$sample_id" , mode: "copy"
             
    input:

        tuple val(sample_id), path(fasta), path(gff)

    output:

        path( "${sample_id}.prot.fa" ), path( "${sample_id}.cds.fa" ), path( "${sample_id}.protcds.fa" ) , path( "${sample_id}.gff_for_jvci.gff3" ), emit: proteins

    script:
    """
    
    #Convert Augustus gff files if found, then do gffread to print out the nucleotide files for each gene.

    head -n 1 $gff > tbd

    if grep -q AUGUSTUS tbd; then 
        python3 $projectDir/bin/convert_augustus_to_gffs.py -i ${gff} -o ${sample_id}.gff_for_jvci.gff3
    else
        mv ${gff} ${sample_id}.gff_for_jvci.gff3
    fi

    gffread -w ${sample_id}.prot.fa -g ${fasta} ${sample_id}.gff_for_jvci.gff3
    gffread -x ${sample_id}.cds.fa -g ${fasta} ${sample_id}.gff_for_jvci.gff3
	gffread -y ${sample_id}.protcds.fa -g ${fasta} ${sample_id}.gff_for_jvci.gff3

    """
}


    
