# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Checkspace 29/05/2020


"""
__author__="raul.ruiz"

from colorama import Fore, init
import sys
import os
import argparse
from anytree import AnyNode, RenderTree
 

def banner():
    print("\n" + 
        Fore.WHITE + " Checkspace " + Fore.RED + "raul.ruiz" + Fore.BLUE
    
    )

 
 
def getFolderSize(currentNode,path):
    _foldersize = 0.00


    
    
    #Loop at folder content  
    for file in os.listdir(path):
        try:
            # If file is a folder, call recursively this funcion to add subfolder size
            if os.path.isdir(os.path.join(path,file)):
                # Create note for subfolder
                node =  AnyNode(id=path,text=file,size=0,parent= currentNode)
                # Obtain size of subfolder 
                subfolderSize = float(getFolderSize(node, os.path.join(path,file) ))
                  
                _foldersize = _foldersize + subfolderSize 
            # Otherwise, add filesize         
            else:
                _foldersize =  _foldersize + float(os.stat(os.path.join(path,file) ).st_size)
        except PermissionError:
            print(Fore.RED + 'Error:', Fore.WHITE+'Access denied for '+os.path.join(path,file))
            _foldersize = 0
    #print(level*'>' , os.path.splitext(os.path.basename(path))[0], round(_foldersize / 1024 / 1024,2))
    currentNode.size = _foldersize /1024 / 1024
    return _foldersize



def checksSpace(path):
    # Root node
    tree = AnyNode(id=path,text=os.path.splitext(os.path.basename(path))[0],size=0)
    
    # Recursively, obtain size of folders
    getFolderSize(tree,path) 

    # Show tree
    level = args['maxlevel'] if args['maxlevel'] else None
    for pre, _, node in RenderTree(tree, maxlevel = level):
        if ( ( not args['size']) or (args['size'] and  node.size > args['size']) ):
            print("%s%s" % (Fore.WHITE+pre, Fore.WHITE+ node.text+(Fore.RED if node.size > 100 else Fore.GREEN )+"("+str(round(node.size,2))+"Mb)"))
    #print(RenderTree(tree, maxlevel = 2))
    

if __name__ == "__main__":
    #Control arguments with parser
    argparser = argparse.ArgumentParser(description='Check folder size')

    # Add the arguments
    argparser.add_argument('path',
                       metavar='path',
                       type=str,
                       help='Path to process')
    argparser.add_argument('--maxlevel', type=int, required=False, action='store', help='Level of depth to consider')                       
    argparser.add_argument('--size', type=int, required=False, action='store', help='Show only folders over size specified in Mb')                       
     
    
    # Execute the parse_args() method
    args = vars(argparser.parse_args())
   
   
    
    # 
    if not os.path.isdir(args['path']):
        print('The path specified does not exist')
        sys.exit()
    
    else:
       checksSpace(args['path'])
 