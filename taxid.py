#!/usr/bin/env python
# -*- coding: utf-8 -*-
#09/2017

__author__ = 'Igor Rodrigues da Costa'
__contact__ = 'igor.bioinfo@gmail.com'

import sys
from Bio import Entrez
from urllib2 import URLError

def argument_parser(hlp = False):
    '''taxid.py -i /path/to/tabfile/tab.csv -o /path/to/output/out.txt
    Output default: current working directory.'''

    default_out = os.getcwd() + '/'
    parser = argparse.ArgumentParser(description='taxid is a script to search NCBI taxonomy for a given species name and
    return its taxonomy ID.',\
                                     argument_default = None, fromfile_prefix_chars = '@')
    parser.add_argument('-i', '--infile', nargs='?', type=str, required=True,\
                        dest='infile', help='Path to the file with tabular data. (default: %(default)s)')
    parser.add_argument('-o', '--outfile', nargs='?', type=str, default=default_out,\
                        dest='outfile', help='Path were the ids will be saved. (default: %(default)s)')
    parser.add_argument('-i', '--ibama', nargs='?', const=True, default=True,\
                        dest='ibama', help='Flag for ibama data. (default: %(default)s)')
    parser.add_argument('-r', '--revizee', nargs='?', const=True, default=False,\
                        dest='revizee', help='Flag for revizee data. (default: %(default)s)')
    parser.add_argument('-h', '--habitat', nargs='?', const=True, default=False,\
                        dest='habitat', help='Flag to habitat data. (default: %(default)s)')
    if hlp:
        args = parser.parse_args(['-h'])
    else:
        args = parser.parse_args().__dict__
    return args
def search_id(term):
    Entrez.email = "igorrcosta@hotmail.com"
    try:
        taxid = Entrez.esearch(db = 'taxonomy', term=term)
    except URLError:
        taxid = Entrez.esearch(db = 'taxonomy', term=term)
    record = Entrez.read(taxid)
    taxid.close()
    if 'ErrorList' in record:
        return []
    return record['IdList']

def get_rank(taxid):
    Entrez.email = "igorrcosta@hotmail.com"
    try:
        handle = Entrez.efetch(db="taxonomy", id=taxid)
    except URLError:
        handle = Entrez.efetch(db="taxonomy", id=taxid)
    record = Entrez.read(handle)
    handle.close()
    rank = record[0]['Rank']
    return rank

def revizee(infile, outfile):
    found = 0
    separator = '\t'
    with open(infile, 'r') as ref_file, open(outfile, 'w') as out:
        for l in ref_file:
            try:
                genero = ''
                especie = ''
                taxid = []
                rank = ''
                cod  = int(l.split(separator)[0])
                especie = l.split(separator)[5].split(',')[0]
                if len(especie.split()) > 1:
                    genero = especie.split()[0]
                familia = l.split(separator)[4]
                ordem = l.split(separator)[3]
                classe = l.split(separator)[2]
                filo = l.split(separator)[1]
                if especie:
                    rank = 'especie'
                    taxid = search_id(especie)
                if not taxid and genero:
                    rank = 'genero'
                    taxid = search_id(genero)
                if not taxid and familia:
                    rank = 'familia'
                    taxid = search_id(familia)
                if not taxid:
                    taxid = ['not found']
                out.write('\t'.join([taxid[0], rank])+'\n')
            except ValueError:
                pass

def habitat(infile, outfile):
    found = 0
    separator = '\t'
    with open(infile, 'r') as ref_file, open(outfile, 'w') as out:
        for l in ref_file:
            try:
                genero = ''
                especie = ''
                taxid = []
                rank = ''
                cod  = int(l.split(separator)[0])
                especie = l.split(separator)[5]
                if len(especie.split()) > 1:
                    genero = especie.split()[0]
                rank_superior = l.split(separator)[3]
                rank_inferior = l.split(separator)[1]
                if especie:
                    taxid = search_id(especie)
                if not taxid and genero:
                    taxid = search_id(genero)
                if not taxid and rank_inferior:
                    taxid = search_id(rank_inferior)
                if not taxid:
                    taxid = ['not found']
                else:
                    rank = get_rank(taxid[0])
                out.write('\t'.join([taxid[0], rank])+'\n')
            except ValueError:
                pass

def ibama(infile, outfile):
    found = 0
    separator = '\t'
    with open(infile, 'r') as ref_file, open(outfile, 'w') as out:
        for l in ref_file:
            try:
                genero = ''
                especie = ''
                taxid = []
                rank = ''
                if len(l.split(separator)) > 4:
                    especie = l.split(separator)[4]
                    genero = l.split(separator)[3]
                    familia = l.split(separator)[2]
                    classe = l.split(separator)[1]
                    filo = l.split(separator)[0]
                    if especie:
                        rank = 'especie'
                        taxid = search_id(especie)
                    if not taxid and genero:
                        rank = 'genero'
                        taxid = search_id(genero)
                    if not taxid and familia:
                        rank = 'familia'
                        taxid = search_id(familia)
                if not taxid:
                    taxid = ['not found']
                out.write('\t'.join([taxid[0], rank])+'\n')
            except ValueError:
                pass
def main(args):
    if args['revizee']:
        revizee(args['infile'], args['outfile'])
    elif args['habitat']:
        habitat(args['infile'], args['outfile'])
    else:
        ibama(args['infile'], args['outfile'])

if __name__ == '__main__':
    args = argument_parser()
    main(args)
