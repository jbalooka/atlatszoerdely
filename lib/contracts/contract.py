#!/usr/local/bin/python2.7
# encoding: utf-8
'''
contracts.contract -- Parses and Pushes data from CSV files to a Neo4j Database

contracts.contract Full 

It defines classes_and_methods

@author:     Bela - Tamas Jozsa

@copyright:  2017 Atlatszo Erdely. All rights reserved.

@license:    license

@contact:    jozsa.bela.tamas@gmail.com
@deffield    updated: 2017.02.03
'''

import sys

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from neo4j.v1 import GraphDatabase, basic_auth
import csv
from robotide.editor.dialoghelps import row

__all__ = []
__version__ = 0.1
__date__ = '2017-01-27'
__updated__ = '2017-01-27'

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg
    
def import_contracts_from_csv(file_path, target_org_name, delimiter='\t', db_data={}):
    with open(file_path, 'rb') as csvfile:
        contractsreader = csv.reader(csvfile, delimiter=delimiter)
        year = 'N/A'
        for row in contractsreader:
            if is_year(row):
                year = get_year(row)
                print "Setting Year to: " + str(year)
            elif is_row_empty(row):
                print "SKIP"
            else:
                print "ROW: " + "|".join(row)
                savetodb(target_org_name, year, row, db_data);

def is_row_empty(row):
    return len("".join(row).strip()) == 0


def savetodb(target_org_name, year, row, db_data):
    company_name = row[1]
    driver = GraphDatabase.driver(db_data['url'], 
                                  auth=basic_auth(db_data['username'], db_data['password']))
    session = driver.session()
    
    if not is_company_found(session, company_name):
        session.run("CREATE (c:Company { name: {name} })", {"name": row[1]})
        session.sync
    
    if not is_org_found(session, target_org_name):
        session.run("CREATE (o:Organization { name: {name} })", {"name": target_org_name})
        session.sync

    session.run("MATCH (o:Organization), (c:Company) WHERE o.name = {org_name} AND c.name  = {company_name} " +
                "CREATE (o) - [ k:CONTRACTED {year: {year}, nr: {nr}, value: {value}, " +
                "objective: {objective} } ] -> (c)", 
                {"org_name" : target_org_name, "company_name" : row[1], "year" : year, 
                 "nr" : row[2], "value" : row[3], "objective" : row[4]})
    session.sync
    session.close()


def is_company_found(session, company_name):
    result = session.run("MATCH (c:Company {name: {company_name} } ) RETURN (c)", 
                {"company_name" : company_name})
    
    return len(list(result)) > 0

def is_org_found(session, org_name):
    result = session.run("MATCH (o:Organization {name: {org_name} })  RETURN (o)", 
                {"org_name" : org_name})
    
    return len(list(result)) > 0


def is_year(row):
    return get_year(row) > 0;
    
def get_year(row):
    year = "".join(row)
    return int(year) if year.isdigit() else 0;

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2017 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-f", "--file", dest="file", help="Full path of the file to be imported")
    parser.add_argument("-o", "--org", dest="org_name", help="Name of the Organization")
    parser.add_argument("--db-url", dest="db_url", help="URL of the Database", default="bolt://localhost:7687")
    parser.add_argument("--db-usr", dest="db_usr", help="Username of the DB User", default="neo4j")
    parser.add_argument("--db-pwd", dest="db_pwd", help="Password of the DB User", default="admin")
    parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
    parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
    # Process arguments
    args = parser.parse_args()

    verbose = args.verbose

    if verbose > 0:
        print("Verbose mode on")
    db_data = {"url" : args.db_url, "username" : args.db_usr, "password" : args.db_pwd}
    import_contracts_from_csv(args.file, args.org_name, '\t', db_data)
    return 0

if __name__ == "__main__":
    sys.exit(main())