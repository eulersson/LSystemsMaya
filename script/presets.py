'''
    Presets Module                                  <presets.py>
    
    This module contains some presets. The user will be able to select them in the main graphics user interface. The presets
    are taken from The Algorithmic Beaute of Plants (Astrid Lindenmayer and Przemyslaw Prusinkiewicz) and from internet sites
    such as Hung-Wen Chen's one (http://www.nbb.cornell.edu/neurobio/land/OldStudentProjects/cs490-94to95/hwchen/).
'''

class preset1:
    def __init__(*args):
        ''' Edits all the fields related to the string generation and calls the procedure. ''' 
        import maya.cmds as cmds
        import LS_string_rewriting
        cmds.textField( "axiomTextField", e=True, tx='F' )
        cmds.intSliderGrp( "depthIntField", e=True, v=4 )
        cmds.intField( "prodRuleProb1", e=True, v=100 )
        cmds.textField( "prodRulePred1", e=True, tx='F' )
        cmds.textField("prodRuleSucc1", e=True, tx='F[&+F]F[->FL][&FB]')
        cmds.checkBox( "prodRuleCheckBox2", e=True, value=False )
        cmds.checkBox("prodRuleCheckBox3", e=True, value=False)
        cmds.checkBox("prodRuleCheckBox4", e=True, value=False)
        cmds.textField( "output", e=True, tx='Press Generate String, please.' )
        cmds.floatSliderGrp("angle", e=True, v=28)
        cmds.floatSliderGrp("length", e=True, v=1.20)
        cmds.floatSliderGrp("radius", e=True, v=0.20)
        cmds.intSliderGrp("cylSubdivs", e=True, v=5)
        cmds.intSliderGrp( "length_atenuation", e=True, v=95 )
        cmds.intSliderGrp( "radius_atenuation", e=True, v=85 )
        cmds.floatSliderGrp("turtleSpeed", e=True, v=0)
        cmds.colorSliderGrp( 'rgb_blossomField', e=True, rgb=(0.624,0,0) )
        cmds.colorSliderGrp( 'rgb_leafField', e=True, rgb=(0,0.624,0) )
        cmds.colorSliderGrp( 'rgb_branchField', e=True, rgb=(0.430,0.230,0.11) )

class preset2:
    def __init__(*args):
        ''' Edits all the fields related to the string generation and calls the procedure. ''' 
        import maya.cmds as cmds
        import LS_string_rewriting
        cmds.textField( "axiomTextField", q=True, tx=True )
        cmds.intSliderGrp( "depthIntField", e=True, v=3 )
        cmds.intField( "prodRuleProb1", e=True, v=100 )
        cmds.textField( "prodRulePred1", e=True, tx='F' )
        cmds.textField("prodRuleSucc1", e=True, tx='F[+FL][-FB][&FL][^FB]F')
        cmds.checkBox( "prodRuleCheckBox2", e=True, value=False )
        cmds.checkBox("prodRuleCheckBox3", e=True, value=False)
        cmds.checkBox("prodRuleCheckBox4", e=True, value=False)
        cmds.textField( "output", e=True, tx='Press Generate String, please.' )
        cmds.floatSliderGrp("angle", e=True, v=25.7)
        cmds.floatSliderGrp("length", e=True, v=3.32)
        cmds.floatSliderGrp("radius", e=True, v=0.50)
        cmds.intSliderGrp("cylSubdivs", e=True, v=6)
        cmds.intSliderGrp( "length_atenuation", e=True, v=90 )
        cmds.intSliderGrp( "radius_atenuation", e=True, v=70 )
        cmds.floatSliderGrp("turtleSpeed", e=True, v=0)
        cmds.colorSliderGrp( 'rgb_branchField', e=True, rgb=(0.242,0.129,0.070) )
        cmds.colorSliderGrp( 'rgb_leafField', e=True, rgb=(0,0.427,0) )
        cmds.colorSliderGrp( 'rgb_blossomField', e=True, rgb=(1.0,1.0,1.0) )


class preset3:
    def __init__(*args):
        ''' Edits all the fields related to the string generation and calls the procedure. ''' 
        import maya.cmds as cmds
        import LS_string_rewriting
        cmds.textField( "axiomTextField", q=True, tx=True )
        cmds.intSliderGrp( "depthIntField", e=True, v=4 )
        cmds.intField( "prodRuleProb1", e=True, v=100 )
        cmds.textField( "prodRulePred1", e=True, tx='F' )
        cmds.textField("prodRuleSucc1", e=True, tx='F[&+F]F[->F][&F]')
        cmds.checkBox( "prodRuleCheckBox2", e=True, value=False )
        cmds.checkBox("prodRuleCheckBox3", e=True, value=False)
        cmds.checkBox("prodRuleCheckBox4", e=True, value=False)
        cmds.textField( "output", e=True, tx='Press Generate String, please' )
        cmds.floatSliderGrp("angle", e=True, v=28)
        cmds.floatSliderGrp("length", e=True, v=1.20)
        cmds.floatSliderGrp("radius", e=True, v=0.20)
        cmds.intSliderGrp("cylSubdivs", e=True, v=5)
        cmds.intSliderGrp( "length_atenuation", e=True, v=100 )
        cmds.intSliderGrp( "radius_atenuation", e=True, v=100 )
        cmds.floatSliderGrp("turtleSpeed", e=True, v=0)
        cmds.colorSliderGrp( 'rgb_blossomField', e=True, rgb=(0.430,0.230,0.11) )
        cmds.colorSliderGrp( 'rgb_leafField', e=True, rgb=(0,0.624,0) )
        cmds.colorSliderGrp( 'rgb_branchField', e=True, rgb=(0.624,0,0) )
class preset4:
    def __init__(*args):
        ''' Edits all the fields related to the string generation and calls the procedure. ''' 
        import maya.cmds as cmds
        import LS_string_rewriting
        cmds.textField( "axiomTextField", q=True, tx=True )
        cmds.intSliderGrp( "depthIntField", e=True, v=4 )
        cmds.intField( "prodRuleProb1", e=True, v=100 )
        cmds.textField( "prodRulePred1", e=True, tx='F' )
        cmds.textField("prodRuleSucc1", e=True, tx='F[&+F]F[->F][&F]')
        cmds.checkBox( "prodRuleCheckBox2", e=True, value=False )
        cmds.checkBox("prodRuleCheckBox3", e=True, value=False)
        cmds.checkBox("prodRuleCheckBox4", e=True, value=False)
        cmds.textField( "output", e=True, tx='Press Generate String, please' )
        cmds.floatSliderGrp("angle", e=True, v=28)
        cmds.floatSliderGrp("length", e=True, v=1.20)
        cmds.floatSliderGrp("radius", e=True, v=0.20)
        cmds.intSliderGrp("cylSubdivs", e=True, v=5)
        cmds.intSliderGrp( "length_atenuation", e=True, v=100 )
        cmds.intSliderGrp( "radius_atenuation", e=True, v=100 )
        cmds.floatSliderGrp("turtleSpeed", e=True, v=0)
        cmds.colorSliderGrp( 'rgb_blossomField', e=True, rgb=(0.430,0.230,0.11) )
        cmds.colorSliderGrp( 'rgb_leafField', e=True, rgb=(0,0.624,0) )
        cmds.colorSliderGrp( 'rgb_branchField', e=True, rgb=(0.624,0,0) )