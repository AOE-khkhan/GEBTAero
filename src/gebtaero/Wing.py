# coding=UTF-8
import numpy as np

## This class represent the wing and is used by the class Simulation to generate the InputFile
class Wing:
    def __init__(self,Name,WingRootPosition):
        ## the name of the wing used to generate the different files
        self.Name = Name
        ## the 3D coordinate of the wing root
        self.WingRootPosition = np.copy(WingRootPosition)
        
        ## a list containing the wing sections
        self.WingSections = []
        ## a list containing the wing frames
        self.Frames = []
        ## a list containing the wing cross sections
        self.CrossSections = []
        ## a list containing the wing keypoints (cf )
        self.KpList = []
        self.KpList.append(WingRootPosition)
        
    def GetWingRootPosition(self):
        return self.WingRootPosition
    
    def GetName(self):
        return self.Name    
        
    ## Add a wing section to the wing and update internal values        
    #@param WingSection the WingSection to add
    def AppendWingSection(self,WingSection):
        # add the wing section
        self.WingSections.append(WingSection)
        
        # add the cross section if not in the list
        if WingSection.GetCrossSection() not in self.CrossSections:
            self.CrossSections.append(WingSection.GetCrossSection())
        # add the frame if not in the list 
        if WingSection.GetFrame() not in self.Frames:
            self.Frames.append(WingSection.GetFrame())
        # add a keypoint to the list
        self.KpList.append(self.KpList[-1]+WingSection.GetFrame().GetAxis()*WingSection.GetSectionLength())
           
    def GetWingSections(self):
        return self.WingSections
        
    def GetCrossSections(self):
        return self.CrossSections

    def GetFrames(self):
        return self.Frames
        
    def GetKpList(self):
        return self.KpList    
        
    ## Compute the weight of the wing using the mass per unit length in the mass mastrix
    #@return the weight of the wing    
    def GetWeight(self):
        WS = self.GetWingSections()
        Weight = 0.
        for Section in WS:
            Weight = Weight + Section.GetSectionLength()*Section.GetCrossSection().GetMassMatrix()[0][0]
        Weight = Weight*9.81
        return Weight     
        
    ## Compute the wing surface using the chord and length of the sections    
    #@return the wing surface
    def GetSurface(self):
        WS = self.GetWingSections()
        Surface = 0.
        for Section in WS:
            Surface = Surface + Section.GetSectionLength()*Section.GetChord()
        return Surface    
        
    ## Modify the length of oneWingSection of the wing and upadte the keypoint list
    def ModifySectionLength(self,index,SectionLength):
        if index>len(self.GetWingSections()):
            raise RuntimeError("the index is greater than the number of wing sections")
        self.WingSections[index].SetSectionLength(SectionLength)   
        # update the liste of key point position
        self.KpList=[]
        self.KpList.append(self.WingRootPosition)
        for i in range(len(self.GetWingSections())):
            Section=self.GetWingSections()[i]
            self.KpList.append(self.KpList[-1]+Section.GetFrame().GetAxis()*Section.GetSectionLength())
