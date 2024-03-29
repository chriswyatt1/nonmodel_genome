#!/usr/bin/env python3

import argparse
import re

from biocode import gff, things

'''
This script converts native (GTF) or GFF output (via the --gff3 option) of Augustus
into GFF3 format.
'''

def main():
    parser = argparse.ArgumentParser( description='Convert native (GTF) or GFF output from Augustus into GFF3 format')

    ## output file to be written
    parser.add_argument('-i', '--input', type=str, required=True, help='Path to a GFF file created by Augustus' )
    parser.add_argument('-o', '--output', type=str, required=True, help='Path to an output file to be created' )
    args = parser.parse_args()

    assemblies = dict()
    current_assembly = None
    
    gene = None
    mRNAs = dict()
    in_sequence = False
    current_sequence = None
    current_gene_comment_lines = list()

    ## Used for tracking the exon count for each gene (for ID purposes)
    exon_count_by_mRNA = dict()
    
    fout = open(args.output, mode='wt', encoding='utf-8')
    fout.write("##gff-version 3\n")

    for line in open(args.input):
        if line.startswith("#"):
            ## Skip any header comments since we printed our own
            if line.startswith("##gff-version"):
                continue
            
            current_gene_comment_lines.append(line)
            
            if line.startswith("# end gene "):
                ## purge the comments, then write the gene
                fout.write( "".join(current_gene_comment_lines) )
                gene.print_as(fh=fout, source='AUGUSTUS', format='gff3')

                gene = None
                mRNAs = dict()
                in_sequence = False
                current_sequence = None
                current_gene_comment_lines = list()

            elif line.startswith("# protein sequence = ["):
                pass
            elif in_sequence is True:
                # build 'current_sequence'
                pass

        else:
            cols = line.split("\t")

            if len(cols) != 9:
                continue

            mol_id = cols[0]
            feat_type = cols[2]

            if feat_type not in ['gene', 'transcript', 'CDS']:
                continue

            ## The output format is GTF by default and (mostly) GFF if the --gff option is used.
            #   If GTF is detected, let's start by transforming the 9th column into GFF so the
            #   libraries can use it
            #   g1  ->  ID=g1
            #   g1.t1  ->  ID=g1.t1;Parent=g1
            #   transcript_id "g1.t1"; gene_id "g1";  ->  ID=g1.t1.cds;Parent=g1.t1
            m_gene = re.match('(g\d+)', cols[8])
            m_transcript = re.match('((g\d+).t\d+)', cols[8])
            m_CDS = re.match('transcript_id "(g\d+.t\d+)"; gene_id "g\d+";', cols[8])

            # the input can be in GTF or GFF.  We need to reformat the 9th column for the GTF entries
            if not cols[8].startswith('ID') and not cols[8].startswith('Parent'):
                if feat_type == 'gene':
                    if m_gene:
                        cols[8] = "ID={0}".format(m_gene.group(1))
                    else:
                        raise Exception("ERROR: GTF detected but gene row has bad 9th column format: {0}".format(cols[8]))
                elif feat_type == 'transcript':
                    if m_transcript:
                        cols[8] = "ID={0};Parent={1}".format(m_transcript.group(1), m_transcript.group(2))
                    else:
                        raise Exception("ERROR: GTF detected but transcript row has bad 9th column format: {0}".format(cols[8]))
                elif feat_type == 'CDS':
                    if m_CDS:
                        cols[8] = "ID={0}.cds;Parent={0}".format(m_CDS.group(1))
                    else:
                        raise Exception("ERROR: GTF detected but CDS row has bad 9th column format: {0}".format(cols[8]))

            feat_id = gff.column_9_value(cols[8], 'ID')

            ## initialize this assembly if we haven't seen it yet
            if mol_id not in assemblies:
                assemblies[mol_id] = things.Assembly(id=mol_id)

            current_assembly = assemblies[mol_id]

            if feat_type == "gene":
                gene = things.Gene(id=feat_id)
                gene.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )

            elif feat_type == "transcript":
                mRNA = things.mRNA(id=feat_id, parent=gene)
                mRNA.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )
                gene.add_mRNA(mRNA)
                mRNAs[mRNA.id] = mRNA

                if feat_id in exon_count_by_mRNA:
                    raise Exception( "ERROR: two different mRNAs found with same ID: {0}".format(feat_id) )
                else:
                    exon_count_by_mRNA[feat_id] = 0
                    
            elif feat_type == "CDS":
                parent_id = gff.column_9_value(cols[8], 'Parent')

                ## sanity check that we've seen this parent
                if parent_id not in mRNAs:
                    raise Exception("ERROR: Found CDS column with parent ({0}) mRNA not yet in the file".format(parent_id))

                CDS = things.CDS(id=feat_id, parent=mRNAs[parent_id])
                CDS.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6], phase=int(cols[7]) )
                mRNA.add_CDS(CDS)
                
                ## exons weren't explicitly defined in the input file, so we need to derive new IDs for them
                exon_count_by_mRNA[parent_id] += 1
                exon_id = "{0}.exon{1}".format(parent_id, exon_count_by_mRNA[parent_id])
                
                exon = things.Exon(id=exon_id, parent=mRNAs[parent_id])
                exon.locate_on( target=current_assembly, fmin=int(cols[3]) - 1, fmax=int(cols[4]), strand=cols[6] )
                mRNA.add_exon(exon)
        

if __name__ == '__main__':
    main()
