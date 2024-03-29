process ORTHOFINDER {
    label 'orthofinder'
    publishDir "$params.outdir/Orthofinder/"
    container = 'davidemms/orthofinder:2.5.4'
    //stageInMode 'copy'
    
    input:
        path '*'
               
    output:
        path("My_result/*/Orthogroups/Orthogroups.tsv") , emit: orthologues

    script:
    """
        count=`ls -1 *.gz 2>/dev/null | wc -l`
        if [ \$count != 0 ]
        then
	    gunzip *.gz
        fi
	    orthofinder -f . -o My_result
    """
}