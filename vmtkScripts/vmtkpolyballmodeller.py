#!/usr/bin/env python

## Program:   VMTK
## Module:    $RCSfile: vmtkpolyballmodeller.py,v $
## Language:  Python
## Date:      $Date: 2005/09/14 09:49:59 $
## Version:   $Revision: 1.7 $

##   Copyright (c) Luca Antiga, David Steinman. All rights reserved.
##   See LICENCE file for details.

##      This software is distributed WITHOUT ANY WARRANTY; without even 
##      the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR 
##      PURPOSE.  See the above copyright notices for more information.


import vtk
import sys
import vtkvmtk
import pypes

vmtkpolyballmodeller = 'vmtkPolyBallModeller'

class vmtkPolyBallModeller(pypes.pypeScript):

    def __init__(self):

        pypes.pypeScript.__init__(self)
        
        self.Surface = None
        self.RadiusArrayName = None
        self.Image = None
        self.ModelBounds = None 
        self.SampleDimensions = [64,64,64]

        self.SetScriptName('vmtkpolyballmodeller')
        self.SetScriptDoc('converts a polyball to an image containing the tube function')
        self.SetInputMembers([
            ['Surface','i','vtkPolyData',1,'','the input surface','vmtksurfacereader'],
            ['RadiusArrayName','radiusarray','str',1,'','name of the array where radius values are stored'],
            ['SampleDimensions','dimensions','int',3,'(0,)','dimensions of the output image'],
            ['ModelBounds','bounds','float',6,'(0.0,)','model bounds in physical coordinates (if None, they are computed automatically)']
            ])
        self.SetOutputMembers([
            ['Image','o','vtkImageData',1,'','the output image','vmtkimagewriter']])

    def Execute(self):

        if self.Surface == None:
            self.PrintError('Error: No input surface.')

        if self.RadiusArrayName == None:
            self.PrintError('Error: No radius array name.')

        modeller = vtkvmtk.vtkvmtkPolyBallModeller()
        modeller.SetInput(self.Surface)
        modeller.SetRadiusArrayName(self.RadiusArrayName)
        modeller.UsePolyBallLineOff()
        modeller.SetSampleDimensions(self.SampleDimensions)
        if self.ModelBounds:
            modeller.SetModelBounds(self.ModelBounds)
        modeller.Update()

        self.Image = modeller.GetOutput()
        
        if self.Image.GetSource():
            self.Image.GetSource().UnRegisterAllOutputs()


if __name__=='__main__':

    main = pypes.pypeMain()
    main.Arguments = sys.argv
    main.Execute()