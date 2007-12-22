from transaction import commit

from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.contentrules.engine.interfaces import IRuleAssignmentManager
from plone.contentrules.engine.interfaces import IRuleStorage

from plone.app.contentrules.tests.base import ContentRulesTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.context import TarballExportContext

from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase

from zope.lifecycleevent.interfaces import IObjectModifiedEvent

zcml_string = """\
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:gs="http://namespaces.zope.org/genericsetup"
           package="plone.app.contentrules">

    <gs:registerProfile
        name="testing"
        title="plone.app.contentrules testing"
        description="Used for testing only" 
        directory="tests/profiles/testing"
        for="Products.CMFCore.interfaces.ISiteRoot"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        />
        
</configure>
"""

class TestContentrulesGSLayer(PloneSite):
    
    @classmethod
    def setUp(cls):
        
        fiveconfigure.debug_mode = True
        zcml.load_string(zcml_string)
        fiveconfigure.debug_mode = False
        
        app = ZopeTestCase.app()
        portal = app.plone
        
        portal_setup = portal.portal_setup
        portal_setup.runAllImportStepsFromProfile('profile-plone.app.contentrules:testing')
        
        commit()
        ZopeTestCase.close(app)

    @classmethod
    def tearDown(cls):
        app = ZopeTestCase.app()
        portal = app.plone
        
        storage = getUtility(IRuleStorage, context=portal)
        for key in list(storage.keys()):
            del storage[key]
        
        commit()
        ZopeTestCase.close(app)

class TestGenericSetup(ContentRulesTestCase):

    layer = TestContentrulesGSLayer
    
    def afterSetUp(self):
        self.storage = getUtility(IRuleStorage)
    
    def testRuleInstalled(self):
        self.failUnless('test1' in self.storage)
        self.failUnless('test2' in self.storage)
        
    def testRulesConfigured(self):
        rule1 = self.storage['test1']
        self.assertEquals("Test rule 1", rule1.title)
        self.assertEquals("A test rule", rule1.description)
        self.assertEquals(IObjectModifiedEvent, rule1.event)
        self.assertEquals(True, rule1.enabled)
        self.assertEquals(False, rule1.stop)
        
        self.assertEquals(2, len(rule1.conditions))
        self.assertEquals("plone.conditions.PortalType", rule1.conditions[0].element)
        self.assertEquals(["Document", "News Item"], list(rule1.conditions[0].check_types))
        self.assertEquals("plone.conditions.Role", rule1.conditions[1].element)
        self.assertEquals(["Manager"], list(rule1.conditions[1].role_names))
        
        self.assertEquals(1, len(rule1.actions))
        self.assertEquals("plone.actions.Notify", rule1.actions[0].element)
        self.assertEquals("A message", rule1.actions[0].message)
        self.assertEquals("info", rule1.actions[0].message_type)
        
        rule2 = self.storage['test2']
        self.assertEquals("Test rule 2", rule2.title)
        self.assertEquals("Another test rule", rule2.description)
        self.assertEquals(IObjectModifiedEvent, rule2.event)
        self.assertEquals(False, rule2.enabled)
        self.assertEquals(True, rule2.stop)
        
        self.assertEquals(1, len(rule2.conditions))
        self.assertEquals("plone.conditions.PortalType", rule2.conditions[0].element)
        self.assertEquals(["Event"], list(rule2.conditions[0].check_types))
        
        self.assertEquals(1, len(rule2.actions))
        self.assertEquals("plone.actions.Workflow", rule2.actions[0].element)
        self.assertEquals("publish", rule2.actions[0].transition)
        
    def testRuleAssigned(self):
        assignable = IRuleAssignmentManager(self.portal.news)
        self.assertEquals(3, len(assignable))
        
        self.assertEquals(True, assignable['test1'].enabled)
        self.assertEquals(False, assignable['test1'].bubbles)
        
        self.assertEquals(False, assignable['test2'].enabled)
        self.assertEquals(True, assignable['test2'].bubbles)
        
        self.assertEquals(False, assignable['test3'].enabled)
        self.assertEquals(False, assignable['test3'].bubbles)
        
    def testAssignmentOrdering(self):
        assignable = IRuleAssignmentManager(self.portal.news)
        self.assertEquals([u'test3', u'test2', u'test1'], assignable.keys())
        
    def testExport(self):
        site = self.portal
        context = TarballExportContext(self.portal.portal_setup)
        exporter = getMultiAdapter((site, context), IBody, name=u'plone.contentrules')
        
        expected = """\
<?xml version="1.0"?>
<contentrules>
 <rule name="test1" title="Test rule 1" description="A test rule"
    enabled="True" event="zope.lifecycleevent.interfaces.IObjectModifiedEvent"
    stop-after="False">
  <conditions>
   <condition type="plone.conditions.PortalType">
    <property name="check_types">
     <element>Document</element>
     <element>News Item</element>
    </property>
   </condition>
   <condition type="plone.conditions.Role">
    <property name="role_names">
     <element>Manager</element>
    </property>
   </condition>
  </conditions>
  <actions>
   <action type="plone.actions.Notify">
    <property name="message">A message</property>
    <property name="message_type">info</property>
   </action>
  </actions>
 </rule>
 <rule name="test2" title="Test rule 2" description="Another test rule"
    enabled="False"
    event="zope.lifecycleevent.interfaces.IObjectModifiedEvent"
    stop-after="True">
  <conditions>
   <condition type="plone.conditions.PortalType">
    <property name="check_types">
     <element>Event</element>
    </property>
   </condition>
  </conditions>
  <actions>
   <action type="plone.actions.Workflow">
    <property name="transition">publish</property>
   </action>
  </actions>
 </rule>
 <rule name="test3" title="Test rule 3" description="Third test rule"
    enabled="True" event="zope.app.container.interfaces.IObjectMovedEvent"
    stop-after="False">
  <conditions/>
  <actions/>
 </rule>
 <assignment name="test3" bubbles="False" enabled="False" location="/news"/>
 <assignment name="test2" bubbles="True" enabled="False" location="/news"/>
 <assignment name="test1" bubbles="False" enabled="True" location="/news"/>
</contentrules>
"""

        body = exporter.body
        self.assertEquals(expected.strip(), body.strip(), body)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestGenericSetup))
    return suite
